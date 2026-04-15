# 01 — Inspección del sistema

> Antes de tocar cualquier cosa en un servidor, primero **mirá** qué hay. Estos comandos te dan el mapa completo del sistema.

---

## Sistema operativo y kernel

```bash
uname -a                    # Kernel, arquitectura, hostname, fecha de compilación
uname -r                    # Solo versión del kernel
cat /etc/os-release         # Distro, versión, ID
hostnamectl                 # Hostname, SO, kernel, arquitectura (systemd)
lsb_release -a              # Info detallada de la distro
```

---

## Hostname

```bash
hostname                    # Nombre actual del host
hostname -I                 # Todas las IPs del sistema
hostnamectl set-hostname nuevo-nombre   # Cambiar hostname (permanente)
```

---

## Tiempo y uptime

```bash
uptime                      # Tiempo encendido, carga promedio
uptime -p                   # Formato legible: "up 3 days, 4 hours"
w                           # Uptime + usuarios conectados + carga
date                        # Fecha y hora actual
timedatectl                 # Zona horaria, NTP, hora sincronizada
timedatectl list-timezones  # Listar zonas disponibles
timedatectl set-timezone America/Santiago   # Cambiar zona horaria
```

---

## CPU

```bash
lscpu                       # Arquitectura, núcleos, hilos, velocidad, caché
nproc                       # Número de procesadores disponibles
cat /proc/cpuinfo           # Info cruda de cada núcleo
lscpu | grep -E 'Model|CPU\(s\)|Thread|Core'   # Resumen rápido
```

---

## Memoria RAM

```bash
free -h                     # RAM y swap, formato legible
free -m                     # En megabytes
cat /proc/meminfo           # Info completa y cruda
vmstat -s                   # Estadísticas de memoria en formato tabla
```

---

## Hardware general

```bash
lshw -short                 # Resumen de todo el hardware
lshw -class network         # Solo hardware de red
lshw -class disk            # Solo discos
dmidecode -t system         # Info del fabricante, modelo, serial (requiere root)
dmidecode -t memory         # Slots de RAM, velocidad, tipo
dmidecode -t bios           # Versión del BIOS/UEFI
hwinfo --short              # Resumen de hardware (puede requerir instalación)
```

---

## Dispositivos y buses

```bash
lspci                       # Dispositivos PCI (GPU, controladores, etc.)
lspci -v                    # Con detalles
lsusb                       # Dispositivos USB conectados
lsblk                       # Discos, particiones y puntos de montaje en árbol
lsblk -f                    # Incluye filesystem y UUID
```

---

## Módulos del kernel

```bash
lsmod                       # Módulos del kernel cargados
modinfo nombre_modulo       # Información de un módulo específico
modprobe nombre_modulo      # Cargar un módulo
modprobe -r nombre_modulo   # Descargar un módulo
```

---

## Variables de entorno del sistema

```bash
env                         # Todas las variables de entorno
printenv PATH               # Variable específica
echo $HOME                  # Otra forma
```

---

## Casos de uso reales

**Antes de instalar software pesado**, verificar RAM y CPU disponibles:
```bash
free -h && lscpu | grep -E 'CPU\(s\)|Thread'
```

**Verificar si el servidor es físico o virtual:**
```bash
dmidecode -t system | grep -i product
systemd-detect-virt          # Devuelve: none, kvm, lxc, vmware, etc.
```

**Ver cuánto tiempo lleva encendido sin reinicios:**
```bash
who -b          # Último boot
last reboot     # Historial de reinicios
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| No sé qué distro es | `cat /etc/os-release` |
| Kernel extraño o viejo | `uname -r` |
| Hora desfasada | `timedatectl status` |
| No sé si es VM o físico | `systemd-detect-virt` |
| Necesito el serial del servidor | `dmidecode -t system` |
