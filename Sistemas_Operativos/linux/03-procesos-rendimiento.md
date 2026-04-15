# 03 — Procesos y rendimiento

> Saber leer el estado de los procesos y el rendimiento del sistema es fundamental para detectar cuellos de botella, procesos zombis, fugas de memoria y problemas de CPU antes de que exploten.

---

## Ver procesos en tiempo real

```bash
top                         # Monitor clásico, actualización cada 3s
htop                        # Versión mejorada con colores e interfaz interactiva
btop                        # Monitor moderno y visual (instalar: apt install btop)
atop                        # Histórico de procesos, incluye disco y red
```

### Atajos útiles dentro de `top`/`htop`
| Tecla | Acción |
|---|---|
| `P` | Ordenar por CPU |
| `M` | Ordenar por memoria |
| `k` | Matar proceso (pide PID) |
| `q` | Salir |
| `1` | Ver CPUs individuales (en top) |
| `F5` | Vista árbol (en htop) |

---

## Listar procesos con `ps`

```bash
ps aux                      # Todos los procesos, todos los usuarios
ps aux | grep nginx         # Filtrar por nombre
ps -ef                      # Formato alternativo con PPID
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu   # Ordenado por CPU
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%mem   # Ordenado por memoria
pstree                      # Ver árbol de procesos
pstree -p                   # Con PIDs
```

---

## Información de un proceso específico

```bash
cat /proc/PID/status        # Estado detallado del proceso
cat /proc/PID/cmdline       # Comando completo con argumentos
ls -la /proc/PID/fd         # Archivos abiertos por el proceso
lsof -p PID                 # Archivos, sockets y conexiones del proceso
strace -p PID               # Syscalls en tiempo real (diagnóstico profundo)
```

---

## Señales y control de procesos

```bash
kill PID                    # Enviar SIGTERM (cierre graceful)
kill -9 PID                 # SIGKILL (fuerza bruta, sin limpieza)
kill -l                     # Listar todas las señales
killall nginx               # Matar todos los procesos con ese nombre
pkill -f "python script.py" # Matar por patrón en el comando
```

### Señales más usadas
| Señal | Número | Uso |
|---|---|---|
| SIGTERM | 15 | Cierre normal (default de kill) |
| SIGKILL | 9 | Cierre forzado, no se puede ignorar |
| SIGHUP | 1 | Recargar configuración |
| SIGSTOP | 19 | Pausar proceso |
| SIGCONT | 18 | Continuar proceso pausado |

---

## Prioridad de procesos

```bash
nice -n 10 comando          # Iniciar proceso con prioridad baja (nice: -20 a 19)
nice -n -5 comando          # Prioridad más alta (requiere root para valores negativos)
renice 10 -p PID            # Cambiar prioridad de proceso en ejecución
renice -5 -p PID            # Aumentar prioridad (root)
```

---

## Carga del sistema (load average)

```bash
uptime                      # Muestra load average: 1min, 5min, 15min
cat /proc/loadavg           # Idem, crudo
```

> **Referencia:** un load average igual al número de CPUs = 100% de uso. Si tienes 4 CPUs y el load es 4.0, el servidor está al límite. Si es 8.0, está saturado.

---

## Rendimiento de CPU

```bash
vmstat 1 5                  # Estadísticas cada 1 segundo, 5 veces
mpstat -P ALL 1             # CPU por núcleo (instalar: sysstat)
sar -u 1 5                  # Uso de CPU histórico y en tiempo real
iostat -x 1                 # CPU + estadísticas de I/O de disco
perf top                    # Profiling de CPU en tiempo real (requiere root)
```

---

## Rendimiento de memoria

```bash
free -h                     # RAM libre/usada/cache
vmstat -s                   # Estadísticas completas de memoria
cat /proc/meminfo           # Detalle completo
slabtop                     # Uso del slab allocator del kernel
```

---

## Procesos en background

```bash
comando &                   # Ejecutar en background
jobs                        # Ver procesos en background de la sesión
fg %1                       # Traer job 1 al foreground
bg %1                       # Enviar job pausado al background
nohup comando &             # Continúa aunque cierres la terminal
disown %1                   # Desvincula el proceso de la sesión
screen / tmux               # Sesiones persistentes (recomendado para tareas largas)
```

---

## OOM Killer (Out Of Memory)

Cuando el sistema se queda sin RAM, el kernel mata procesos automáticamente.

```bash
dmesg | grep -i "oom\|killed process"      # Ver si el OOM killer actuó
journalctl -k | grep -i "oom"              # Idem desde journalctl
cat /proc/PID/oom_score                    # Puntuación OOM de un proceso (mayor = más riesgo)
echo -17 > /proc/PID/oom_adj               # Proteger proceso del OOM killer (root)
```

---

## Casos de uso reales

**Encontrar qué proceso consume más CPU:**
```bash
ps aux --sort=-%cpu | head -10
```

**Encontrar qué proceso consume más RAM:**
```bash
ps aux --sort=-%mem | head -10
```

**Ver si el sistema estuvo bajo presión de memoria:**
```bash
journalctl -b -1 | grep -i "oom\|killed"
```

**Matar todos los procesos de un usuario:**
```bash
pkill -u usuario
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| Servidor lento, no sé por qué | `htop` ordenado por CPU y memoria |
| Proceso zombi | `ps aux \| grep Z` → matar el proceso padre |
| Sistema se cuelga periódicamente | `dmesg \| grep -i oom` |
| Proceso no muere con kill | `kill -9 PID` |
| Load average muy alto | `vmstat 1` para ver si es CPU, I/O o procesos |
