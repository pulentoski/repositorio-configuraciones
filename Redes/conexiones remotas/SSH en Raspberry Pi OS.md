# Guía de Instalación y Configuración de SSH en Raspberry Pi OS

## Instalación de OpenSSH

Raspberry Pi OS suele incluir OpenSSH, pero si no está instalado, usa:
```bash
sudo apt update && sudo apt install -y openssh-server
```

## Habilitar y Verificar el Servicio

### Iniciar el servicio SSH:
```bash
sudo systemctl start ssh
```

### Habilitar el servicio al iniciar el sistema:
```bash
sudo systemctl enable ssh
```

### Verificar el estado del servicio:
```bash
sudo systemctl status ssh
```

## Habilitar SSH desde `raspi-config`
```bash
sudo raspi-config
```
Ve a **Interfacing Options > SSH** y actívalo.

## Configuración de SSH

El archivo de configuración principal está en:
```bash
/etc/ssh/sshd_config
```

Algunas opciones recomendadas:
- **Cambiar el puerto por defecto** (Ejemplo: 2222)
  ```bash
  Port 2222
  ```
- **Deshabilitar acceso root directo**
  ```bash
  PermitRootLogin no
  ```
- **Permitir solo usuarios específicos**
  ```bash
  AllowUsers usuario1 usuario2
  ```
- **Habilitar autenticación con clave pública**
  ```bash
  PasswordAuthentication no
  ```

Aplicar cambios:
```bash
sudo systemctl restart ssh
```

## Configuración de Claves SSH

### Generar un par de claves SSH
```bash
ssh-keygen -t ed25519
```

### Copiar clave pública al servidor
```bash
ssh-copy-id usuario@raspberrypi
```

### Conectar al Raspberry Pi
```bash
ssh -p 2222 usuario@raspberrypi
```

## Seguridad Adicional

- **Configurar Fail2Ban para prevenir ataques de fuerza bruta**
  ```bash
  sudo apt install fail2ban
  ```
- **Usar autenticación con claves en lugar de contraseña**
- **Deshabilitar protocolos inseguros en `/etc/ssh/sshd_config`**
  ```bash
  Protocol 2
  ```
- **Restringir acceso con `ufw` (firewall)**
  ```bash
  sudo ufw allow 2222/tcp
  sudo ufw enable
  ```

## Desinstalación de SSH

Si deseas eliminar OpenSSH:
```bash
sudo apt remove --purge -y openssh-server
```

## Referencias
- [Documentación Oficial de OpenSSH](https://www.openssh.com/manual.html)
- [Guía de Raspberry Pi](https://www.raspberrypi.com/documentation/)
