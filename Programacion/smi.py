#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         SMIC — Sistema de Monitoreo de Infraestructuras      ║
║                  Consola Serial Profesional v2.0             ║
║                      Nodo LoRa Mesh                          ║
╚══════════════════════════════════════════════════════════════╝

Uso:
    python3 smic_console_v2.py
    python3 smic_console_v2.py --port /dev/ttyUSB0
    python3 smic_console_v2.py --port COM3          (Windows)
    python3 smic_console_v2.py --log

Instalación:
    pip install pyserial
    pip3 install pyserial --break-system-packages   (Linux)
"""

import serial
import serial.tools.list_ports
import threading
import sys
import os
import time
import argparse
import glob
import logging
import re
from datetime import datetime


# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════

VERSION   = "2.0.0"
BAUD_RATE = 115200
LOG_DIR   = os.path.expanduser("~/smic_logs")

# VID/PID conocidos
KNOWN_DEVICES = {
    (0x10C4, 0xEA60): "Heltec V3 (CP2102)",
    (0x303A, 0x1001): "XIAO ESP32-S3",
    (0x1A86, 0x7523): "CH340 (genérico)",
    (0x0403, 0x6001): "FTDI (genérico)",
}


# ══════════════════════════════════════════════════════════════
# COLORES ANSI
# ══════════════════════════════════════════════════════════════

class C:
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'

    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    GRAY    = '\033[90m'

    BG_RED  = '\033[41m'


# ══════════════════════════════════════════════════════════════
# LOGGER
# ══════════════════════════════════════════════════════════════

class SMICLogger:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.logger  = None
        if enabled:
            os.makedirs(LOG_DIR, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(LOG_DIR, f"smic_{ts}.log")
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(asctime)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            self.logger = logging.getLogger("SMIC")
            print(f"{C.GRAY}  Log: {log_file}{C.RESET}")

    def log(self, message):
        if self.enabled and self.logger:
            clean = re.sub(r'\033\[[0-9;]*m', '', message)
            self.logger.info(clean)


# ══════════════════════════════════════════════════════════════
# ESTADÍSTICAS EN TIEMPO REAL
# ══════════════════════════════════════════════════════════════

class NodeStats:
    def __init__(self):
        self.node_id   = "—"
        self.node_name = "—"
        self.board     = "—"
        self.freq      = "—"
        self.neighbors = 0
        self.tx        = 0
        self.rx        = 0
        self.fwd       = 0
        self.rssi      = 0
        self.snr       = 0.0
        self.uptime    = 0
        self.heap      = 0

    def parse_line(self, line):
        m = re.search(r'\[Stats\] Vecinos:(\d+) Tx:(\d+) Rx:(\d+) Fwd:(\d+) Heap:(\d+)', line)
        if m:
            self.neighbors = int(m.group(1))
            self.tx        = int(m.group(2))
            self.rx        = int(m.group(3))
            self.fwd       = int(m.group(4))
            self.heap      = int(m.group(5))

        m = re.search(r'RSSI=(-?\d+)', line)
        if m: self.rssi = int(m.group(1))

        m = re.search(r'SNR=([\d.]+)', line)
        if m: self.snr = float(m.group(1))

        m = re.search(r'ID: (0x[0-9A-Fa-f]+)', line)
        if m: self.node_id = m.group(1)

        m = re.search(r'Nombre: (.+)', line)
        if m: self.node_name = m.group(1).strip()

        m = re.search(r'Placa: (.+)', line)
        if m: self.board = m.group(1).strip()

        m = re.search(r'Freq: (.+)', line)
        if m: self.freq = m.group(1).strip()

        m = re.search(r'Uptime: (\d+)', line)
        if m: self.uptime = int(m.group(1))


# ══════════════════════════════════════════════════════════════
# FORMATEADOR DE OUTPUT
# ══════════════════════════════════════════════════════════════

class LineFormatter:
    @staticmethod
    def format(line):
        line = line.strip()
        if not line:
            return None

        ts = f"{C.GRAY}{datetime.now().strftime('%H:%M:%S')}{C.RESET} "

        if 'ERROR' in line:
            return f"{ts}{C.BG_RED}{C.WHITE}{C.BOLD} ERROR {C.RESET} {C.RED}{line}{C.RESET}"

        if 'WARN' in line or 'fallo' in line.lower():
            return f"{ts}{C.YELLOW}⚠  {line}{C.RESET}"

        if '>>> MENSAJE' in line:
            return f"\n{ts}{C.MAGENTA}{C.BOLD}{'─'*50}\n  {line}{C.RESET}\n"

        if 'Nuevo vecino' in line:
            return f"{ts}{C.GREEN}{C.BOLD}◉  {line}{C.RESET}"

        if 'BEACON de' in line and 'Handler' in line:
            return f"{ts}{C.CYAN}📡 {line}{C.RESET}"

        if 'Nueva ruta' in line:
            return f"{ts}{C.BLUE}→  {line}{C.RESET}"

        if 'Ruta expirada' in line or 'Vecino timeout' in line:
            return f"{ts}{C.YELLOW}✗  {line}{C.RESET}"

        if 'Paquete enviado OK' in line:
            return f"{ts}{C.GREEN}↑  {line}{C.RESET}"

        if 'Recibido' in line and '[LoRa]' in line:
            return f"{ts}{C.CYAN}↓  {line}{C.RESET}"

        if 'Paquete duplicado' in line:
            return f"{ts}{C.GRAY}⊘  {line}{C.RESET}"

        if 'invalido' in line.lower() or 'inválido' in line:
            return f"{ts}{C.YELLOW}⊗  {line}{C.RESET}"

        if '[Stats]' in line:
            return f"{ts}{C.GRAY}◌  {line}{C.RESET}"

        if '[Setup]' in line or 'LORA MESH NETWORK' in line:
            return f"{ts}{C.BLUE}{line}{C.RESET}"

        if '===' in line or '───' in line or '=====' in line:
            return f"{ts}{C.BLUE}{line}{C.RESET}"

        if '[LoRa]' in line:
            return f"{ts}{C.CYAN}{line}{C.RESET}"

        if '[Display]' in line or '[Routing]' in line or '[Handler]' in line:
            return f"{ts}{C.GRAY}{line}{C.RESET}"

        if '[CMD]' in line:
            return f"{ts}{C.YELLOW}›  {line}{C.RESET}"

        if line.startswith('#') and ('RSSI' in line or 'Dest' in line):
            return f"{ts}{C.WHITE}{C.BOLD}  {line}{C.RESET}"

        if '(sin vecinos)' in line or '(sin rutas)' in line:
            return f"{ts}{C.GRAY}  {line}{C.RESET}"

        if any(line.startswith(k) for k in ['ID:', 'Nombre:', 'Placa:', 'FW:', 'Freq:', 'Uptime:']):
            parts = line.split(':', 1)
            if len(parts) == 2:
                return f"{ts}  {C.GRAY}{parts[0]}:{C.RESET}{C.WHITE}{parts[1]}{C.RESET}"

        return f"{ts}{line}"


# ══════════════════════════════════════════════════════════════
# DETECCIÓN DE PUERTO
# ══════════════════════════════════════════════════════════════

def list_ports():
    """Lista todos los puertos disponibles con descripción."""
    ports = list(serial.tools.list_ports.comports())
    result = []
    for p in ports:
        vid_pid = (p.vid, p.pid) if p.vid and p.pid else None
        name = KNOWN_DEVICES.get(vid_pid, p.description or "Puerto desconocido")
        star = "★ " if vid_pid in KNOWN_DEVICES else "  "
        result.append((p.device, name, star, vid_pid in KNOWN_DEVICES))
    return result

def find_port():
    """Detecta automáticamente el puerto SMIC por VID/PID o nombre."""
    # Linux — buscar por nombre
    candidates = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    if candidates:
        return sorted(candidates)[0]

    # Windows/Mac — buscar por VID/PID conocido
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if (p.vid, p.pid) in KNOWN_DEVICES:
            return p.device

    # Fallback — primer puerto disponible
    if ports:
        return ports[0].device

    return None

def select_port_interactive():
    """Muestra lista de puertos y deja elegir al usuario."""
    ports = list_ports()
    if not ports:
        return None

    print(f"\n{C.BLUE}{'═'*50}{C.RESET}")
    print(f"  {C.BOLD}Puertos disponibles:{C.RESET}")
    print(f"{C.BLUE}{'─'*50}{C.RESET}")

    for i, (device, name, star, known) in enumerate(ports):
        color = C.GREEN if known else C.WHITE
        print(f"  {C.GRAY}[{i+1}]{C.RESET} {star}{color}{device}{C.RESET}  {C.GRAY}{name}{C.RESET}")

    print(f"{C.BLUE}{'─'*50}{C.RESET}")

    while True:
        try:
            sys.stdout.write(f"  Selecciona [1-{len(ports)}] o Enter para auto-detectar: ")
            sys.stdout.flush()
            choice = input().strip()

            if choice == '':
                auto = find_port()
                if auto:
                    print(f"  {C.CYAN}Auto-detectado: {auto}{C.RESET}")
                    return auto
                print(f"  {C.RED}No se detectó ninguna placa SMIC.{C.RESET}")
                return None

            idx = int(choice) - 1
            if 0 <= idx < len(ports):
                return ports[idx][0]
            print(f"  {C.RED}Opción inválida.{C.RESET}")
        except (ValueError, EOFError):
            return None


# ══════════════════════════════════════════════════════════════
# BANNER Y AYUDA
# ══════════════════════════════════════════════════════════════

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner(port, baud, log_enabled):
    print(f"\n{C.BLUE}{'═'*62}{C.RESET}")
    print(f"{C.BLUE}║{C.RESET}  {C.BOLD}{C.WHITE}SMIC — Consola Serial v{VERSION}{C.RESET}")
    print(f"{C.BLUE}║{C.RESET}  {C.GRAY}Sistema de Monitoreo de Infraestructuras Críticas{C.RESET}")
    print(f"{C.BLUE}{'═'*62}{C.RESET}")
    print(f"  {C.GRAY}Puerto :{C.RESET} {C.GREEN}{port}{C.RESET}")
    print(f"  {C.GRAY}Baud   :{C.RESET} {C.GREEN}{baud}{C.RESET}")
    print(f"  {C.GRAY}Log    :{C.RESET} {C.GREEN}{'Activo → ' + LOG_DIR if log_enabled else 'Desactivado'}{C.RESET}")
    print(f"  {C.GRAY}Ayuda  :{C.RESET} {C.YELLOW}.help{C.RESET}   {C.GRAY}Salir:{C.RESET} {C.YELLOW}.quit{C.RESET} o {C.YELLOW}Ctrl+C{C.RESET}")
    print(f"{C.BLUE}{'─'*62}{C.RESET}\n")

def show_status(stats):
    rssi_color = C.GREEN if stats.rssi > -80 else C.YELLOW if stats.rssi > -100 else C.RED
    uptime_str = f"{stats.uptime//3600}h {(stats.uptime%3600)//60}m" if stats.uptime > 0 else "—"
    heap_kb    = f"{stats.heap // 1024} KB" if stats.heap > 0 else "—"

    print(f"\n{C.BLUE}{'─'*62}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}Nodo   {C.RESET} {stats.node_name} {C.GRAY}({stats.node_id}){C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}Placa  {C.RESET} {stats.board}  {C.GRAY}|{C.RESET}  Freq: {stats.freq}")
    print(f"  {C.BOLD}{C.WHITE}Red    {C.RESET} Vecinos: {C.CYAN}{C.BOLD}{stats.neighbors}{C.RESET}  "
          f"Tx: {C.GREEN}{stats.tx}{C.RESET}  Rx: {C.CYAN}{stats.rx}{C.RESET}  Fwd: {C.GRAY}{stats.fwd}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}Radio  {C.RESET} RSSI: {rssi_color}{stats.rssi} dBm{C.RESET}  SNR: {stats.snr} dB")
    print(f"  {C.BOLD}{C.WHITE}Sistema{C.RESET} Uptime: {uptime_str}  Heap libre: {heap_kb}")
    print(f"{C.BLUE}{'─'*62}{C.RESET}\n")

def show_help():
    print(f"\n{C.BLUE}{'═'*62}{C.RESET}")
    print(f"  {C.BOLD}Comandos del nodo{C.RESET}")
    print(f"{C.BLUE}{'─'*62}{C.RESET}")
    for cmd, desc in [
        ("help",             "Lista de comandos del nodo"),
        ("info",             "ID, nombre, placa, frecuencia, uptime"),
        ("neighbors",        "Tabla de vecinos detectados"),
        ("routes",           "Tabla de rutas activas"),
        ("stats",            "Estadísticas de paquetes"),
        ("beacon",           "Forzar envío de beacon"),
        ("broadcast <msg>",  "Mensaje a todos los nodos"),
        ("msg <id> <msg>",   "Mensaje a nodo específico"),
        ("screen",           "Rotar pantalla OLED (Heltec V3)"),
        ("config show",      "Ver configuración LoRa actual"),
        ("config freq <mhz>","Cambiar frecuencia"),
        ("config sf <7-12>", "Cambiar Spreading Factor"),
        ("config save",      "Guardar config en flash"),
    ]:
        print(f"  {C.GREEN}{cmd:<22}{C.RESET} {desc}")

    print(f"\n  {C.BOLD}Comandos locales{C.RESET}")
    print(f"{C.BLUE}{'─'*62}{C.RESET}")
    for cmd, desc in [
        (".help",    "Mostrar esta ayuda"),
        (".status",  "Estadísticas en tiempo real del nodo"),
        (".ports",   "Listar puertos disponibles"),
        (".clear",   "Limpiar pantalla"),
        (".port",    "Mostrar puerto activo"),
        (".quit",    "Salir de la consola"),
    ]:
        print(f"  {C.YELLOW}{cmd:<22}{C.RESET} {desc}")
    print(f"{C.BLUE}{'═'*62}{C.RESET}\n")


# ══════════════════════════════════════════════════════════════
# HILO DE LECTURA SERIAL
# ══════════════════════════════════════════════════════════════

running   = True
formatter = LineFormatter()

def read_serial(ser, stats, logger):
    global running
    buffer = ""

    while running:
        try:
            if ser.in_waiting > 0:
                data   = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
                buffer += data

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    stats.parse_line(line)
                    formatted = formatter.format(line)

                    if formatted is not None:
                        sys.stdout.write('\r\033[K')
                        print(formatted)
                        logger.log(line)
                        sys.stdout.write(f"{C.GREEN}smic{C.RESET}{C.GRAY}›{C.RESET} ")
                        sys.stdout.flush()
            else:
                time.sleep(0.02)

        except serial.SerialException as e:
            if running:
                print(f"\n{C.RED}[ERROR] Conexión perdida: {e}{C.RESET}")
                running = False
            break
        except Exception as e:
            if running:
                print(f"\n{C.RED}[ERROR] {e}{C.RESET}")


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    global running

    parser = argparse.ArgumentParser(description='SMIC — Consola Serial Profesional')
    parser.add_argument('--port', '-p', default=None,               help='Puerto serial (ej: /dev/ttyUSB0 o COM3)')
    parser.add_argument('--baud', '-b', type=int, default=BAUD_RATE, help='Baud rate (default: 115200)')
    parser.add_argument('--log',  '-l', action='store_true',        help='Guardar log en archivo')
    parser.add_argument('--list', action='store_true',              help='Listar puertos y salir')
    args = parser.parse_args()

    # Solo listar puertos
    if args.list:
        ports = list_ports()
        if not ports:
            print("No se encontraron puertos.")
        else:
            for device, name, star, known in ports:
                print(f"{star}{device}  —  {name}")
        return

    clear_screen()

    # Seleccionar puerto
    port = args.port
    if port is None:
        # Intentar auto-detectar primero
        auto = find_port()
        if auto:
            port = auto
            print(f"\n{C.CYAN}[Auto] Puerto detectado: {port}{C.RESET}")
        else:
            # Mostrar lista interactiva
            port = select_port_interactive()
            if port is None:
                print(f"{C.RED}[ERROR] No se encontró ningún puerto.{C.RESET}")
                print(f"        Conecta la placa y vuelve a intentar.")
                print(f"        O especifica: python smic_console_v2.py --port COM3")
                sys.exit(1)

    # Logger
    logger = SMICLogger(enabled=args.log)

    # Conectar
    try:
        ser = serial.Serial(port, args.baud, timeout=0.1)
        time.sleep(0.5)
        ser.reset_input_buffer()
    except serial.SerialException as e:
        print(f"{C.RED}[ERROR] No se pudo abrir {port}: {e}{C.RESET}")
        if os.name == 'posix':
            print(f"        Verifica permisos: sudo usermod -a -G dialout $USER")
        else:
            print(f"        Verifica que el driver CP210x está instalado.")
            print(f"        Descarga: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers")
        sys.exit(1)
    except PermissionError:
        print(f"{C.RED}[ERROR] Sin permisos para {port}.{C.RESET}")
        print(f"        Ejecuta: sudo usermod -a -G dialout $USER")
        sys.exit(1)

    clear_screen()
    show_banner(port, args.baud, args.log)

    stats  = NodeStats()
    thread = threading.Thread(target=read_serial, args=(ser, stats, logger), daemon=True)
    thread.start()

    try:
        while running:
            try:
                sys.stdout.write(f"{C.GREEN}smic{C.RESET}{C.GRAY}›{C.RESET} ")
                sys.stdout.flush()
                cmd = input().strip()
            except EOFError:
                break

            if not cmd:
                continue

            # Comandos locales
            if cmd in ('.quit', '.exit', '.q'):
                break
            elif cmd in ('.help', '.h', '?'):
                show_help()
                continue
            elif cmd == '.status':
                show_status(stats)
                continue
            elif cmd == '.ports':
                ports = list_ports()
                print(f"\n{C.BLUE}{'─'*50}{C.RESET}")
                for device, name, star, known in ports:
                    color = C.GREEN if known else C.WHITE
                    print(f"  {star}{color}{device}{C.RESET}  {C.GRAY}{name}{C.RESET}")
                print(f"{C.BLUE}{'─'*50}{C.RESET}\n")
                continue
            elif cmd == '.clear':
                clear_screen()
                show_banner(port, args.baud, args.log)
                continue
            elif cmd == '.port':
                print(f"  Puerto: {C.GREEN}{port}{C.RESET}  Baud: {C.GREEN}{args.baud}{C.RESET}")
                continue

            # Enviar al nodo
            try:
                ser.write((cmd + '\n').encode('utf-8'))
                logger.log(f"CMD > {cmd}")
            except serial.SerialException as e:
                print(f"{C.RED}[ERROR] Fallo al enviar: {e}{C.RESET}")
                running = False
                break

    except KeyboardInterrupt:
        pass

    finally:
        running = False
        time.sleep(0.3)
        try:
            ser.close()
        except Exception:
            pass

        print(f"\n{C.BLUE}{'─'*62}{C.RESET}")
        print(f"  {C.BOLD}Sesión SMIC finalizada{C.RESET}")
        if stats.tx > 0 or stats.rx > 0:
            print(f"  Tx: {C.GREEN}{stats.tx}{C.RESET}  "
                  f"Rx: {C.CYAN}{stats.rx}{C.RESET}  "
                  f"Vecinos: {C.CYAN}{stats.neighbors}{C.RESET}")
        print(f"{C.BLUE}{'─'*62}{C.RESET}\n")


if __name__ == '__main__':
    main()
