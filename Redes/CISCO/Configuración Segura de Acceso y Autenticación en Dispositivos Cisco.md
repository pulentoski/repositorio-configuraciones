# Configuración Segura de Acceso y Autenticación en Dispositivos Cisco

Este documento presenta la configuración recomendada para asegurar el acceso a dispositivos Cisco mediante contraseñas cifradas, control de intentos de inicio de sesión, configuración SSH, ACLs y monitoreo. Cada comando se explica de manera técnica y resumida.

# 1. Cifrado de Contraseñas y Políticas de Seguridad

Cifra todas las contraseñas almacenadas.
  
    service password-encryption

Define longitud mínima de contraseña de 8 caracteres.
  
    security passwords min-length 8

# 2. Control de Intentos de Inicio de Sesión

Bloquea acceso 120s tras 3 intentos fallidos en 60s.
   
    login block-for 120 attempts 3 within 60

Bloquea acceso 15s tras 5 intentos fallidos en 60s.
   
    login block-for 15 attempts 5 within 60

Retraso de 10s entre intentos de login.
  
    login delay 10

Registra inicios de sesión exitosos.
  
    login on-success log

Registra intentos fallidos de inicio de sesión.
  
    login on-failure log

# 3. Configuración de Contraseña Enable

Contraseña enable pre-encriptada tipo 9 (SCRYPT).
  
    enable secret 9 $9$HZNdzLHwhPtZ3U$D901UD5GvBy.m8Tf9vCGDJRcYy8zIMbyRJgtxgRkwzY

Contraseña enable cifrada con algoritmo SCRYPT.
   
    enable algorithm-type scrypt secret cisco12345

# 4. Gestión de Usuarios

Crea usuario "Bob" con contraseña MD5.
   
    username Bob secret cisco54321

Reconfigura contraseña de "Bob" con SCRYPT.
   
    username Bob algorithm-type scrypt secret cisco54321

# 5. Configuración de ACL para Acceso Restringido

Crea ACL estándar PERMIT-ADMIN.
   
    ip access-list standard PERMIT-ADMIN

Comentario descriptivo de ACL.
  
    remark Permit only Administrative hosts

Permite acceso desde IP 192.168.10.10.
  
    permit 192.168.10.10

Permite acceso desde IP 192.168.11.10.
   
    permit 192.168.11.10

Restringe acceso a IPs de ACL en modo quiet.
  
    login quiet-mode access-class PERMIT-ADMIN

# 6. Configuración de SSH

Configura nombre de dominio del dispositivo.
   
    ip domain-name span.com

Genera claves RSA de 1024 bits para SSH.
  
    crypto key generate rsa general-keys modulus 1024

Habilita SSH versión 2.
  
    ip ssh version 2

Tiempo de espera para autenticación SSH 60s.
   
    ip ssh time-out 60

Máximo de 2 reintentos de autenticación SSH.
    
    ip ssh authentication-retries 2

# 7. Configuración de Líneas VTY

Accede a líneas VTY 0 a 4.
  
    line vty 0 4

Establece contraseña VTY.
    
    password cisco123

Habilita autenticación local en VTY.
  
    login local

Timeout de sesión VTY 5min30s.
  
    exec-timeout 5 30

Restringe VTY solo a conexiones SSH.
  
    transport input ssh

# 8. Monitoreo y Diagnóstico

Muestra intentos fallidos de login.
  
    show login failures

Muestra configuración actual de SSH.
   
    show ip ssh
