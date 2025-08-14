# Configuración de SSH en Dispositivos Cisco

Este documento describe la configuración de SSH en dispositivos Cisco, incluyendo hostname, dominio, usuario, claves RSA, líneas VTY, versión SSH, interfaz de gestión y verificación.  
Cada comando incluye explicación técnica y resumida.

# 1. Configurar Hostname y Dominio

Cambia el nombre del dispositivo.
  
    hostname R1

Configura un nombre de dominio requerido para SSH.
 
    ip domain-name ejemplo.com

# 2. Generar Claves RSA (Para Cifrado SSH)

Genera claves RSA para cifrado de sesiones SSH.
  
    crypto key generate rsa

Genera claves RSA especificando el tamaño de 2048 bits.
    
    crypto key generate rsa general-keys modulus 2048

# 3. Configurar Usuario y Contraseña para SSH

Crea un usuario con privilegio máximo y contraseña cifrada.
    
    username admin privilege 15 secret contraseña

# 4. Habilitar SSH y Configurar Líneas VTY

Accede a las líneas virtuales VTY 0 a 4.
    
    line vty 0 4

Permite solo conexiones SSH en VTY.
    
    transport input ssh

Habilita autenticación local para VTY.
    
    login local

# 5. Configurar Versión SSH (Opcional)

Habilita SSH versión 2, más seguro que la versión 1.
  
    ip ssh version 2

# 6. Habilitar Acceso SSH en una Interfaz

# 7. Verificar la Configuración SSH

Muestra el estado de la configuración SSH.
  
    show ip ssh

Muestra las sesiones SSH activas.
  
    show ssh

# 8. Probar SSH desde una PC en Packet Tracer

1 - Abre la PC en Packet Tracer y ve a "Desktop" > "Command Prompt".

2 - Conecta vía SSH usando el usuario y la IP del router.
  
    ssh -l admin 192.168.1.1

Ingresa la contraseña configurada para autenticación.
