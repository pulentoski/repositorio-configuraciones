# 07 — Logs y auditoría

> Los logs son la memoria del sistema. Saber leerlos, filtrarlos y analizarlos es lo que separa a un sysadmin que adivina de uno que diagnostica.

---

## Archivos de log principales

> **Qué es:** Un log es un registro con fecha y hora de lo que ocurre en el sistema: accesos, errores y cambios.
>
> **Para qué sirve:** Son la evidencia para detectar incidentes y demostrar cumplimiento (NIST AU-2, AU-6).

| Archivo | Contenido |
|---|---|
| `/var/log/syslog` | Log general del sistema (Debian/Ubuntu) |
| `/var/log/messages` | Log general (RHEL/CentOS) |
| `/var/log/auth.log` | Autenticaciones, sudo, SSH (Debian/Ubuntu) |
| `/var/log/secure` | Idem para RHEL/CentOS |
| `/var/log/kern.log` | Mensajes del kernel |
| `/var/log/dmesg` | Boot del kernel |
| `/var/log/dpkg.log` | Instalaciones de paquetes (Debian) |
| `/var/log/apt/` | Historial de apt |
| `/var/log/nginx/` | Access y error logs de nginx |
| `/var/log/mysql/` | Logs de MySQL/MariaDB |
| `/var/log/fail2ban.log` | Bans por fail2ban |

---

## Leer y seguir logs

> **Qué es:** Formas de ver el contenido de un log completo, parcial o en tiempo real.
>
> **Para qué sirve:** Observar eventos mientras ocurren, por ejemplo un intento de login.

```bash
tail -f /var/log/syslog             # Seguir en tiempo real
tail -n 100 /var/log/auth.log       # Últimas 100 líneas
head -n 50 /var/log/syslog          # Primeras 50 líneas
cat /var/log/syslog | less          # Paginar
less +F /var/log/syslog             # less siguiendo el archivo (q para parar, F para seguir)
```

---

## Filtrar con grep

> **Qué es:** grep busca líneas que contienen un texto o patrón.
>
> **Para qué sirve:** Encontrar en segundos el evento relevante dentro de miles de líneas.

```bash
grep "error" /var/log/syslog                    # Buscar "error"
grep -i "error" /var/log/syslog                 # Ignorar mayúsculas
grep -n "failed" /var/log/auth.log              # Con número de línea
grep -v "INFO" /var/log/syslog                  # Excluir líneas con "INFO"
grep -E "error|warning|critical" /var/log/syslog  # Múltiples patrones
grep -A 5 "FAILED" /var/log/auth.log            # 5 líneas después del match
grep -B 5 "FAILED" /var/log/auth.log            # 5 líneas antes del match
grep -C 5 "FAILED" /var/log/auth.log            # 5 líneas antes y después
grep -r "error" /var/log/nginx/                 # Recursivo en directorio
```

---

## Procesamiento con awk y sed

> **Qué es:** awk extrae y procesa columnas; sed transforma texto.
>
> **Para qué sirve:** Generar estadísticas desde logs: IPs más frecuentes, errores por hora, etc.

```bash
# awk: filtrar columnas y procesar texto
awk '{print $1, $4}' /var/log/nginx/access.log          # Columnas 1 y 4
awk '$9 == "404"' /var/log/nginx/access.log              # Filtrar por código HTTP
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -20  # Top IPs

# sed: reemplazar y transformar
sed -n '/Jan 15/p' /var/log/syslog          # Solo líneas con "Jan 15"
sed 's/error/ERROR/g' archivo.log           # Reemplazar texto
sed '/^#/d' archivo.conf                    # Eliminar comentarios
```

---

## journalctl (systemd journal)

> **Qué es:** Consulta del registro central de systemd, filtrable por servicio, fecha y prioridad.
>
> **Para qué sirve:** Auditar un servicio específico (por ejemplo `ssh`) en un rango de tiempo.

```bash
journalctl                              # Todo el journal
journalctl -f                           # En tiempo real
journalctl -u servicio                  # Logs de un servicio
journalctl -u servicio -f               # Seguir logs de un servicio
journalctl -b                           # Boot actual
journalctl -b -1                        # Boot anterior
journalctl --since "2024-01-01 08:00"
journalctl --since "1 hour ago"
journalctl --since "1 hour ago" --until "30 minutes ago"
journalctl -p err                       # Solo errores (emerg, alert, crit, err)
journalctl -p warning                   # Warnings y superiores
journalctl -k                           # Solo kernel
journalctl --no-pager | grep -i error   # Pipe a grep
journalctl -o json-pretty -u nginx      # Formato JSON
```

---

## Rotación de logs con logrotate

> **Qué es:** Proceso que archiva, comprime y elimina logs antiguos según reglas.
>
> **Para qué sirve:** Evitar que los logs llenen el disco y definir cuánto tiempo se conserva la evidencia (NIST AU-11).

```bash
cat /etc/logrotate.conf             # Configuración global
ls /etc/logrotate.d/                # Configuraciones por aplicación
logrotate -d /etc/logrotate.conf    # Dry run (simular sin ejecutar)
logrotate -f /etc/logrotate.conf    # Forzar rotación ahora
```

### Ejemplo de configuración logrotate

```bash
# logrotate no admite comentarios al final de la línea: van en su propia línea
/var/log/miapp/*.log {
    # Rotar diariamente y mantener 7 archivos
    daily
    rotate 7
    # Comprimir logs viejos, desde el segundo
    compress
    delaycompress
    # Sin error si no existe; no rotar si está vacío
    missingok
    notifempty
    # Permisos del nuevo archivo
    create 0640 www-data adm
    postrotate
        systemctl reload nginx
    endscript
}
```

---

## Auditoría con auditd

> **Qué es:** Sistema de auditoría del kernel que registra accesos a archivos y ejecución de comandos según reglas.
>
> **Para qué sirve:** Auditoría detallada: saber quién modificó un archivo crítico y cuándo.

```bash
# Instalar
apt install auditd

# Estado
systemctl status auditd
auditctl -s                         # Estado del subsistema de auditoría
auditctl -l                         # Reglas activas

# Agregar reglas
auditctl -w /etc/passwd -p wa -k cambios_passwd   # Monitorear escrituras en /etc/passwd
auditctl -w /etc/sudoers -p wa -k sudoers          # Monitorear sudoers
auditctl -a always,exit -F arch=b64 -S execve -k ejecuciones  # Registrar ejecuciones

# Consultar logs de auditoría
ausearch -k cambios_passwd          # Buscar por clave
ausearch -f /etc/passwd             # Buscar por archivo
ausearch -ua root                   # Acciones del usuario root
ausearch -ts today                  # Solo hoy
aureport --summary                  # Resumen
aureport --logins                   # Resumen de logins
aureport --failed                   # Solo fallos
```

---

## Monitoreo de accesos SSH

> **Qué es:** Revisión de los eventos de conexión remota registrados en auth.log.
>
> **Para qué sirve:** Detectar ataques de fuerza bruta y accesos no autorizados.

```bash
# Ver intentos fallidos de login
grep "Failed password" /var/log/auth.log
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# Ver logins exitosos
grep "Accepted" /var/log/auth.log

# Ver intentos de login como root
grep "Invalid user\|Failed password for root" /var/log/auth.log

# Con journalctl
journalctl -u ssh --since "24 hours ago" | grep -i "failed\|invalid"
```

---

## Eventos de autenticación en auth.log (Ubuntu)

> **Qué es:** Cada intento de acceso o uso de sudo deja una línea con fecha, usuario, IP y resultado.
>
> **Para qué sirve:** Reconocer cada tipo de evento para poder analizarlo y citarlo como evidencia en una auditoría.

> Con `PasswordAuthentication no` las líneas `Failed password` dejan de aparecer: los intentos fallidos se ven con los mensajes de esta tabla.

| Evento | Línea típica en `/var/log/auth.log` |
|---|---|
| Login con llave exitoso | `sshd[...]: Accepted publickey for usr_admin from 203.0.113.10 port 51234 ssh2: ED25519 SHA256:...` |
| Llave OK, falta el MFA | `sshd[...]: Partial publickey for usr_admin from 203.0.113.10 ...` |
| MFA exitoso | `sshd[...]: Accepted keyboard-interactive/pam for usr_admin from 203.0.113.10 ...` |
| Código MFA incorrecto | `sshd(pam_google_authenticator)[...]: Invalid verification code for usr_admin` |
| Cliente sin llave válida | `sshd[...]: Connection closed by authenticating user usr_admin 203.0.113.10 port 51234 [preauth]` |
| Usuario inexistente | `sshd[...]: Invalid user admin from 198.51.100.7 port 40022` |
| Intento como root | `sshd[...]: ROOT LOGIN REFUSED FROM 198.51.100.7 port 40022` |
| Grupo no autorizado | `sshd[...]: User invitado from 203.0.113.10 not allowed because none of user's groups are listed in AllowGroups` |
| sudo permitido | `sudo: usr_admin : TTY=pts/0 ; PWD=/home/usr_admin ; USER=root ; COMMAND=/usr/bin/apt update` |
| sudo con comando no autorizado | `sudo: usr_auditor : command not allowed ; TTY=pts/0 ; ... ; COMMAND=/usr/bin/cat /etc/shadow` |
| sudo sin permisos | `sudo: invitado : user NOT in sudoers ; TTY=pts/0 ; ... ; COMMAND=/usr/bin/ls /root` |

```bash
# Accesos SSH: exitosos, parciales, fallidos y rechazados
sudo grep -E "Accepted|Partial|Failed|Invalid|REFUSED|not allowed|Connection closed by authenticating" /var/log/auth.log

# Uso de sudo (permitido y denegado)
sudo grep "sudo:" /var/log/auth.log
sudo grep -E "command not allowed|NOT in sudoers" /var/log/auth.log

# Códigos MFA incorrectos
sudo grep "Invalid verification code" /var/log/auth.log

# Mismo análisis con journalctl
journalctl -u ssh --since today --no-pager

# Sesiones: quién entró, quién falló, quién está conectado
last -a | head -20
sudo lastb -a | head -20
who
```

**Cómo leer un evento para el informe:** fecha y hora → servicio (`sshd`, `sudo`) → usuario → IP de origen → resultado. Ese es el contenido mínimo que exige NIST AU-3.

---

## Centralización de logs con rsyslog

> **Qué es:** Envío de logs a un servidor central.
>
> **Para qué sirve:** Si un atacante borra los logs locales, la copia central se conserva (NIST AU-9).

```bash
# Ver configuración
cat /etc/rsyslog.conf
ls /etc/rsyslog.d/

# Enviar logs a servidor remoto (en rsyslog.conf del cliente)
*.* @192.168.1.100:514      # UDP
*.* @@192.168.1.100:514     # TCP

# Recibir logs en el servidor
# Descomentar en rsyslog.conf:
# module(load="imudp")
# input(type="imudp" port="514")

systemctl restart rsyslog
```

---

## Casos de uso reales

**Investigar un intento de acceso no autorizado:**
```bash
grep "Invalid user" /var/log/auth.log | awk '{print $10,$13}' | sort | uniq -c | sort -rn
```

**Ver los últimos errores de cualquier servicio:**
```bash
journalctl -p err -b --no-pager | tail -30
```

**Cuánto espacio ocupan los logs:**
```bash
du -sh /var/log/*  | sort -rh | head -10
journalctl --disk-usage
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| Logs llenos, disco al 100% | `journalctl --vacuum-size=1G` |
| No encuentro cuándo falló algo | `journalctl -b -1 -p err` |
| Quiero ver accesos SSH de hoy | `journalctl -u ssh --since today` |
| Log de nginx vacío | `systemctl status nginx` — puede estar fallando antes de loguear |
| auditd llena el disco | Revisar reglas demasiado amplias con `auditctl -l` |
