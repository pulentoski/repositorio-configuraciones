# Guía de Instalación y Configuración de SSH en Linux

## Instalación de OpenSSH

### En Debian, Ubuntu y derivados:
```bash
sudo apt update && sudo apt install -y openssh-server
```

### En RHEL, CentOS y Fedora:
```bash
sudo dnf install -y openssh-server
```

### En Arch Linux:
```bash
sudo pacman -S openssh
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
ssh-keygen -t rsa -b 4096
```

### Copiar clave pública al servidor
```bash
ssh-copy-id usuario@servidor
```

### Conectar al servidor
```bash
ssh -p 2222 usuario@servidor
```

## Seguridad Adicional

- **Configurar Fail2Ban para prevenir ataques de fuerza bruta**
  ```bash
  sudo apt install fail2ban  # Debian/Ubuntu
  sudo dnf install fail2ban  # RHEL/CentOS
  ```
- **Usar autenticación con claves en lugar de contraseña**
- **Deshabilitar protocolos inseguros en `/etc/ssh/sshd_config`**
  ```bash
  Protocol 2
  ```

## Desinstalación de SSH

Si deseas eliminar OpenSSH:

### En Debian, Ubuntu y derivados:
```bash
sudo apt remove --purge -y openssh-server
```

### En RHEL, CentOS y Fedora:
```bash
sudo dnf remove -y openssh-server
```

### En Arch Linux:
```bash
sudo pacman -Rns openssh
```

## Referencias
- [Documentación Oficial de OpenSSH](https://www.openssh.com/manual.html)
