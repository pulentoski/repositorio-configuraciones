# 06 — Servicios y systemd

> systemd es el gestor de servicios de prácticamente todas las distros modernas. Dominarlo te permite controlar qué corre en tu servidor, cuándo y cómo se recupera ante fallos.

---

## Gestión básica de servicios

```bash
systemctl start nginx           # Iniciar servicio
systemctl stop nginx            # Detener servicio
systemctl restart nginx         # Reiniciar (stop + start)
systemctl reload nginx          # Recargar configuración sin reiniciar (si lo soporta)
systemctl status nginx          # Ver estado, últimas líneas de log, PID

systemctl enable nginx          # Habilitar al inicio del sistema
systemctl disable nginx         # Deshabilitar al inicio
systemctl enable --now nginx    # Habilitar y arrancar inmediatamente
systemctl disable --now nginx   # Deshabilitar y detener inmediatamente

systemctl is-active nginx       # ¿Está corriendo? (active/inactive)
systemctl is-enabled nginx      # ¿Arranca en el boot? (enabled/disabled)
systemctl is-failed nginx       # ¿Falló? (failed/active)
```

---

## Ver servicios del sistema

```bash
systemctl list-units --type=service             # Todos los servicios activos
systemctl list-units --type=service --all       # Incluye inactivos y fallidos
systemctl list-units --state=failed             # Solo los que fallaron
systemctl list-unit-files --type=service        # Todos los servicios con su estado de boot
```

---

## Journalctl — Logs del sistema

```bash
journalctl                          # Todos los logs (paginado)
journalctl -f                       # Seguir logs en tiempo real (como tail -f)
journalctl -n 50                    # Últimas 50 líneas
journalctl -u nginx                 # Logs de un servicio específico
journalctl -u nginx -f              # Seguir logs de nginx en tiempo real
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx --since "2024-01-01" --until "2024-01-02"
journalctl -b                       # Logs del boot actual
journalctl -b -1                    # Logs del boot anterior
journalctl --list-boots             # Lista de todos los boots
journalctl -p err                   # Solo errores
journalctl -p err -b                # Errores del boot actual
journalctl -k                       # Solo mensajes del kernel (dmesg)
journalctl --disk-usage             # Espacio usado por los logs
journalctl --vacuum-size=500M       # Reducir logs a 500MB
journalctl --vacuum-time=30d        # Eliminar logs de más de 30 días
```

---

## Unidades systemd (unit files)

Los archivos de configuración de servicios están en:
- `/lib/systemd/system/` — instalados por paquetes (no editar)
- `/etc/systemd/system/` — personalizaciones y servicios propios

```bash
systemctl cat nginx                 # Ver el unit file de un servicio
systemctl edit nginx                # Editar/sobreescribir sin tocar el original
systemctl daemon-reload             # Recargar configuración después de cambios
```

### Estructura de un unit file básico

```ini
[Unit]
Description=Mi aplicación web
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/miapp
ExecStart=/opt/miapp/start.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# Crear servicio personalizado
nano /etc/systemd/system/miapp.service
systemctl daemon-reload
systemctl enable --now miapp
```

---

## Targets (niveles de ejecución)

Los targets son el equivalente moderno a los runlevels.

```bash
systemctl get-default               # Ver target actual
systemctl set-default multi-user.target   # Sin interfaz gráfica (servidores)
systemctl set-default graphical.target    # Con interfaz gráfica
systemctl isolate rescue.target     # Modo rescate (root solo)

# Equivalencias con runlevels
# poweroff.target  = nivel 0
# rescue.target    = nivel 1
# multi-user.target = nivel 3
# graphical.target = nivel 5
# reboot.target    = nivel 6
```

---

## Cron — tareas programadas

```bash
crontab -e                  # Editar crontab del usuario actual
crontab -l                  # Ver crontab actual
crontab -r                  # Eliminar crontab
crontab -u usuario -e       # Editar crontab de otro usuario (root)
cat /etc/crontab            # Crontab del sistema
ls /etc/cron.d/             # Crontabs adicionales del sistema
ls /etc/cron.daily/         # Scripts que corren diariamente
```

### Sintaxis de cron

```
┌───────── minuto (0-59)
│ ┌───────── hora (0-23)
│ │ ┌───────── día del mes (1-31)
│ │ │ ┌───────── mes (1-12)
│ │ │ │ ┌───────── día de la semana (0-7, 0 y 7 = domingo)
│ │ │ │ │
* * * * * comando

# Ejemplos
0 2 * * *   /scripts/backup.sh           # Todos los días a las 2:00 AM
*/5 * * * * /scripts/monitoreo.sh        # Cada 5 minutos
0 0 * * 0   /scripts/limpieza_semanal.sh # Domingos a medianoche
0 */6 * * * /scripts/sync.sh            # Cada 6 horas
```

---

## Systemd timers (alternativa moderna a cron)

```bash
systemctl list-timers               # Ver todos los timers activos
systemctl list-timers --all         # Incluye inactivos
```

### Ejemplo de timer

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Backup diario

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Script de backup

[Service]
Type=oneshot
ExecStart=/scripts/backup.sh
```

```bash
systemctl enable --now backup.timer
```

---

## Apagado y reinicio

```bash
systemctl reboot            # Reiniciar
systemctl poweroff          # Apagar
systemctl suspend           # Suspender
shutdown -h now             # Apagar ahora
shutdown -r now             # Reiniciar ahora
shutdown -h +10             # Apagar en 10 minutos
shutdown -c                 # Cancelar shutdown programado
```

---

## Casos de uso reales

**Servicio que falla al arrancar, investigar por qué:**
```bash
systemctl status nombre_servicio
journalctl -u nombre_servicio -n 50 --no-pager
```

**Crear un script que corre al reiniciar:**
```bash
# En crontab
@reboot /scripts/mi_script.sh

# O como servicio systemd con After=network.target
```

**Ver qué servicios tardan más en arrancar:**
```bash
systemd-analyze blame
systemd-analyze critical-chain
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| Servicio falla silenciosamente | `journalctl -u servicio -n 100` |
| No arranca en el boot | `systemctl is-enabled servicio` |
| Cambié el unit file y no aplica | `systemctl daemon-reload` |
| Cron no ejecuta el script | Revisar permisos, logs en `/var/log/syslog` |
| Quiero saber cuánto tarda el boot | `systemd-analyze` |
