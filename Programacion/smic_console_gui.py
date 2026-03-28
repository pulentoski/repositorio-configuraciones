# SMIC LoRa Mesh Console GUI
# ============================================================
# INSTALACIÓN:
#   pip install pyserial
#   (tkinter viene incluido con Python en Windows y la mayoría de Linux)
#
# En Ubuntu/Debian si falta tkinter:
#   sudo apt install python3-tk
#
# Agregar usuario al grupo dialout (Linux, para acceso a puertos serial):
#   sudo usermod -a -G dialout $USER
#   (requiere cerrar sesión y volver a entrar)
#
# USO:
#   python smic_console_gui.py
# ============================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import serial
import serial.tools.list_ports
import threading
import queue
import time
import datetime
import os
import sys

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

APP_TITLE   = "SMIC LoRa Mesh Console"
APP_VERSION = "1.0.0"
BAUD_DEFAULT = 115200

# VID/PID conocidos → nombre del chip
KNOWN_DEVICES = {
    (0x10C4, 0xEA60): "Silicon Labs CP2102 (Heltec V3)",
    (0x303A, 0x1001): "Espressif (XIAO ESP32-S3)",
    # variantes adicionales
    (0x1A86, 0x7523): "CH340 (ESP32 genérico)",
    (0x0403, 0x6001): "FTDI FT232R",
    (0x2341, 0x0043): "Arduino Uno",
}

# Colores del log
LOG_COLORS = {
    "green":  "#4EC94E",
    "cyan":   "#4EC9E0",
    "yellow": "#D4D44E",
    "red":    "#E04E4E",
    "gray":   "#909090",
    "white":  "#E0E0E0",
}

# Palabras clave → color
def classify_line(line: str) -> str:
    l = line.upper()
    if any(k in l for k in ("BEACON", "VECIN", "NEIGHBOR", "ROUT", "MESH")):
        return "green"
    if any(k in l for k in ("RECV", "MSG:", "RECIBIDO", "RX")):
        return "cyan"
    if any(k in l for k in ("STAT", "INFO", "TX", "UPTIME", "FREE")):
        return "yellow"
    if any(k in l for k in ("ERROR", "FAIL", "ERR:", "WARN", "TIMEOUT")):
        return "red"
    return "gray"


# ---------------------------------------------------------------------------
# Hilo de lectura serial
# ---------------------------------------------------------------------------

class SerialReader(threading.Thread):
    """Lee líneas del puerto serial y las deposita en una cola."""

    def __init__(self, port: str, baud: int, rx_queue: queue.Queue,
                 status_cb, reconnect_delay: float = 3.0):
        super().__init__(daemon=True)
        self.port           = port
        self.baud           = baud
        self.rx_queue       = rx_queue
        self.status_cb      = status_cb
        self.reconnect_delay = reconnect_delay
        self._stop_event    = threading.Event()
        self._ser: serial.Serial | None = None
        self.connected      = False

    # ── API pública ──────────────────────────────────────────────────────────

    def send(self, data: str):
        if self._ser and self._ser.is_open:
            try:
                self._ser.write((data + "\r\n").encode("utf-8"))
            except serial.SerialException:
                pass

    def stop(self):
        self._stop_event.set()
        if self._ser and self._ser.is_open:
            try:
                self._ser.close()
            except Exception:
                pass

    # ── Bucle principal ──────────────────────────────────────────────────────

    def run(self):
        while not self._stop_event.is_set():
            try:
                self._ser = serial.Serial(
                    self.port, self.baud,
                    timeout=1,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                )
                self.connected = True
                self.status_cb("connected", self.port, self.baud)
                self._read_loop()
            except serial.SerialException as e:
                self.connected = False
                self.status_cb("error", str(e), 0)
                if not self._stop_event.is_set():
                    time.sleep(self.reconnect_delay)
            finally:
                if self._ser and self._ser.is_open:
                    try:
                        self._ser.close()
                    except Exception:
                        pass
                if not self._stop_event.is_set():
                    self.connected = False
                    self.status_cb("reconnecting", self.port, self.baud)

    def _read_loop(self):
        while not self._stop_event.is_set():
            try:
                raw = self._ser.readline()
                if raw:
                    line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                    if line:
                        self.rx_queue.put(line)
            except serial.SerialException:
                break
            except Exception:
                break


# ---------------------------------------------------------------------------
# Aplicación principal
# ---------------------------------------------------------------------------

class SMICConsole(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE}  v{APP_VERSION}")
        self.minsize(900, 580)
        self.configure(bg="#1E1E1E")

        # Estado
        self._reader: SerialReader | None = None
        self._rx_queue: queue.Queue       = queue.Queue()
        self._packet_count: int           = 0
        self._log_file                    = None
        self._log_path: str               = ""

        # Fuentes
        self._font_mono  = ("Consolas", 10) if sys.platform == "win32" else ("Monospace", 10)
        self._font_ui    = ("Segoe UI", 10) if sys.platform == "win32" else ("Sans", 10)
        self._font_bold  = ("Segoe UI", 10, "bold") if sys.platform == "win32" else ("Sans", 10, "bold")

        self._build_ui()
        self._configure_log_tags()
        self._scan_ports()
        self._poll_queue()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ════════════════════════════════════════════════════════════════════════
    # Construcción de UI
    # ════════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        # ── Barra superior de conexión ────────────────────────────────────
        top = tk.Frame(self, bg="#252526", pady=4, padx=6)
        top.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top, text="Puerto:", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).pack(side=tk.LEFT)

        self._port_var = tk.StringVar()
        self._port_cb  = ttk.Combobox(top, textvariable=self._port_var,
                                       width=34, state="readonly",
                                       font=self._font_ui)
        self._port_cb.pack(side=tk.LEFT, padx=(4, 8))

        tk.Label(top, text="Baud:", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).pack(side=tk.LEFT)
        self._baud_var = tk.StringVar(value=str(BAUD_DEFAULT))
        baud_entry = tk.Entry(top, textvariable=self._baud_var, width=8,
                              bg="#3C3C3C", fg="#E0E0E0",
                              insertbackground="white",
                              font=self._font_mono)
        baud_entry.pack(side=tk.LEFT, padx=(4, 8))

        self._btn_connect = tk.Button(
            top, text="Conectar", command=self._toggle_connect,
            bg="#0E7A0E", fg="white", activebackground="#117711",
            font=self._font_bold, relief=tk.FLAT, padx=10)
        self._btn_connect.pack(side=tk.LEFT, padx=2)

        tk.Button(top, text="Actualizar", command=self._scan_ports,
                  bg="#3C3C3C", fg="#CCCCCC", activebackground="#505050",
                  font=self._font_ui, relief=tk.FLAT, padx=8
                  ).pack(side=tk.LEFT, padx=2)

        # Checkbox log a archivo
        self._save_log_var = tk.BooleanVar(value=False)
        tk.Checkbutton(top, text="Guardar log", variable=self._save_log_var,
                       command=self._toggle_log_file,
                       bg="#252526", fg="#CCCCCC", selectcolor="#3C3C3C",
                       activebackground="#252526", activeforeground="#CCCCCC",
                       font=self._font_ui).pack(side=tk.LEFT, padx=(12, 0))

        self._log_path_lbl = tk.Label(top, text="", bg="#252526",
                                       fg="#6A9955", font=self._font_ui)
        self._log_path_lbl.pack(side=tk.LEFT, padx=4)

        # ── Paneles principales ───────────────────────────────────────────
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL,
                               bg="#1E1E1E", sashwidth=5,
                               sashrelief=tk.FLAT)
        paned.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Panel izquierdo — Log
        left_frame = tk.Frame(paned, bg="#1E1E1E")
        paned.add(left_frame, minsize=400, stretch="always")

        self._build_log_panel(left_frame)

        # Panel derecho — Control
        right_frame = tk.Frame(paned, bg="#252526", width=280)
        paned.add(right_frame, minsize=250, stretch="never")

        self._build_control_panel(right_frame)

        # Ajuste proporcional inicial 70/30
        self.update_idletasks()
        total = self.winfo_width()
        if total > 10:
            paned.sash_place(0, int(total * 0.70), 0)

        # ── Barra de estado ───────────────────────────────────────────────
        self._build_status_bar()

    # ── Panel de log ─────────────────────────────────────────────────────────

    def _build_log_panel(self, parent):
        header = tk.Frame(parent, bg="#252526")
        header.pack(fill=tk.X)

        tk.Label(header, text="LOG EN TIEMPO REAL",
                 bg="#252526", fg="#9CDCFE",
                 font=self._font_bold).pack(side=tk.LEFT, padx=6, pady=3)

        tk.Button(header, text="Limpiar", command=self._clear_log,
                  bg="#3C3C3C", fg="#CCCCCC", activebackground="#505050",
                  font=self._font_ui, relief=tk.FLAT, padx=6
                  ).pack(side=tk.RIGHT, padx=4, pady=2)

        self._log_text = scrolledtext.ScrolledText(
            parent,
            bg="#1E1E1E", fg="#E0E0E0",
            font=self._font_mono,
            state=tk.DISABLED,
            wrap=tk.WORD,
            insertbackground="white",
            selectbackground="#264F78",
            relief=tk.FLAT,
            padx=4, pady=4,
        )
        self._log_text.pack(fill=tk.BOTH, expand=True)

    # ── Panel de control ─────────────────────────────────────────────────────

    def _build_control_panel(self, parent):
        # Scrollable container
        canvas   = tk.Canvas(parent, bg="#252526", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                   command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(canvas, bg="#252526")
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _resize(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(win_id, width=event.width)

        inner.bind("<Configure>", _resize)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        p = inner  # alias corto

        # ── Sección: Comando libre ────────────────────────────────────────
        self._section(p, "COMANDO")

        cmd_row = tk.Frame(p, bg="#252526")
        cmd_row.pack(fill=tk.X, padx=6, pady=(0, 4))

        self._cmd_var = tk.StringVar()
        cmd_entry = tk.Entry(cmd_row, textvariable=self._cmd_var,
                             bg="#3C3C3C", fg="#E0E0E0",
                             insertbackground="white",
                             font=self._font_mono, relief=tk.FLAT)
        cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        cmd_entry.bind("<Return>", lambda e: self._send_command())

        tk.Button(cmd_row, text="Enviar",
                  command=self._send_command,
                  bg="#0078D7", fg="white", activebackground="#1080DD",
                  font=self._font_ui, relief=tk.FLAT, padx=8
                  ).pack(side=tk.LEFT, padx=(4, 0))

        # ── Botones rápidos ───────────────────────────────────────────────
        self._section(p, "ACCIONES RÁPIDAS")

        quick_cmds = [
            ("help",      "help"),
            ("info",      "info"),
            ("neighbors", "neighbors"),
            ("routes",    "routes"),
            ("stats",     "stats"),
            ("beacon",    "beacon"),
            ("screen",    "screen"),
            ("reboot",    "reboot"),
        ]

        btn_frame = tk.Frame(p, bg="#252526")
        btn_frame.pack(fill=tk.X, padx=6, pady=(0, 6))

        for i, (label, cmd) in enumerate(quick_cmds):
            btn = tk.Button(
                btn_frame, text=label,
                command=lambda c=cmd: self._send_raw(c),
                bg="#3C3C3C", fg="#9CDCFE",
                activebackground="#505050",
                font=self._font_ui, relief=tk.FLAT,
                width=9, padx=2, pady=2,
            )
            btn.grid(row=i // 2, column=i % 2, padx=2, pady=2, sticky="ew")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # ── Sección: Mensajes ─────────────────────────────────────────────
        self._section(p, "MENSAJES")

        msg_frame = tk.Frame(p, bg="#252526")
        msg_frame.pack(fill=tk.X, padx=6, pady=(0, 6))

        tk.Label(msg_frame, text="Destino:", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).grid(row=0, column=0, sticky="w", pady=2)
        self._msg_dest_var = tk.StringVar(value="broadcast")
        tk.Entry(msg_frame, textvariable=self._msg_dest_var,
                 bg="#3C3C3C", fg="#E0E0E0",
                 insertbackground="white",
                 font=self._font_mono, relief=tk.FLAT
                 ).grid(row=0, column=1, sticky="ew", padx=(4, 0), ipady=2)

        tk.Label(msg_frame, text="Mensaje:", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).grid(row=1, column=0, sticky="w", pady=2)
        self._msg_body_var = tk.StringVar()
        msg_entry = tk.Entry(msg_frame, textvariable=self._msg_body_var,
                             bg="#3C3C3C", fg="#E0E0E0",
                             insertbackground="white",
                             font=self._font_mono, relief=tk.FLAT)
        msg_entry.grid(row=1, column=1, sticky="ew", padx=(4, 0), ipady=2)
        msg_entry.bind("<Return>", lambda e: self._send_message())

        msg_frame.columnconfigure(1, weight=1)

        tk.Button(msg_frame, text="Enviar mensaje",
                  command=self._send_message,
                  bg="#7B2FBE", fg="white", activebackground="#8A3FCC",
                  font=self._font_ui, relief=tk.FLAT
                  ).grid(row=2, column=0, columnspan=2, sticky="ew",
                         pady=(6, 0), ipady=3)

        # ── Sección: Configuración LoRa ───────────────────────────────────
        self._section(p, "CONFIG LoRa")

        cfg_frame = tk.Frame(p, bg="#252526")
        cfg_frame.pack(fill=tk.X, padx=6, pady=(0, 6))

        # SF
        tk.Label(cfg_frame, text="SF:", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).grid(row=0, column=0, sticky="w", pady=2)
        self._sf_var = tk.StringVar(value="9")
        ttk.Combobox(cfg_frame, textvariable=self._sf_var,
                     values=[str(i) for i in range(7, 13)],
                     width=6, state="readonly", font=self._font_ui
                     ).grid(row=0, column=1, sticky="w", padx=(4, 0))

        # BW
        tk.Label(cfg_frame, text="BW:", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).grid(row=1, column=0, sticky="w", pady=2)
        self._bw_var = tk.StringVar(value="125")
        ttk.Combobox(cfg_frame, textvariable=self._bw_var,
                     values=["125", "250", "500"],
                     width=6, state="readonly", font=self._font_ui
                     ).grid(row=1, column=1, sticky="w", padx=(4, 0))

        # Frecuencia
        tk.Label(cfg_frame, text="Freq (MHz):", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).grid(row=2, column=0, sticky="w", pady=2)
        self._freq_var = tk.StringVar(value="915.0")
        tk.Entry(cfg_frame, textvariable=self._freq_var,
                 bg="#3C3C3C", fg="#E0E0E0",
                 insertbackground="white",
                 font=self._font_mono, relief=tk.FLAT, width=10
                 ).grid(row=2, column=1, sticky="w", padx=(4, 0), ipady=2)

        # Sync word
        tk.Label(cfg_frame, text="Sync word:", bg="#252526", fg="#CCCCCC",
                 font=self._font_ui).grid(row=3, column=0, sticky="w", pady=2)
        self._sync_var = tk.StringVar(value="0x12")
        tk.Entry(cfg_frame, textvariable=self._sync_var,
                 bg="#3C3C3C", fg="#E0E0E0",
                 insertbackground="white",
                 font=self._font_mono, relief=tk.FLAT, width=10
                 ).grid(row=3, column=1, sticky="w", padx=(4, 0), ipady=2)

        cfg_frame.columnconfigure(1, weight=1)

        btn_cfg_row = tk.Frame(p, bg="#252526")
        btn_cfg_row.pack(fill=tk.X, padx=6, pady=(0, 8))

        tk.Button(btn_cfg_row, text="Aplicar config",
                  command=self._apply_config,
                  bg="#C17F24", fg="white", activebackground="#D08F30",
                  font=self._font_ui, relief=tk.FLAT, padx=6, pady=3
                  ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        tk.Button(btn_cfg_row, text="Guardar en flash",
                  command=self._save_config,
                  bg="#5A7A5A", fg="white", activebackground="#6A8A6A",
                  font=self._font_ui, relief=tk.FLAT, padx=6, pady=3
                  ).pack(side=tk.LEFT, fill=tk.X, expand=True)

    # ── Barra de estado ──────────────────────────────────────────────────────

    def _build_status_bar(self):
        bar = tk.Frame(self, bg="#007ACC", height=24)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        bar.pack_propagate(False)

        # Indicador de estado (canvas circular)
        self._status_canvas = tk.Canvas(bar, width=16, height=16,
                                         bg="#007ACC", highlightthickness=0)
        self._status_canvas.pack(side=tk.LEFT, padx=(6, 2), pady=4)
        self._status_dot = self._status_canvas.create_oval(
            2, 2, 14, 14, fill="#E04E4E", outline="")

        self._status_port_lbl  = tk.Label(bar, text="Desconectado",
                                           bg="#007ACC", fg="white",
                                           font=self._font_ui)
        self._status_port_lbl.pack(side=tk.LEFT, padx=(2, 16))

        self._status_baud_lbl  = tk.Label(bar, text="",
                                           bg="#007ACC", fg="#BBDEFB",
                                           font=self._font_ui)
        self._status_baud_lbl.pack(side=tk.LEFT, padx=(0, 16))

        self._status_count_lbl = tk.Label(bar, text="Paquetes: 0",
                                           bg="#007ACC", fg="#BBDEFB",
                                           font=self._font_ui)
        self._status_count_lbl.pack(side=tk.LEFT)

        # Versión a la derecha
        tk.Label(bar, text=f"SMIC Console  v{APP_VERSION}",
                 bg="#007ACC", fg="#BBDEFB",
                 font=self._font_ui).pack(side=tk.RIGHT, padx=8)

    # ── Helpers de UI ────────────────────────────────────────────────────────

    def _section(self, parent, title: str):
        frm = tk.Frame(parent, bg="#3C3C3C")
        frm.pack(fill=tk.X, padx=0, pady=(8, 2))
        tk.Label(frm, text=f"  {title}",
                 bg="#3C3C3C", fg="#9CDCFE",
                 font=self._font_bold, anchor="w"
                 ).pack(fill=tk.X, ipady=2)

    def _configure_log_tags(self):
        for name, color in LOG_COLORS.items():
            self._log_text.tag_configure(name, foreground=color)
        self._log_text.tag_configure(
            "timestamp", foreground="#555566")

    # ════════════════════════════════════════════════════════════════════════
    # Escaneo de puertos
    # ════════════════════════════════════════════════════════════════════════

    def _scan_ports(self):
        ports = serial.tools.list_ports.comports()
        options = []
        for p in ports:
            vid = p.vid
            pid = p.pid
            if vid is not None and pid is not None:
                chip = KNOWN_DEVICES.get((vid, pid))
                if chip:
                    label = f"{p.device}  —  {chip}"
                    options.insert(0, label)  # prioridad al inicio
                    continue
            # Puerto desconocido pero existente
            desc = p.description or p.device
            options.append(f"{p.device}  —  {desc}")

        if not options:
            options = ["(sin puertos disponibles)"]

        self._port_cb["values"] = options
        self._port_cb.current(0)

        self._log(f"[SCAN] {len(ports)} puerto(s) encontrado(s)", "yellow")

    def _selected_port(self) -> str:
        """Extrae solo el nombre del puerto del ítem seleccionado."""
        val = self._port_var.get().strip()
        if "  —  " in val:
            return val.split("  —  ")[0].strip()
        return val.split()[0] if val else ""

    # ════════════════════════════════════════════════════════════════════════
    # Conexión / desconexión
    # ════════════════════════════════════════════════════════════════════════

    def _toggle_connect(self):
        if self._reader and self._reader.connected:
            self._disconnect()
        else:
            self._connect()

    def _connect(self):
        port = self._selected_port()
        if not port or port.startswith("("):
            messagebox.showwarning("Sin puerto",
                                   "Selecciona un puerto válido primero.")
            return
        try:
            baud = int(self._baud_var.get())
        except ValueError:
            baud = BAUD_DEFAULT

        self._log(f"[CONN] Conectando a {port} @ {baud} baud...", "yellow")

        self._reader = SerialReader(
            port, baud, self._rx_queue,
            status_cb=self._serial_status_cb,
        )
        self._reader.start()
        self._btn_connect.configure(text="Desconectar",
                                     bg="#8A1C1C")

    def _disconnect(self):
        if self._reader:
            self._reader.stop()
            self._reader = None
        self._btn_connect.configure(text="Conectar", bg="#0E7A0E")
        self._update_status_bar("disconnected", "", 0)
        self._log("[CONN] Desconectado.", "yellow")

    def _serial_status_cb(self, state: str, info: str, baud: int):
        """Llamado desde el hilo serial — encola evento para el hilo GUI."""
        self._rx_queue.put(("__STATUS__", state, info, baud))

    # ════════════════════════════════════════════════════════════════════════
    # Cola de recepción → GUI
    # ════════════════════════════════════════════════════════════════════════

    def _poll_queue(self):
        try:
            while True:
                item = self._rx_queue.get_nowait()
                if isinstance(item, tuple) and item[0] == "__STATUS__":
                    _, state, info, baud = item
                    self._handle_status(state, info, baud)
                else:
                    self._handle_line(item)
        except queue.Empty:
            pass
        self.after(50, self._poll_queue)

    def _handle_line(self, line: str):
        color = classify_line(line)
        self._log(line, color)
        self._packet_count += 1
        self._status_count_lbl.configure(
            text=f"Paquetes: {self._packet_count}")
        if self._log_file:
            try:
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._log_file.write(f"{ts}  {line}\n")
                self._log_file.flush()
            except Exception:
                pass

    def _handle_status(self, state: str, info: str, baud: int):
        if state == "connected":
            self._update_status_bar("connected", info, baud)
            self._log(f"[CONN] Conectado a {info} @ {baud} baud", "yellow")
        elif state == "reconnecting":
            self._update_status_bar("reconnecting", info, baud)
            self._log(f"[CONN] Reconectando a {info}...", "yellow")
        elif state == "error":
            self._update_status_bar("disconnected", "", 0)
            self._log(f"[CONN] Error: {info}", "red")

    # ════════════════════════════════════════════════════════════════════════
    # Log
    # ════════════════════════════════════════════════════════════════════════

    def _log(self, text: str, color: str = "gray"):
        self._log_text.configure(state=tk.NORMAL)
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self._log_text.insert(tk.END, f"[{ts}] ", "timestamp")
        self._log_text.insert(tk.END, text + "\n", color)
        self._log_text.configure(state=tk.DISABLED)
        self._log_text.see(tk.END)

    def _clear_log(self):
        self._log_text.configure(state=tk.NORMAL)
        self._log_text.delete("1.0", tk.END)
        self._log_text.configure(state=tk.DISABLED)
        self._packet_count = 0
        self._status_count_lbl.configure(text="Paquetes: 0")

    # ════════════════════════════════════════════════════════════════════════
    # Envío de comandos
    # ════════════════════════════════════════════════════════════════════════

    def _send_raw(self, cmd: str):
        if not self._reader or not self._reader.connected:
            self._log("[TX] No conectado.", "red")
            return
        self._reader.send(cmd)
        self._log(f"[TX] {cmd}", "white")

    def _send_command(self):
        cmd = self._cmd_var.get().strip()
        if cmd:
            self._send_raw(cmd)
            self._cmd_var.set("")

    def _send_message(self):
        dest = self._msg_dest_var.get().strip() or "broadcast"
        body = self._msg_body_var.get().strip()
        if not body:
            return
        cmd = f"send {dest} {body}"
        self._send_raw(cmd)
        self._msg_body_var.set("")

    def _apply_config(self):
        sf   = self._sf_var.get()
        bw   = self._bw_var.get()
        freq = self._freq_var.get().strip()
        sync = self._sync_var.get().strip()
        self._send_raw(f"config sf {sf}")
        self._send_raw(f"config bw {bw}")
        self._send_raw(f"config freq {freq}")
        self._send_raw(f"config sync {sync}")

    def _save_config(self):
        self._send_raw("saveconfig")

    # ════════════════════════════════════════════════════════════════════════
    # Barra de estado
    # ════════════════════════════════════════════════════════════════════════

    def _update_status_bar(self, state: str, port: str, baud: int):
        colors = {
            "connected":    ("#4EC94E", f"{port}  {baud} baud"),
            "reconnecting": ("#D4D44E", f"Reconectando {port}..."),
            "disconnected": ("#E04E4E", "Desconectado"),
        }
        dot_color, text = colors.get(state, ("#E04E4E", "Desconectado"))
        self._status_canvas.itemconfig(self._status_dot, fill=dot_color)
        self._status_port_lbl.configure(text=text)
        self._status_baud_lbl.configure(
            text=f"{baud} baud" if state == "connected" else "")

    # ════════════════════════════════════════════════════════════════════════
    # Log a archivo
    # ════════════════════════════════════════════════════════════════════════

    def _toggle_log_file(self):
        if self._save_log_var.get():
            path = filedialog.asksaveasfilename(
                title="Guardar log en archivo",
                defaultextension=".txt",
                filetypes=[("Texto", "*.txt"), ("Log", "*.log"),
                           ("Todos", "*.*")],
                initialfile=f"smic_log_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt",
            )
            if path:
                try:
                    self._log_file = open(path, "a", encoding="utf-8")
                    self._log_path = path
                    short = os.path.basename(path)
                    self._log_path_lbl.configure(text=f"→ {short}")
                    self._log(f"[LOG] Guardando en: {path}", "yellow")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
                    self._save_log_var.set(False)
            else:
                self._save_log_var.set(False)
        else:
            if self._log_file:
                try:
                    self._log_file.close()
                except Exception:
                    pass
                self._log_file = None
                self._log_path_lbl.configure(text="")
                self._log("[LOG] Log a archivo detenido.", "yellow")

    # ════════════════════════════════════════════════════════════════════════
    # Cierre
    # ════════════════════════════════════════════════════════════════════════

    def _on_close(self):
        self._disconnect()
        if self._log_file:
            try:
                self._log_file.close()
            except Exception:
                pass
        self.destroy()


# ---------------------------------------------------------------------------
# Estilos ttk
# ---------------------------------------------------------------------------

def _apply_dark_theme(root: tk.Tk):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground="#3C3C3C",
                    background="#3C3C3C",
                    foreground="#E0E0E0",
                    selectbackground="#264F78",
                    selectforeground="#E0E0E0",
                    arrowcolor="#E0E0E0")
    style.map("TCombobox",
              fieldbackground=[("readonly", "#3C3C3C")],
              foreground=[("readonly", "#E0E0E0")])
    style.configure("TScrollbar",
                    background="#3C3C3C",
                    troughcolor="#1E1E1E",
                    arrowcolor="#888888")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = SMICConsole()
    _apply_dark_theme(app)
    app.mainloop()
