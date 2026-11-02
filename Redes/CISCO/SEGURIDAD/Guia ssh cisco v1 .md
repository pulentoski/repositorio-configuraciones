# 🔐 Configuración de SSH en Dispositivos Cisco

Configuración de SSH en routers y switches Cisco: versiones, prerrequisitos, configuración paso a paso, verificación y prueba desde Packet Tracer.
Cada comando incluye una explicación breve.

---

# 📘 1. ¿Qué es SSH?

SSH (Secure Shell) permite administrar equipos de red de forma remota con la comunicación cifrada. Reemplaza a Telnet, que envía usuario, contraseña y comandos en texto plano.

SSH entrega:

- **Autenticación:** por contraseña o por clave pública.
- **Cifrado:** algoritmos simétricos como AES protegen los datos transmitidos.
- **Integridad:** los MAC (Message Authentication Code) detectan si los datos fueron alterados.

---

# 🔢 2. Versiones de SSH en Cisco IOS

| `show ip ssh` muestra | Significado |
|---|---|
| `version 1.5` | Solo SSHv1. Es obsoleto e inseguro. |
| `version 1.99` | Modo compatibilidad: acepta v1 y v2. Es el valor por defecto al generar las claves. |
| `version 2.0` | Solo SSHv2. Es lo recomendado. |

- `1.99` no es una versión del protocolo. Indica que el equipo acepta ambas.
- SSHv2 requiere claves RSA de **768 bits como mínimo**. Se recomiendan 2048.
- En SSHv2, al autenticar con clave pública, el cliente **firma** un dato de la sesión con su clave privada y el servidor verifica la firma con la clave pública. El esquema de "desafío que el cliente descifra" corresponde a SSHv1.

---

# 📋 3. Prerrequisitos

Para que SSH funcione, el equipo necesita:

1. Un hostname distinto al de fábrica (`Router` o `Switch`).
2. Un nombre de dominio.
3. Claves RSA generadas.
4. Un usuario local, o un servidor AAA.
5. Una IP alcanzable (interfaz o SVI).

> ⚠️ El hostname y el dominio se usan para nombrar las claves RSA. Si faltan, `crypto key generate rsa` da error.

---

# ⚙️ 4. Entrar a Configuración Global

Entra al modo privilegiado.

    enable

Entra al modo de configuración global. Todos los comandos siguientes se ejecutan aquí.

    configure terminal

---

# 🏷️ 5. Hostname, Dominio y Contraseña de Enable

Cambia el nombre del dispositivo. Es obligatorio antes de generar las claves.

    hostname R1

Configura el dominio que se usa para nombrar las claves RSA.

    ip domain-name ejemplo.com

Protege el modo privilegiado con una contraseña cifrada (hash).

    enable secret Cisco123

---

# 👤 6. Crear Usuario Local

Crea un usuario con privilegio máximo y contraseña cifrada.

    username admin privilege 15 secret Admin123

> 💡 Use `secret`, no `password`. `password` se guarda en texto plano o con un cifrado débil (tipo 7).

---

# 🔑 7. Generar Claves RSA

Genera un par de claves RSA de 2048 bits.

    crypto key generate rsa general-keys modulus 2048

> ⚠️ Si se ejecuta solo `crypto key generate rsa`, el equipo pregunta el tamaño y propone 512 por defecto. Con 512 bits no funciona SSHv2. Escriba siempre `2048`.

Al generar las claves, SSH queda habilitado automáticamente en modo `1.99`.

---

# 🛡️ 8. Forzar SSH Versión 2

Deja activo solo SSHv2. Debe ejecutarse **después** de generar las claves.

    ip ssh version 2

Tiempo máximo (segundos) para completar la autenticación.

    ip ssh time-out 60

Número de intentos de autenticación permitidos por conexión.

    ip ssh authentication-retries 3

---

# 🌐 9. Configurar IP de Gestión

**En un router:** asigna una IP a una interfaz física y la activa.

    interface g0/0
     ip address 192.168.1.1 255.255.255.0
     no shutdown
    exit

**En un switch:** asigna una IP a la SVI y define el gateway.

    interface vlan 1
     ip address 192.168.1.2 255.255.255.0
     no shutdown
    exit
    ip default-gateway 192.168.1.1

---

# 🖧 10. Configurar Líneas VTY

Accede a las líneas virtuales 0 a 4 (en switches existen también 5 a 15).

    line vty 0 4

Permite solo conexiones SSH y bloquea Telnet.

    transport input ssh

Usa la base de usuarios locales para autenticar.

    login local

Cierra la sesión tras 5 minutos de inactividad.

    exec-timeout 5 0

    exit

Vuelve al modo privilegiado y guarda la configuración.

    end
    copy running-config startup-config

---

# ✅ 11. Verificación

Muestra el estado de SSH, la versión activa, el timeout y los reintentos.

    show ip ssh

Salida esperada:

    SSH Enabled - version 2.0

> ⚠️ Si aparece `1.99`, falta `ip ssh version 2`.
> ⚠️ Si aparece `SSH Disabled`, faltan las claves RSA.

Muestra las sesiones SSH activas.

    show ssh

Muestra las claves RSA generadas.

    show crypto key mypubkey rsa

Muestra los usuarios conectados por VTY.

    show users

---

# 💻 12. Probar desde una PC en Packet Tracer

1. Abra la PC y vaya a **Desktop > Command Prompt**.
2. Conéctese con el usuario y la IP del equipo:

        ssh -l admin 192.168.1.1

3. Ingrese la contraseña del usuario (`Admin123`).
4. Para entrar al modo privilegiado use `enable` (`Cisco123`). Con privilegio 15 se entra directo.

---

# 📄 13. Configuración Completa (Router)

    enable
    configure terminal
     hostname R1
     ip domain-name ejemplo.com
     enable secret Cisco123
     username admin privilege 15 secret Admin123
     crypto key generate rsa general-keys modulus 2048
     ip ssh version 2
     ip ssh time-out 60
     ip ssh authentication-retries 3
     interface g0/0
      ip address 192.168.1.1 255.255.255.0
      no shutdown
     exit
     line vty 0 4
      transport input ssh
      login local
      exec-timeout 5 0
     exit
    end
    copy running-config startup-config

---

# 🛠️ 14. Errores Comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `Please define a hostname other than Router` | Hostname por defecto | `hostname R1` |
| `Please define a domain-name first` | Falta dominio | `ip domain-name ejemplo.com` |
| `ip ssh version 2` falla | Claves de 512 bits | Regenerar con `modulus 2048` |
| `SSH Disabled` | No hay claves RSA | `crypto key generate rsa general-keys modulus 2048` |
| `Connection refused` | VTY sin `transport input ssh` o sin IP | Revisar VTY e interfaz |
| `% Login invalid` | Usuario o contraseña errados, o falta `login local` | Revisar `username` y VTY |
| `crypto key encrypt rsa` no existe | No soportado en Packet Tracer | Omitir en PT |
