# 08 — Seguridad del servidor

> Un servidor expuesto sin hardening es una invitación abierta. Estas son las prácticas y herramientas fundamentales para reducir la superficie de ataque.

---

## SSH — Configuración segura

> **Qué es:** SSH es el protocolo de administración remota cifrada. Su configuración está en `/etc/ssh/sshd_config`.
>
> **Para qué sirve:** Es la puerta de entrada al servidor: si SSH es débil, todo el servidor lo es.

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

> `sshd_config` **no admite comentarios al final de la línea**: `PermitRootLogin no  # comentario` hace fallar el servicio. Los comentarios van en su propia línea.

> **Ubuntu en la nube:** existe `/etc/ssh/sshd_config.d/50-cloud-init.conf`, que puede sobrescribir `PasswordAuthentication`. En OpenSSH gana el **primer** valor leído, así que lo recomendado es crear un archivo propio que se lea antes: `/etc/ssh/sshd_config.d/10-seguridad.conf`.

```bash
sudo nano /etc/ssh/sshd_config.d/10-seguridad.conf
```

```bash
# Nunca login directo como root
PermitRootLogin no
# Solo llaves, sin contraseñas
PasswordAuthentication no
PubkeyAuthentication yes
# Máximo 3 intentos por conexión y 20 s para autenticarse
MaxAuthTries 3
LoginGraceTime 20
# Deshabilitar reenvío gráfico si no se usa
X11Forwarding no
# Mensaje legal antes del login
Banner /etc/ssh/banner.txt
# Detecta conexiones caídas (no cierra sesiones inactivas: ver TMOUT más abajo)
ClientAliveInterval 300
ClientAliveCountMax 2
# Cambiar el puerto es opcional. En AWS, el nuevo puerto debe abrirse
# antes en el Security Group, o se pierde el acceso a la instancia.
# Port 2222
```

```bash
# Validar sintaxis ANTES de reiniciar (sin salida = correcto)
sudo sshd -t

# Aplicar cambios (en Ubuntu el servicio se llama ssh)
sudo systemctl restart ssh

# Ver la configuración efectiva que quedó aplicada
sudo sshd -T | grep -Ei "permitroot|passwordauth|maxauth|authenticationmethods|allowgroups"
```

> Mantener una sesión SSH abierta mientras se prueban cambios, y probar desde una **segunda** terminal. Si algo falla, se corrige desde la sesión abierta.

---

## Autenticación multifactor (MFA) en SSH

> **Qué es:** MFA exige dos factores distintos: algo que se tiene (la llave SSH) y algo que se genera en el celular (código TOTP de 6 dígitos que cambia cada 30 s).
>
> **Para qué sirve:** Si roban la llave, no basta para entrar. Cumple NIST IA-2(1).

Se usa Google Authenticator (TOTP). Sirve cualquier app compatible: Google Authenticator, Microsoft Authenticator, Authy.

**1. Instalar el módulo PAM**
```bash
sudo apt install libpam-google-authenticator -y
```

**2. Enrolar cada usuario** (ejecutar como el usuario, no con sudo)
```bash
google-authenticator
```
Respuestas recomendadas: `y` (códigos basados en tiempo) → escanear el QR con la app → guardar los códigos de emergencia → `y` (actualizar archivo) → `y` (no reutilizar códigos) → `n` (no ampliar ventana) → `y` (limitar intentos).

**3. Configurar PAM** en `/etc/pam.d/sshd`
```bash
# Comentar esta línea: si no, además pedirá la contraseña Linux
#@include common-auth

# Agregar al final:
auth required pam_google_authenticator.so nullok
```
`nullok` deja entrar sin MFA a usuarios que aún no se enrolan (por ejemplo `ubuntu`). Cuando todos estén enrolados, se quita para que el MFA sea obligatorio.

**4. Configurar SSH** en `/etc/ssh/sshd_config.d/10-seguridad.conf`
```bash
UsePAM yes
KbdInteractiveAuthentication yes
# Exige llave Y código: sin esta línea, la llave sola basta y el MFA nunca se pide
AuthenticationMethods publickey,keyboard-interactive
```

**5. Aplicar y probar**
```bash
sudo sshd -t && sudo systemctl restart ssh
# Desde otra terminal:
ssh -i llave.pem usr_admin@IP_PUBLICA
# Debe pedir: Verification code:
```

> El TOTP depende de la hora. Si los códigos fallan siempre, revisar `timedatectl` en el servidor y la hora del celular.

---

## Acceso condicional y control de sesiones

> **Qué es:** Reglas que deciden quién puede entrar, desde dónde y por cuánto tiempo.
>
> **Para qué sirve:** Limitar el acceso por grupo e IP, cortar sesiones inactivas y limitar intentos fallidos (NIST AC-7, AC-12, AC-17).

**Acceso por grupo e IP** (en `10-seguridad.conf`)
```bash
# Solo estos grupos pueden entrar por SSH.
# Incluir el grupo del usuario administrador (en EC2: ubuntu) o quedará fuera.
AllowGroups sysops auditores ubuntu

# Restricción por IP: el usuario auditor solo desde una IP específica.
# Formato USUARIO@IP o USUARIO@RED/MÁSCARA. Los usuarios no listados quedan bloqueados.
AllowUsers ubuntu usr_admin usr_auditor@203.0.113.10
```
`AllowGroups` y `AllowUsers` se aplican juntos: el usuario debe cumplir ambos.

**MFA solo para un grupo** (alternativa a exigirlo a todos)
```bash
Match Group sysops
    AuthenticationMethods publickey,keyboard-interactive
```
Los bloques `Match` van **al final** del archivo: todo lo que sigue a un `Match` queda dentro de él.

**Límite de intentos y de sesiones simultáneas**
```bash
# En 10-seguridad.conf: intentos por conexión y tiempo para autenticarse
MaxAuthTries 3
LoginGraceTime 20
```
```bash
# Máximo 2 sesiones simultáneas por usuario del grupo auditores (vía pam_limits)
echo "@auditores hard maxlogins 2" | sudo tee -a /etc/security/limits.conf
```

**Cierre de sesiones inactivas** (`ClientAliveInterval` no lo hace: solo detecta conexiones caídas)
```bash
# Cierra la shell tras 10 minutos sin actividad
echo 'readonly TMOUT=600; export TMOUT' | sudo tee /etc/profile.d/99-tmout.sh
```

**Revisión de sesiones**
```bash
who                          # Quién está conectado ahora
w                            # Conectados y qué están haciendo
last -a | head -20           # Historial de sesiones con IP
sudo lastb -a | head -20     # Intentos fallidos
lastlog                      # Último acceso de cada usuario
loginctl list-sessions       # Sesiones activas según systemd
sudo pkill -KILL -t pts/1    # Cerrar a la fuerza la sesión de la terminal pts/1
```

---

## Fail2ban — Bloqueo automático de ataques

> **Qué es:** Servicio que lee los logs y bloquea en el firewall las IPs con demasiados intentos fallidos.
>
> **Para qué sirve:** Frenar ataques de fuerza bruta de forma automática.

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
# Duración del ban, ventana de tiempo e intentos antes del ban
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true
# ssh = puerto 22. Si se cambió el puerto, poner el número (ej. 2222)
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 24h
```

```bash
systemctl restart fail2ban
```

---

## UFW — Firewall simplificado

> **Qué es:** Interfaz simple para administrar el firewall del sistema operativo.
>
> **Para qué sirve:** Segunda capa de filtrado dentro del servidor, además del Security Group de AWS (defensa en profundidad).

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

> **Qué es:** Parches que corrigen vulnerabilidades conocidas del sistema y los paquetes.
>
> **Para qué sirve:** La mayoría de las intrusiones explotan fallas ya parchadas; actualizar es el control más efectivo (NIST SI-2).

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

> **Qué es:** Herramienta que revisa la configuración del sistema y entrega un puntaje y recomendaciones.
>
> **Para qué sirve:** Obtener un diagnóstico rápido de hardening y una lista de mejoras.

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

> **Qué es:** Un rootkit es malware que se oculta en el sistema para mantener acceso.
>
> **Para qué sirve:** Revisar si un servidor fue comprometido.

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

> **Qué es:** Un certificado permite cifrar el tráfico web (HTTPS) y acreditar la identidad del servidor.
>
> **Para qué sirve:** Proteger los datos en tránsito (NIST SC-8).

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

> **Qué es:** Búsqueda de archivos con permisos peligrosos o modificados.
>
> **Para qué sirve:** Detectar vías de escalamiento de privilegios o archivos alterados.

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

> **Qué es:** Hardening es reducir la superficie de ataque quitando lo innecesario y restringiendo lo que queda.
>
> **Para qué sirve:** Complementar el hardening de SSH y firewall con ajustes del sistema.

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
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sshd -t && systemctl restart ssh
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
| SSH falla al reiniciar | `sshd -t` muestra la línea con error |
| Ya no pide el código MFA | Falta `AuthenticationMethods publickey,keyboard-interactive` |
| Pide contraseña además del código | Comentar `@include common-auth` en `/etc/pam.d/sshd` |
| Quedé fuera de la instancia EC2 | EC2 Instance Connect o consola serial desde AWS |
| SSH no acepta la clave | `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys` |
| Puerto SSH bloqueado por UFW | `ufw status` desde consola local |
| Certificado SSL expirado | `certbot renew` o `openssl x509 -noout -enddate -in cert.pem` |
