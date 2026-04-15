# 12 — Troubleshooting y diagnóstico avanzado

> Cuando algo falla en producción, necesitas encontrar la causa raíz rápido. Este módulo reúne las herramientas más potentes para diagnóstico profundo del sistema.

---

## Metodología de diagnóstico

Antes de ejecutar comandos al azar, seguir este orden:

```
1. ¿Qué síntoma se observa exactamente?
2. ¿Cuándo empezó? ¿Hubo cambios previos?
3. Revisar logs (journalctl, /var/log/)
4. Ver estado del sistema (CPU, RAM, disco, red)
5. Identificar el componente afectado
6. Aislar la causa
7. Aplicar fix
8. Verificar que se resolvió
9. Documentar
```

---

## dmesg — Mensajes del kernel

```bash
dmesg                               # Todos los mensajes del kernel
dmesg | tail -50                    # Últimos 50 mensajes
dmesg -T                            # Con timestamps legibles
dmesg -T | tail -50
dmesg | grep -i "error\|fail\|warn"
dmesg | grep -i "oom\|killed"       # OOM killer
dmesg | grep -i "ata\|disk\|i/o"    # Errores de disco
dmesg | grep -i "eth\|network"      # Problemas de red
dmesg -w                            # Seguir en tiempo real
```

---

## lsof — Archivos y conexiones abiertas

```bash
lsof                                # Todos los archivos abiertos (enorme output)
lsof | wc -l                        # Cuántos descriptores hay abiertos
lsof -p PID                         # Archivos abiertos por un proceso
lsof -u usuario                     # Archivos de un usuario
lsof /var/log/syslog                # Qué proceso tiene este archivo abierto
lsof +D /directorio                 # Archivos abiertos en un directorio
lsof -i                             # Todas las conexiones de red
lsof -i :80                         # Qué usa el puerto 80
lsof -i tcp                         # Solo TCP
lsof -i @10.0.0.1                   # Conexiones a una IP específica

# Caso típico: "device is busy" al desmontar
lsof +D /mnt/punto_montaje          # Qué proceso está usando ese mount
```

---

## strace — Syscalls de un proceso

```bash
strace comando                      # Trazar syscalls de un comando
strace -p PID                       # Adjuntarse a proceso en ejecución
strace -e open,read,write comando   # Solo syscalls específicas
strace -o /tmp/trace.txt comando    # Guardar en archivo
strace -c comando                   # Resumen estadístico de syscalls
strace -f comando                   # Incluir procesos hijo (fork)
strace -T comando                   # Mostrar tiempo por syscall
```

---

## tcpdump — Captura de tráfico de red

```bash
tcpdump -i eth0                     # Capturar en interfaz eth0
tcpdump -i any                      # Todas las interfaces
tcpdump -i eth0 -n                  # Sin resolución de nombres
tcpdump -i eth0 port 80             # Solo tráfico en puerto 80
tcpdump -i eth0 host 10.0.0.5       # Solo tráfico de/hacia esa IP
tcpdump -i eth0 src 10.0.0.5        # Solo origen
tcpdump -i eth0 dst 10.0.0.5        # Solo destino
tcpdump -i eth0 -c 100              # Capturar solo 100 paquetes
tcpdump -i eth0 -w /tmp/captura.pcap    # Guardar para analizar con Wireshark
tcpdump -i eth0 'tcp port 443 and host 10.0.0.1'   # Filtro combinado
```

---

## netstat y ss — Conexiones de red

```bash
ss -tuln                            # Puertos escuchando
ss -tulnp                           # Puertos escuchando + proceso
ss -anp                             # Todas las conexiones
ss -s                               # Resumen estadístico
ss state established                # Solo conexiones establecidas
ss -t state time-wait               # Conexiones en TIME_WAIT
ss dst 10.0.0.5                     # Conexiones hacia esa IP
ss -tp | grep CLOSE_WAIT            # Conexiones CLOSE_WAIT (posible memory leak)
```

---

## perf — Profiling del sistema

```bash
perf top                            # Top de funciones que consumen CPU (tiempo real)
perf stat comando                   # Estadísticas de CPU para un comando
perf record -a -g sleep 10          # Grabar 10 segundos
perf report                         # Ver reporte del recording
perf stat -e cache-misses,instructions comando   # Métricas específicas
```

---

## Diagnóstico de disco e I/O

```bash
iostat -x 1                         # I/O por disco cada segundo
iostat -xd 1 sda                    # Solo disco sda
iotop                               # Procesos con más I/O (como top pero para disco)
iotop -o                            # Solo procesos con I/O activo
iotop -a                            # Acumulado en vez de instantáneo

# Latencia de disco
ioping /dev/sda                     # Latencia de acceso al disco
ioping -c 10 /dev/sda               # 10 muestras

# Velocidad de lectura/escritura
dd if=/dev/sda of=/dev/null bs=1M count=1000 status=progress   # Lectura secuencial
dd if=/dev/zero of=/tmp/test bs=1M count=1000 oflag=direct status=progress  # Escritura
```

---

## Diagnóstico de memoria

```bash
free -h                             # Resumen de RAM y swap
vmstat 1 10                         # Estadísticas cada segundo x10
cat /proc/meminfo                   # Info detallada
pmap PID                            # Mapa de memoria de un proceso
pmap -x PID | sort -n -k3 | tail -10  # Ordenado por uso de memoria
valgrind --leak-check=full ./programa   # Detectar memory leaks
```

---

## Diagnóstico de CPU

```bash
top -b -n 1                         # Snapshot de procesos (no interactivo)
mpstat -P ALL 1                     # CPU por núcleo
sar -u 1 10                         # Uso de CPU histórico
pidstat 1                           # Estadísticas por proceso
perf top                            # Profiling de funciones
```

---

## Diagnóstico de red avanzado

```bash
# Seguimiento de ruta con latencias
mtr --report dominio.com            # MTR en modo reporte
mtr --report-cycles 100 dominio.com # 100 ciclos para mayor precisión

# Diagnóstico de DNS
dig +trace dominio.com              # Trace completo de resolución DNS
nslookup -type=MX dominio.com       # Registros MX
dig dominio.com ANY                 # Todos los registros

# Ancho de banda
iperf3 -s                           # Servidor (en el destino)
iperf3 -c 10.0.0.5                  # Cliente: medir ancho de banda
iperf3 -c 10.0.0.5 -t 30 -P 4      # 30 segundos, 4 streams en paralelo

# Ver tráfico por proceso
nethogs eth0                        # Tráfico de red por proceso
iftop -i eth0                       # Tráfico en tiempo real por conexión
```

---

## Investigar crashes del kernel (kdump)

```bash
# Ver si hubo kernel panic
dmesg | grep -i "panic\|bug\|oops"
journalctl -k -b -1 | grep -i "panic\|oops"

# Historial de reinicios
last reboot
who -b
journalctl --list-boots
```

---

## /proc y /sys — El sistema de archivos virtual

```bash
cat /proc/version                   # Versión del kernel
cat /proc/uptime                    # Segundos encendido
cat /proc/loadavg                   # Load average
cat /proc/meminfo                   # Info de memoria
cat /proc/cpuinfo                   # Info de CPU
cat /proc/net/dev                   # Estadísticas de red
cat /proc/diskstats                 # Estadísticas de disco
cat /proc/PID/maps                  # Mapa de memoria del proceso
cat /proc/PID/net/tcp               # Conexiones TCP del proceso

# /sys para hardware
cat /sys/class/net/eth0/speed       # Velocidad del adaptador de red
cat /sys/class/block/sda/size       # Tamaño del disco en sectores
```

---

## Protocolo de respuesta a incidente

```bash
# 1. Capturar estado actual ANTES de tocar nada
ps aux > /tmp/incidente_ps.txt
netstat -tulnp > /tmp/incidente_net.txt
df -h > /tmp/incidente_df.txt
free -h > /tmp/incidente_mem.txt
journalctl -b > /tmp/incidente_logs.txt

# 2. Ver logs del período del incidente
journalctl --since "2 hours ago" --no-pager > /tmp/logs_incidente.txt

# 3. Ver cambios recientes
find /etc -newer /etc/passwd -type f 2>/dev/null   # Archivos config modificados
rpm -qa --last 2>/dev/null | head -20               # Últimos paquetes instalados (RHEL)
dpkg -l | grep "^ii" > /tmp/paquetes.txt            # Lista de paquetes instalados
```

---

## Troubleshooting por síntoma

| Síntoma | Dónde mirar |
|---|---|
| Servidor lento sin razón aparente | `htop`, `iostat -x 1`, `vmstat 1` |
| Proceso que no responde | `strace -p PID`, `lsof -p PID` |
| Puerto no abre | `ss -tulnp`, `ufw status`, `iptables -L` |
| Disco lleno de repente | `du -sh /* \| sort -rh`, `lsof \| grep deleted` |
| Memoria creciente (memory leak) | `pmap PID`, `valgrind` |
| Red lenta | `mtr destino`, `iperf3`, `tcpdump` |
| Proceso zombie | `ps aux \| grep Z` → matar el padre |
| Alta carga con poca CPU visible | `iostat -x 1` — probablemente I/O wait |
| DNS no resuelve | `dig @8.8.8.8 dominio.com`, `cat /etc/resolv.conf` |
| Conexión SSH cuelga | `ssh -v servidor` para debug verbose |
