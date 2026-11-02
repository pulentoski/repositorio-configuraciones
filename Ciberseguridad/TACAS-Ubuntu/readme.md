# 🔐 TACACS+ Server (tac_plus-ng) - Cisco IOS 15 Integration con SSH

Autenticación centralizada RFC 8907 para routers Cisco usando tac_plus-ng en Ubuntu 24.04 LTS, con acceso remoto exclusivamente por SSHv2.

![License](https://img.shields.io/badge/license-MIT%2FGPL-blue) ![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-orange) ![IOS](https://img.shields.io/badge/Cisco%20IOS-15.9-green) ![SSH](https://img.shields.io/badge/SSH-v2-black)

---

## 📋 Contenido

- [Resumen](#-resumen)
- [Requisitos](#️-requisitos)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Verificación](#️-verificación)
- [Troubleshooting](#-troubleshooting)
- [Limitaciones Conocidas](#️-limitaciones-conocidas)
- [Lecciones Aprendidas](#-lecciones-aprendidas)
- [Para Docentes](#-para-docentes)
- [Referencias](#-referencias)

---

## 📖 Resumen

Implementación de un servidor TACACS+ basado en **tac_plus-ng** (fork moderno y mantenido, compatible con RFC 8907) para autenticar por **SSHv2** a los usuarios de routers Cisco IOS 15.9.

### ✨ Características Implementadas

- ✅ Acceso remoto solo por SSHv2 (Telnet deshabilitado)
- ✅ Autenticación centralizada contra servidor TACACS+ remoto
- ✅ Fallback a usuario local si el servidor no responde
- ✅ Acceso por consola sin autenticación (seguridad física)
- ✅ Cifrado del payload TACACS+ con clave compartida
- ✅ Compatible con RFC 8907
- ✅ Compilación desde código fuente

### ❌ No Implementado (Opcional)

- Logging en archivo (la configuración está presente, pero tac_plus-ng no escribe logs)
- Enable con TACACS+
- Backend LDAP/Active Directory
- TLS 1.3 (RFC 9887)
- MFA

---

## 🖥️ Requisitos

### Hardware

- **Servidor Ubuntu:** 1 vCPU, 512 MB RAM, 2 GB disco (mínimo)
- **Router Cisco:** IOS 15.x o superior, con imagen que soporte crypto (k9)
- **Red:** conectividad L3 entre ambos (TCP 49 para TACACS+, TCP 22 para SSH)

### Software

- **Ubuntu:** 24.04 LTS o similar Debian-based
- **Cisco IOS:** 15.9 (probado)
- **Cliente SSH:** OpenSSH (incluido en Ubuntu)

### Librerías de compilación

```
build-essential libssl-dev libpam0g-dev libpcre2-dev libcurl4-openssl-dev
libldap2-dev libradcli-dev zlib1g-dev libc-ares-dev
```

---

## 📦 Instalación

### 1️⃣ Preparar Ubuntu

#### ⚠️ 1.1 Configurar DNS (obligatorio, primer paso)

Sin DNS, `apt` y `git` fallan.

```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 1.1.1.1" >> /etc/resolv.conf
cat /etc/resolv.conf
```

> 💡 En CML y VirtualBox, `systemd-resolved` puede quedar apuntando solo a `127.0.0.53` sin servidores reales.
> Síntoma: `Temporary failure resolving 'archive.ubuntu.com'`

#### 1.2 Instalar dependencias

```bash
apt update
apt install -y build-essential libssl-dev libpam0g-dev git perl \
              libpcre2-dev libcurl4-openssl-dev libldap2-dev \
              libradcli-dev zlib1g-dev libc-ares-dev
```

#### 1.3 Descargar y compilar

```bash
cd /tmp
git clone https://github.com/MarcJHuber/event-driven-servers.git
cd event-driven-servers
./configure --minimum
make
make install
```

#### 1.4 Verificar instalación

```bash
which tac_plus-ng
# /usr/local/sbin/tac_plus-ng

tac_plus-ng -v
# tac_plus-ng version fd4818b7.../PCRE2
```

### 2️⃣ Crear estructura de directorios

```bash
mkdir -p /etc/tac_plus-ng
mkdir -p /var/log/tac_plus-ng
chmod 777 /var/log/tac_plus-ng
touch /var/log/tac_plus-ng/tac_plus.log
chmod 666 /var/log/tac_plus-ng/tac_plus.log
```

---

## ⚙️ Configuración

### 🔑 Nota Crítica: Clave Compartida

- TACACS+ cifra el payload completo (usuario, contraseña, comandos) con la clave.
- La clave debe ser **idéntica** en el servidor y en el router.
- Si no coinciden, la autenticación falla sin mensajes útiles.

```bash
# Ubuntu
grep "key = " /etc/tac_plus-ng/tac_plus-ng.cfg
```
```
! Router
show run | section tacacs
```

---

### 1️⃣ Servidor TACACS+ (Ubuntu)

**Archivo:** `/etc/tac_plus-ng/tac_plus-ng.cfg`

```
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

> ⚠️ El ejemplo de tac_plus-ng usa el puerto 4949. El estándar IANA para TACACS+ es **TCP 49**, que es lo que Cisco espera por defecto.

#### Iniciar servidor

```bash
tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg &
```

#### Verificar puerto

```bash
ss -tuln | grep 49
# tcp   LISTEN 0   128   *:49   *:*
```

---

### 2️⃣ Router Cisco (IOS 15) — Paso a Paso

#### 2.1 Conectividad previa

```
ping 10.10.10.2
! !!!!! (5/5 100%)
```

#### 2.2 Identidad del equipo y enable

```
configure terminal
 hostname RT-1
 ip domain-name lab.local
 enable secret cisco123
```

| Comando | Función |
|---|---|
| `hostname RT-1` | Cambia el nombre por defecto. Es obligatorio para generar las claves RSA. |
| `ip domain-name lab.local` | Dominio usado para nombrar las claves RSA. |
| `enable secret cisco123` | Contraseña de modo privilegiado, almacenada como hash. |

#### 2.3 Usuario local de respaldo

```
 username admin privilege 15 secret Admin123
```

> ⚠️ El método `local` del fallback usa **esta** base de usuarios, no el `enable secret`. Sin un usuario local, si TACACS+ cae, nadie puede entrar por SSH.

#### 2.4 Claves RSA y SSHv2

```
 crypto key generate rsa general-keys modulus 2048
 ip ssh version 2
 ip ssh time-out 60
 ip ssh authentication-retries 3
```

| Comando | Función |
|---|---|
| `crypto key generate rsa ... modulus 2048` | Genera las claves del servidor SSH. SSHv2 requiere 768 bits como mínimo. |
| `ip ssh version 2` | Desactiva SSHv1. Debe ir después de generar las claves. |
| `ip ssh time-out 60` | Tiempo máximo (en segundos) para autenticarse. |
| `ip ssh authentication-retries 3` | Intentos permitidos por conexión. |

#### 2.5 AAA y servidor TACACS+

```
 aaa new-model
 aaa authentication login TACACS_LOGIN group tacacs+ local
 !
 tacacs server TACACS-SERVER
  address ipv4 10.10.10.2
  key demo
 exit
```

| Comando | Función |
|---|---|
| `aaa new-model` | Activa el framework AAA. |
| `aaa authentication login TACACS_LOGIN group tacacs+ local` | Lista de métodos: primero TACACS+ y, si no responde, usuarios locales. |
| `tacacs server` | Define la IP y la clave del servidor. |

#### 2.6 Líneas VTY solo SSH

```
 line vty 0 4
  login authentication TACACS_LOGIN
  transport input ssh
  exec-timeout 5 0
 exit
```

#### 2.7 Consola

```
 line con 0
  no login
 exit
end
write memory
```

> ⚠️ `no login` en consola es el acceso de emergencia si TACACS+ o la red fallan. Su protección es física (sala y rack con llave), no AAA.

#### 2.8 Configuración completa

```
configure terminal
 hostname RT-1
 ip domain-name lab.local
 enable secret cisco123
 username admin privilege 15 secret Admin123
 crypto key generate rsa general-keys modulus 2048
 ip ssh version 2
 ip ssh time-out 60
 ip ssh authentication-retries 3
 !
 aaa new-model
 aaa authentication login TACACS_LOGIN group tacacs+ local
 !
 tacacs server TACACS-SERVER
  address ipv4 10.10.10.2
  key demo
 exit
 !
 line vty 0 4
  login authentication TACACS_LOGIN
  transport input ssh
  exec-timeout 5 0
 exit
 !
 line con 0
  no login
 exit
end
write memory
```

---

## ✔️ Verificación

### 1️⃣ Ubuntu — Servidor activo

```bash
ps aux | grep tac_plus-ng
ss -tuln | grep 49
```

### 2️⃣ Router — SSH y AAA

```
show ip ssh
! SSH Enabled - version 2.0

show run | include aaa
! aaa new-model
! aaa authentication login TACACS_LOGIN group tacacs+ local

show run | section tacacs
! tacacs server TACACS-SERVER
!  address ipv4 10.10.10.2
!  key demo

show run | section line vty
! login authentication TACACS_LOGIN
! transport input ssh

show tacacs
! Muestra conexiones, paquetes enviados/recibidos y estado del servidor
```

### 3️⃣ Prueba funcional — Login SSH con TACACS+

Desde Ubuntu u otra máquina:

```bash
ssh test@10.10.10.1
# Password: testpass
# RT-1>
```

> ⚠️ Si OpenSSH rechaza la conexión por algoritmos, revise [Troubleshooting](#-no-matching-key-exchange--host-key-type-ssh).

### 4️⃣ Prueba funcional — Enable

```
RT-1>enable
Password: cisco123
RT-1#
```

### 5️⃣ Prueba de fallback local

```bash
# Ubuntu: detener TACACS+
killall tac_plus-ng
```
```bash
ssh admin@10.10.10.1
# Password: Admin123  → acceso con usuario local
```

### 6️⃣ Confirmar que Telnet está bloqueado

```bash
telnet 10.10.10.1
# Connection refused / cierre inmediato
```

---

## 🔧 Troubleshooting

### ❌ "no matching key exchange / host key type" (SSH)

**Síntoma:**

```
Unable to negotiate with 10.10.10.1 port 22: no matching key exchange method found.
Their offer: diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1
```

**Causa:** OpenSSH 9.x (Ubuntu 24.04) deshabilita por defecto los algoritmos SHA-1 que usa IOS 15.9.

**Solución (por conexión):**

```bash
ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 \
    -o HostKeyAlgorithms=+ssh-rsa \
    -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    test@10.10.10.1
```

**Solución (permanente, solo para el lab):** `~/.ssh/config`

```
Host 10.10.10.1
    KexAlgorithms +diffie-hellman-group14-sha1
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
```

> 💡 Es una excepción para equipos legacy. No debe aplicarse globalmente.

---

### ❌ "Connection refused" en puerto 22

**Causa:** SSH no está habilitado en el router.

```
show ip ssh
```

| Salida | Causa | Solución |
|---|---|---|
| `SSH Disabled` | No hay claves RSA | `crypto key generate rsa general-keys modulus 2048` |
| `version 1.99` | Falta forzar v2 | `ip ssh version 2` |
| `ip ssh version 2` da error | Claves de 512 bits | Regenerar con `modulus 2048` |
| `Please define a hostname other than Router` | Hostname por defecto | `hostname RT-1` |

También verifique que `line vty` tenga `transport input ssh`.

---

### ❌ "Authentication failed" (caso más común)

**Causa raíz (90 %):** la clave compartida es distinta en el router y en el servidor.

```bash
# Ubuntu
grep "key = " /etc/tac_plus-ng/tac_plus-ng.cfg
```
```
! Router
show run | section tacacs
```

**Sincronizar (opción router):**

```
configure terminal
 tacacs server TACACS-SERVER
  key demo
end
```

**Sincronizar (opción Ubuntu):**

```bash
sed -i 's/key = cisco/key = demo/g' /etc/tac_plus-ng/tac_plus-ng.cfg
killall tac_plus-ng
tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg &
```

---

### ❌ Usuario TACACS+ rechazado, pero el usuario local funciona

**Causa:** TACACS+ no responde y el router está usando el fallback local.

```
! Router
ping 10.10.10.2
show tacacs
```
```bash
# Ubuntu
ps aux | grep tac_plus-ng
ss -tuln | grep 49
grep "user test" /etc/tac_plus-ng/tac_plus-ng.cfg
```

---

### ❌ Usuario "test" no existe

```bash
cat >> /etc/tac_plus-ng/tac_plus-ng.cfg << 'EOF'

    user test {
        password login = clear testpass
        password pap = login
        profile = admin
    }
EOF
killall tac_plus-ng
tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg &
```

> ⚠️ El bloque `user` debe quedar **dentro** de `id = tac_plus-ng { ... }`. Si se agrega con `>>` al final del archivo, queda fuera. Edite con `nano` si es necesario.

---

### ⚠️ Contraseña correcta, pero falla

**Causa:** caracteres especiales (`@`, `#`, `!`) en la contraseña del servidor.

```
# ❌ password login = clear Pass@123
# ✅ password login = clear Passw0rd123
```

---

### ❌ Consola del router bloqueada

**Causa:** consola con autenticación AAA y sin usuario local.

```
# CML: Right-click → Stop → Wipe → Start
line con 0
 no login
```

---

## ⚠️ Limitaciones Conocidas

1. **Enable no autentica con TACACS+** en este lab. Workaround: `enable secret` local.
2. **Logs no se escriben en archivo.** Workaround: modo debug.
   ```bash
   tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg -d 8
   ```
3. **Caracteres especiales en passwords:** use solo `a-z A-Z 0-9 _ -`.
4. **Usuario `nobody:nobody`** no existe en algunos Ubuntu. Workaround: `chmod 777` en el directorio de logs.
5. **Algoritmos SSH legacy** en IOS 15.9: requieren habilitar SHA-1 en el cliente OpenSSH.

---

## 🔀 Comparación: TACACS+ vs Alternativas

| Aspecto | TACACS+ | RADIUS | SSH Keys locales |
|---|---|---|---|
| Protocolo | RFC 8907, TCP 49 | RFC 2865, UDP 1812/1813 | SSH |
| Cifrado | Payload completo | Solo el password | Asimétrico |
| Separación AAA | Authn / Authz / Acct separados | Authn + Authz combinados | Solo authn |
| Accounting por comando | ✅ | Básico | ❌ |
| Uso típico | Administración de equipos | VPN, WiFi, 802.1X | Pocos equipos |

**Regla:** TACACS+ para administración de equipos de red; RADIUS para acceso de usuarios a la red.

---

## 🎓 Flujo de Autenticación SSH + TACACS+

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USUARIO ABRE SESIÓN SSH                                  │
│    $ ssh test@10.10.10.1                                    │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. NEGOCIACIÓN SSHv2 (TCP 22)                               │
│    - Intercambio de claves (Diffie-Hellman)                 │
│    - Router presenta su clave RSA de host                   │
│    - Se establece el túnel cifrado cliente ↔ router         │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. USUARIO ENVÍA CREDENCIALES DENTRO DEL TÚNEL SSH          │
│    test / testpass                                          │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ROUTER APLICA LISTA TACACS_LOGIN                         │
│    Método 1: group tacacs+                                  │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. ROUTER → SERVIDOR (TCP 49)                               │
│    Payload TACACS+ cifrado con clave "demo"                 │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. SERVIDOR DESCIFRA Y VALIDA                               │
│    ✓ Clave coincide → busca usuario → compara password      │
│    ✗ Clave no coincide → datos ilegibles → falla            │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. RESPUESTA EN LA MISMA SESIÓN TCP 49                      │
│    PASS o FAIL (cifrado con la misma clave)                 │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. RESULTADO EN EL ROUTER                                   │
│    ✓ PASS    → RT-1>                                        │
│    ✗ FAIL    → "Authentication failed" (sin fallback)       │
│    ✗ TIMEOUT → Método 2: local (username admin)             │
└─────────────────────────────────────────────────────────────┘
```

### Puntos críticos

- **Dos capas de cifrado:** SSH protege el tramo usuario ↔ router; la clave TACACS+ protege el tramo router ↔ servidor.
- **El fallback local solo actúa si el servidor no responde.** Un FAIL explícito no pasa al método local.
- **TACACS+ no informa la causa del rechazo.** No dice "usuario no existe" ni "password incorrecto", para no revelar usuarios válidos.

### Estrategia de debugging

```
Si falla el login:
  1. ¿SSH responde?         → show ip ssh / ssh -v
  2. ¿Clave idéntica?       → comparar ambos lados
  3. ¿Usuario existe?       → grep "user" en la config
  4. ¿Servidor responde?    → ping + ps aux + ss -tuln + show tacacs
  5. ¿Caracteres especiales? → usar solo alfanuméricos
```

---

## 📚 Lecciones Aprendidas

1. **DNS primero:** sin DNS no hay `apt` ni `git`.
2. **Clave compartida idéntica:** es la causa de la mayoría de las fallas.
3. **IOS 15 soporta TACACS+:** debuggee la configuración antes de culpar a la versión.
4. **La consola es el último recurso:** `no login` más protección física.
5. **Puerto 49:** es el estándar IANA. El 4949 del ejemplo no lo es.
6. **El fallback local requiere un usuario local:** `enable secret` no reemplaza a `username`.
7. **IOS legacy vs OpenSSH moderno:** los algoritmos SHA-1 deben habilitarse explícitamente en el cliente.
8. **Los logs de tac_plus-ng son escasos:** use `-d 8` y debuggee por capas.

---

## 👨‍🎓 Para Docentes

### Objetivos de Aprendizaje

- ✅ Compilar e instalar tac_plus-ng desde código fuente
- ✅ Configurar SSHv2 en Cisco IOS
- ✅ Implementar AAA con TACACS+ y fallback local
- ✅ Debuggear autenticación centralizada por capas
- ✅ Diferenciar TACACS+, RADIUS y claves SSH

### 🟢 Nivel Básico

**Verificar instalación y SSH**

```bash
which tac_plus-ng && tac_plus-ng -v
ss -tuln | grep 49
```
```
show ip ssh
```

**Agregar usuario `alice`** (dentro del bloque `tac_plus-ng`):

```
user alice {
    password login = clear Alice123
    password pap = login
    profile = admin
}
```

Reinicie el servidor y pruebe con `ssh alice@10.10.10.1`.

**Cambiar enable secret**

```
configure terminal
 enable secret NewPassword123
end
write memory
```

### 🟡 Nivel Intermedio

**Cambiar la clave compartida en ambos lados**

```bash
sed -i 's/key = demo/key = mycluster123/g' /etc/tac_plus-ng/tac_plus-ng.cfg
killall tac_plus-ng
tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg &
```
```
configure terminal
 tacacs server TACACS-SERVER
  key mycluster123
end
write memory
```

**Simular caída de TACACS+ y observar el fallback**

```bash
killall tac_plus-ng
ssh admin@10.10.10.1   # debe entrar con usuario local
ssh test@10.10.10.1    # debe fallar
```

**Clave incorrecta deliberada:** cambie la clave solo en Ubuntu, intente el login con `test` y pida al alumno que encuentre la causa.

**Verificar que Telnet está bloqueado:** `telnet 10.10.10.1` debe fallar. Explicar por qué.

### 🔴 Nivel Avanzado

**Diagnóstico sin logs.** Entregue escenarios rotos:

1. Clave distinta
2. Servidor detenido
3. Usuario inexistente
4. Password con `@`
5. Router sin claves RSA
6. VTY con `transport input telnet`

Herramientas permitidas: `ping`, `grep`, `ss`, `show ip ssh`, `show tacacs`, `ssh -v`.

**Captura de tráfico.** Capture con Wireshark los tramos TCP 22 y TCP 49. ¿Qué se ve en cada uno? ¿Qué cambiaría con Telnet?

**Diseño a producción:**

- 3 routers y 1 servidor TACACS+ (¿y redundancia?)
- Perfiles: admin, operator, tech-support
- ¿Cómo se maneja la caída del servidor?
- ¿Cómo se rotan claves y contraseñas?

---

## ✅ Checklist de Verificación

### Servidor Ubuntu

- [ ] DNS configurado: `grep nameserver /etc/resolv.conf`
- [ ] tac_plus-ng instalado: `which tac_plus-ng && tac_plus-ng -v`
- [ ] Proceso corriendo: `ps aux | grep tac_plus-ng`
- [ ] Puerto 49 escuchando: `ss -tuln | grep 49`
- [ ] Usuario definido: `grep "user test" /etc/tac_plus-ng/tac_plus-ng.cfg`
- [ ] Clave configurada: `grep "key = " /etc/tac_plus-ng/tac_plus-ng.cfg`

### Router Cisco

- [ ] Ping al servidor: `ping 10.10.10.2`
- [ ] Hostname y dominio: `show run | include hostname|domain`
- [ ] SSH v2 activo: `show ip ssh` → `version 2.0`
- [ ] Usuario local de respaldo: `show run | include username`
- [ ] AAA habilitado: `show run | include aaa`
- [ ] Servidor TACACS+: `show run | section tacacs`
- [ ] VTY solo SSH: `show run | section line vty`
- [ ] Consola sin login AAA: `show run | section line con`

### Prueba Funcional

- [ ] `ssh test@10.10.10.1` → `RT-1>`
- [ ] `enable` → `RT-1#`
- [ ] Fallback: con el servidor detenido, `ssh admin@10.10.10.1` funciona
- [ ] `telnet 10.10.10.1` es rechazado

---

## 📋 Especificaciones de Lab

| Componente | Valor |
|---|---|
| Ubuntu | 24.04.4 LTS, kernel 6.8, x86_64 |
| Router | Cisco IOSv 15.9 |
| Plataforma | CML 2.0 |
| Ubuntu IP | 10.10.10.2/24 |
| Router IP | 10.10.10.1/24 |
| TACACS+ | TCP 49 |
| SSH | TCP 22, v2 |
| Shared key | `demo` |
| Usuario TACACS+ | `test` / `testpass` |
| Usuario local | `admin` / `Admin123` |
| Enable secret | `cisco123` |

---

## 📖 Referencias

| Documento | Enlace |
|---|---|
| RFC 8907 (TACACS+) | https://www.rfc-editor.org/rfc/rfc8907 |
| RFC 9887 (TACACS+ sobre TLS 1.3) | https://www.rfc-editor.org/rfc/rfc9887 |
| RFC 4253 (SSH Transport) | https://www.rfc-editor.org/rfc/rfc4253 |
| tac_plus-ng | https://github.com/MarcJHuber/event-driven-servers |
| Cisco AAA | https://www.cisco.com/c/en/us/support/docs/security/ios-aaa/ |
| IANA Ports | https://www.iana.org/assignments/service-names-port-numbers/ |

---

## 📄 Licencia

Este proyecto utiliza software bajo licencias MIT y GPL. Ver `LICENSE`.

## ✍️ Autor

**Daniel "pulentoski" Soto**
🏢 Docente — INACAP La Serena | Área de Informática, Ciberseguridad y Telecomunicaciones
💼 Co-founder — EscudoNorte (Cybersecurity & Compliance Consultancy)
📍 Región de Coquimbo, Chile
