# Administración de Servidores Linux — Guía de Referencia

Guía completa de comandos y procedimientos para administración de sistemas Linux. Organizada de lo más básico a lo más avanzado, con ejemplos reales y tablas de troubleshooting.

---

## Módulos

| # | Módulo | Descripción |
|---|---|---|
| 01 | [Inspección del sistema](./01-inspeccion-sistema.md) | uname, lscpu, dmidecode, hardware |
| 02 | [Red y conectividad](./02-red-conectividad.md) | ip, ss, nmap, firewall, DNS |
| 03 | [Procesos y rendimiento](./03-procesos-rendimiento.md) | top, ps, kill, vmstat, load average |
| 04 | [Almacenamiento y filesystems](./04-almacenamiento-filesystems.md) | df, fdisk, LVM, SMART, fstab |
| 05 | [Usuarios, grupos y permisos](./05-usuarios-grupos-permisos.md) | useradd, chmod, sudo, ACL |
| 06 | [Servicios y systemd](./06-servicios-systemd.md) | systemctl, journalctl, cron, timers |
| 07 | [Logs y auditoría](./07-logs-auditoria.md) | journalctl, grep, awk, auditd, logrotate |
| 08 | [Seguridad del servidor](./08-seguridad-servidor.md) | SSH hardening, fail2ban, ufw, SSL |
| 09 | [Backups y recuperación](./09-backups-recuperacion.md) | rsync, tar, borg, LVM snapshots |
| 10 | [Scripting y automatización](./10-scripting-automatizacion.md) | Bash, variables, loops, funciones |
| 11 | [Virtualización y contenedores](./11-virtualizacion-contenedores.md) | Proxmox, Docker, LXC, virsh |
| 12 | [Troubleshooting y diagnóstico](./12-troubleshooting-diagnostico.md) | strace, tcpdump, lsof, perf |

---

## Referencia rápida — Comandos más usados

```bash
# Sistema
uname -a && uptime && free -h && df -h

# Red
ip -br addr && ss -tulnp

# Procesos
ps aux --sort=-%cpu | head -10

# Servicios
systemctl status servicio
journalctl -u servicio -f

# Logs de errores del boot actual
journalctl -p err -b --no-pager

# Ver qué usa un puerto
ss -tulnp | grep :PUERTO

# Ver qué proceso usa un archivo
lsof /ruta/al/archivo
```

---

## Convenciones usadas en esta guía

- Los comandos que requieren root están marcados implícitamente (la mayoría de diagnóstico y configuración)
- `VMID` y `CTID` son los IDs numéricos de VMs y contenedores en Proxmox
- `PID` es el ID de proceso, obtenible con `ps aux` o `pgrep nombre`
- Los ejemplos usan la red `10.0.0.0/24` como red interna de referencia

---

## Entorno de referencia

- **Hipervisor:** Proxmox VE
- **SO base:** Debian 12 / Ubuntu 22.04 LTS
- **Arquitectura:** x86_64
