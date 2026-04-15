# 08 — Seguridad del servidor

> Un servidor expuesto sin hardening es una invitación abierta. Estas son las prácticas y herramientas fundamentales para reducir la superficie de ataque.

---

## SSH — Configuración segura

### Autenticación con clave pública (recomendado)

```bash
# En tu máquina local: generar par de claves
ssh-keygen -t ed25519 -C "tu@email.com"         # Ed25519 (recomendado, más seguro)
ssh-keygen -t rsa -b 4096 -C "tu@email.com"     # RSA 4096 bits (alternativa)

# Copiar clave pública al servidor
ssh-copy-id usuario@servidor
# O manualmente:
cat ~/.ssh/id_ed25519.pub | ssh usuario@servidor "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Verificar que funciona ANTES de deshabilitar contraseñas
ssh usuario@servidor
```

### Hardening de /etc/ssh/sshd_config

```bash
# Opciones recomendadas
Port 2222                           # Cambiar puerto por defecto
PermitRootLogin no                  # Nunca login directo como root
PasswordAuthentication no           # Solo claves, sin contraseñas
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
MaxAuthTries 3                      # Máximo 3 intentos
LoginGraceTime 20                   # 20 segundos para autenticarse
AllowUsers usuario1 usuario2        # Solo estos usuarios pueden conectarse
X11Forwarding no                    # Deshabilitar si no se usa
Banner /etc/ssh/banner.txt          # Mensaje legal antes del login
ClientAliveInterval 300             # Cerrar sesiones inactivas (5 min)
ClientAliveCountMax 2

# Aplicar cambios
systemctl restart sshd
```

---

## Fail2ban — Bloqueo automático de ataques

```bash
# Instalar
apt install fail2ban

# Estado
systemctl status fail2ban
fail2ban-client status              # Ver jails activas
fail2ban-client status sshd         # Estado de la jail SSH

# Gestión de IPs baneadas
fail2ban-client set sshd unbanip 1.2.3.4    # Desbanear IP
fail2ban-client banned              # Ver todas las IPs baneadas
```

### Configuración en /etc/fail2ban/jail.local

```ini
[DEFAULT]
bantime = 1h           # Duración del ban
findtime = 10m         # Ventana de tiempo para contar intentos
maxretry = 5           # Intentos antes del ban

[sshd]
enabled = true
port = 2222            # Si cambiaste el puerto SSH
logpath = /var/log/auth.log
maxretry = 3
bantime = 24h
```

```bash
systemctl restart fail2ban
```

---

## UFW — Firewall simplificado

```bash
# Estado
ufw status
ufw status verbose
ufw status numbered         # Con números de reglas

# Configuración básica (servidor web)
ufw default deny incoming   # Bloquear todo lo entrante por defecto
ufw default allow outgoing  # Permitir todo lo saliente

ufw allow ssh               # Puerto 22
ufw allow 2222/tcp          # SSH en puerto personalizado
ufw allow 80/tcp            # HTTP
ufw allow 443/tcp           # HTTPS
ufw allow from 10.0.0.0/24  # Permitir red interna completa
ufw allow from 10.0.0.5 to any port 5432   # PostgreSQL solo desde IP específica

# Activar
ufw enable

# Eliminar regla
ufw delete allow 80/tcp
ufw delete 3                # Por número (de ufw status numbered)

# Logs
ufw logging on
tail -f /var/log/ufw.log
```

---

## Actualizaciones de seguridad

```bash
# Debian/Ubuntu
apt update
apt upgrade
apt list --upgradable
apt-get dist-upgrade         # Incluye actualizaciones de kernel

# Actualizaciones automáticas de seguridad
apt install unattended-upgrades
dpkg-reconfigure unattended-upgrades
cat /etc/apt/apt.conf.d/50unattended-upgrades

# RHEL/CentOS
yum update
dnf update
dnf check-update
```

---

## Auditoría de seguridad con Lynis

```bash
# Instalar
apt install lynis

# Auditar el sistema completo
lynis audit system

# Ver puntaje y sugerencias
# El reporte queda en /var/log/lynis.log
# El reporte detallado en /var/log/lynis-report.dat
```

---

## Verificar rootkits

```bash
# chkrootkit
apt install chkrootkit
chkrootkit

# rkhunter
apt install rkhunter
rkhunter --update
rkhunter --check
rkhunter --check --skip-keypress      # Sin pausas interactivas
```

---

## Gestión de certificados SSL/TLS

```bash
# Ver certificado de un sitio
openssl s_client -connect dominio.com:443
echo | openssl s_client -connect dominio.com:443 2>/dev/null | openssl x509 -noout -dates

# Verificar certificado local
openssl x509 -in certificado.crt -text -noout
openssl x509 -in certificado.crt -noout -enddate  # Fecha de expiración

# Generar certificado autofirmado (para uso interno)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Let's Encrypt con certbot
apt install certbot
certbot certonly --standalone -d dominio.com
certbot renew                           # Renovar todos los certificados
certbot renew --dry-run                 # Probar renovación sin ejecutar
```

---

## Monitoreo de archivos críticos

```bash
# Ver archivos SUID/SGID (posibles vectores de escalación)
find / -perm /4000 2>/dev/null          # SUID
find / -perm /2000 2>/dev/null          # SGID

# Archivos world-writable (peligrosos)
find / -perm -o+w -not -path "/proc/*" 2>/dev/null

# Archivos sin dueño
find / -nouser -o -nogroup 2>/dev/null

# Verificar integridad de paquetes instalados
debsums -c                              # Verifica checksums de archivos de paquetes (Debian)
rpm -Va                                 # Idem en RHEL/CentOS
```

---

## Hardening adicional

```bash
# Deshabilitar servicios innecesarios
systemctl list-units --type=service --state=running
systemctl disable --now servicio_innecesario

# Limitar acceso a comandos sensibles
chmod 700 /usr/bin/top                  # Solo root (ejemplo)

# Configurar umask seguro
echo "umask 027" >> /etc/profile        # Nuevos archivos: 640, directorios: 750

# Bloquear acceso a /proc/PID de otros usuarios
# En /etc/fstab:
proc /proc proc defaults,hidepid=2 0 0

# Limitar core dumps
echo "* hard core 0" >> /etc/security/limits.conf
```

---

## Casos de uso reales

**Hardening rápido de un servidor nuevo:**
```bash
apt update && apt upgrade -y
ufw default deny incoming && ufw allow 22/tcp && ufw enable
apt install fail2ban -y && systemctl enable --now fail2ban
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
```

**Verificar si alguien entró al servidor:**
```bash
last -n 20
grep "Accepted" /var/log/auth.log | tail -20
journalctl -u ssh --since "24 hours ago"
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| Me baneé a mí mismo con fail2ban | Acceso físico/consola → `fail2ban-client set sshd unbanip TU_IP` |
| SSH no acepta la clave | `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys` |
| Puerto SSH bloqueado por UFW | `ufw status` desde consola local |
| Certificado SSL expirado | `certbot renew` o `openssl x509 -noout -enddate -in cert.pem` |
