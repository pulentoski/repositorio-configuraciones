# 🔐 TACACS+ Server (tac_plus-ng) - Cisco IOS Integration (Debian 13 Trixie)

Autenticación centralizada RFC 8907 para routers Cisco usando `tac_plus-ng` en **Debian 13 (Trixie)**. Adaptado y mantenido por Daniel "pulentoski" Soto.

---

## 📋 Contenido
1. [Resumen](#-resumen)
2. [Requisitos](#-requisitos)
3. [Instalación en Debian 13](#-instalación)
4. [Estructura de Directorios y Permisos de Logs](#-creación-de-estructura-de-directorios)
5. [Configuración del Servidor TACACS+](#-configuración)
6. [Configuración del Router Cisco (IOS 15/17)](#2️⃣-router-cisco-ios-15)
7. [Verificación Funcional](#-verificación)
8. [Troubleshooting Avanzado](#-troubleshooting)
9. [Lecciones Aprendidas](#-lecciones-aprendidas)

---

## 📖 Resumen
Implementación de un servidor TACACS+ funcional basado en `tac_plus-ng` (fork moderno mantenido del protocolo TACACS+ estándar RFC 8907) para autenticar usuarios en routers Cisco IOS, optimizado y probado para **Debian 13 (Trixie)**.

### ✨ Características Implementadas
- ✅ Autenticación centralizada contra servidor TACACS+ remoto.
- ✅ Fallback automático a autenticación local si el servidor no responde.
- ✅ Acceso por consola sin autenticación obligatoria (`no login` para seguridad física / emergencia).
- ✅ Cifrado robusto de credenciales vía clave compartida pre-compartida (Pre-shared key).
- ✅ Compatible RFC 8907 (estándar IETF TACACS+).
- ✅ Compilación desde código fuente adaptada a repositorios modernos de Debian 13.

---

## 🖥️ Requisitos

### Hardware
- **Servidor Debian 13:** 1 vCPU, 512 MB RAM, 2 GB disk (mínimo).
- **Router Cisco:** IOS 15.x o superior (también compatible con IOS-XE).
- **Red:** Conectividad L3 bidireccional entre ambos extremos (Puerto **TCP 49**).

### Software
- **Sistema Operativo:** Debian 13 (Trixie).
- **Herramientas de compilación y librerías de desarrollo:**
  ```bash
  apt update && apt install -y build-essential libssl-dev libpam0g-dev git perl \
                libpcre2-dev libcurl4-openssl-dev libldap2-dev \
                libradcli-dev zlib1g-dev libc-ares-dev
  ```

---

## 📦 Instalación

### 1️⃣ Preparación de Debian 13
Asegúrate de contar con conectividad y resolución de nombres adecuada en tu entorno de laboratorio:
```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 1.1.1.1" >> /etc/resolv.conf
```

### 2️⃣ Instalar Dependencias Actualizadas
Debian 13 incluye paquetes modernos por defecto. Ejecuta la instalación de dependencias necesarias para compilar `tac_plus-ng`:
```bash
apt update
apt install -y build-essential libssl-dev libpam0g-dev git perl \
              libpcre2-dev libcurl4-openssl-dev libldap2-dev \
              libradcli-dev zlib1g-dev libc-ares-dev
```

### 3️⃣ Descargar y Compilar
Clona el repositorio oficial de `event-driven-servers`, configúralo con el modificador `--minimum` y compílalo:
```bash
cd /tmp
git clone https://github.com/MarcJHuber/event-driven-servers.git
cd event-driven-servers
./configure --minimum
make
make install
```

### 4️⃣ Verificar Instalación
```bash
which tac_plus-ng
# Resultado esperado: /usr/local/sbin/tac_plus-ng

tac_plus-ng -v
# Muestra la versión compilada basada en PCRE2
```

---

## 📁 Creación de Estructura de Directorios y Logs
En Debian, el manejo de usuarios del sistema como `nobody` puede variar según la versión. Para evitar errores de permisos en los archivos de registro (`tac_plus.log`), estructuramos los directorios con permisos globales seguros:

```bash
mkdir -p /etc/tac_plus-ng
mkdir -p /var/log/tac_plus-ng
chmod 777 /var/log/tac_plus-ng
touch /var/log/tac_plus-ng/tac_plus.log
chmod 666 /var/log/tac_plus-ng/tac_plus.log
```

---

## ⚙️ Configuración

### 🔐 Nota Crítica: Clave Compartida (Shared Key)
- TACACS+ encripta **toda** la comunicación (usuario, contraseña y comandos ejecutados).
- La clave compartida debe ser **idéntica byte por byte** tanto en el servidor Debian como en el router Cisco.
- Si no coinciden, la autenticación fallará de manera silenciosa sin arrojar mensajes útiles en los logs.

### 1️⃣ Servidor TACACS+ (Debian 13)
Crea o edita el archivo de configuración en `/etc/tac_plus-ng/tac_plus-ng.cfg`:

```c
id = spawnd {
    background = no
    listen { port = 49 }
}

id = tac_plus-ng {    
    log = "/var/log/tac_plus-ng/tac_plus.log"
    
    host world {
        address = 0.0.0.0/0
        key = demo
    }

    profile admin {
        script {
            if (service == shell) {
                permit
            }
        }
    }    

    user test {
        password login = clear testpass
        password pap = login
        profile = admin
    }
}
```

#### Iniciar el Servidor en Background o Modo Debug
```bash
tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg &
```

#### Verificar que el puerto estándar esté escuchando (Puerto 49 IANA)
```bash
ss -tuln | grep 49
# Resultado esperado: tcp   LISTEN 0      128  *:49  *:*
```

---

### 2️⃣ Router Cisco (IOS 15)
Configura el modelo AAA, el servidor TACACS+ y el acceso segurizado en las líneas de consola y VTY:

```c
config t
!
aaa new-model
!
aaa authentication login TACACS_LOGIN group tacacs+ local
!
tacacs server TACACS-SERVER
  address ipv4 <IP-DEBIAN-13>
  key demo
exit
!
line vty 0 4
  login authentication TACACS_LOGIN
  transport input ssh telnet
exit
!
line con 0
  no login
exit
!
enable password cisco123
!
end
wr mem
```

> **⚠️ Nota de Seguridad:** Mantener `no login` en la consola física (`line con 0`) es un salvavidas crítico de emergencia ante fallas de red o caídas del servicio TACACS+.

---

## ✔️ Verificación y Pruebas Funcionales

1. **Verificar procesos y puertos en Debian:**
   ```bash
   ps aux | grep tac_plus-ng
   ss -tuln | grep 49
   ```
2. **Prueba de acceso vía Telnet/SSH:**
   ```bash
   telnet <IP-ROUTER>
   ```
   * **Username:** `test`
   * **Password:** `testpass`
   * *Resultado esperado:* Acceso exitoso al prompt del router (`Router>`).

---

## 🔧 Troubleshooting y Errores Comunes

- **Error: `% Authentication failed` en el Router**
  * **Causa principal:** Desalineación en la clave compartida (`key`). 
  * **Solución:** Valida con `grep "key = " /etc/tac_plus-ng/tac_plus-ng.cfg` en Debian y compárala con `show run | include tacacs` en el router. Deben coincidir exactamente.
- **Uso de contraseñas complejas:** Evita caracteres especiales (`@`, `#`, `!`) en los hashes de texto plano dentro de `tac_plus-ng.cfg` ya que pueden generar problemas en el parser del demonio. Utiliza cadenas alfanuméricas (`a-z`, `A-Z`, `0-9`).
- **Modo Debugging en Debian:** Si necesitas inspeccionar intentos de inicio de sesión fallidos, ejecuta el servidor interactivo con nivel de depuración alto:
  ```bash
  tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg -d 8
  ```

---

## 📚 Referencias
- [RFC 8907 - TACACS+ Protocol Specification](https://www.rfc-editor.org/rfc/rfc8907)
- [Repositorio Oficial tac_plus-ng (MarcJHuber)](https://github.com/MarcJHuber/event-driven-servers)
- [Cisco IOS AAA Configuration Guide](https://www.cisco.com/)