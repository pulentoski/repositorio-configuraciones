# Guía Completa: FreePBX 16 en VirtualBox

**Versión:** 3.0 (Final - Actualizada con instalación real)  
**Fecha:** Septiembre 2026  
**Para:** Alumnos de INACAP - Área Informática, Ciberseguridad y Telecomunicaciones  
**Instructor:** pulentoski (EscudoNorte)

---

## 1. Requisitos Previos

### Hardware mínimo recomendado:
- **CPU:** 2 núcleos (4 recomendado)
- **RAM:** 4 GB mínimo (preferible)
- **Disco duro:** 25 GB mínimo
- **Conexión de red:** Acceso a Internet

### Software requerido:
- **VirtualBox 6.1+** ([descargar](https://www.virtualbox.org/))
- **FreePBX 16 ISO:** `SNG7-PBX16-64bit-2306-1.iso` (1.7 GB)
- **Softphone SIP:** Linphone (para Linux/Ubuntu) o Zoiper (multiplataforma)

---

## 2. Descargar el ISO de FreePBX 16

1. Accede a [Sangoma FreePBX Downloads](https://downloads.freepbxdistro.org/ISO/)
2. Descarga: `SNG7-PBX16-64bit-2306-1.iso` (versión 2306 - junio 2023)
3. Verifica el checksum SHA256 si es posible

---

## 3. Crear la Máquina Virtual en VirtualBox

### 3.1 Nueva VM

1. Abre **VirtualBox**
2. Haz clic en **Nueva**
3. Completa con estos datos:

| Campo | Valor |
|-------|-------|
| **Nombre** | FreePBX16 |
| **Tipo** | Linux |
| **Versión** | CentOS / Red Hat (64-bit) |
| **Memoria RAM** | 4096 MB (4 GB) |
| **Disco duro** | Crear uno nuevo |
| **Tipo de disco** | VDI |
| **Almacenamiento** | Dinámico |
| **Tamaño** | **25 GB** |

### 3.2 Configuración de red (CRÍTICO)

1. **Configuración** → **Red**
2. **Adaptador 1:**
   - **Conectado a:** **NAT** ← OBLIGATORIO
   - **Nombre:** eth0

**⚠️ NAT es crítico para DHCP y acceso a Internet.**

### 3.3 Montar el ISO

1. **Configuración** → **Almacenamiento**
2. **Controlador IDE** → **Vacio**
3. Haz clic en el ícono del CD
4. **Seleccionar archivo** → Busca el ISO descargado
5. **Aceptar**

---

## 4. Instalación Automática de FreePBX 16

### 4.1 Inicia la VM

1. Haz doble clic en la VM o presiona **Iniciar**

### 4.2 Menú de arranque SNG0S 7

Se mostrará:
```
SNG0S 7

FreePBX 16 Installation (Asterisk 20) - Recommended
FreePBX 16 Installation (Asterisk 18)
...
```

**Selecciona:** `FreePBX 16 Installation (Asterisk 20)`

Presiona **Enter**.

### 4.3 Tipo de instalación gráfica

```
Graphical Installation - Output to VGA
Graphical Installation - Output to Serial
Graphical Installation - Output to UNC
```

**Selecciona:** `Graphical Installation - Output to VGA`

Presiona **Enter**.

### 4.4 Instalación automática vs avanzada

```
FreePBX Automatic Installation
FreePBX Advanced Installation
```

**Selecciona:** `FreePBX Automatic Installation` (recomendado)

Presiona **Enter**.

**Información:**
```
Automatic install of Asterisk 20 and FreePBX 16
Root password is set to 'SangomadDefaultPassword' (without quotes).
```

**La instalación arrancará automáticamente.**

**Tiempo estimado:** 15-25 minutos

Espera a que termine completamente.

### 4.5 Pantalla de finalización

Se mostrará:
```
Complete!

SNGOS is now successfully installed and ready for you to use!
Go ahead and reboot to start using it!
```

**Presiona el botón `Reboot`.**

La VM se reiniciará desde el disco duro.

---

## 5. Configuración Inicial del Panel Web

### 5.1 Panel de bienvenida

Cuando arranca, se abre automáticamente la **interfaz web** en:

```
https://192.168.0.3/admin/config.php
```

Se mostrará: **"Welcome to FreePBX Administration!"**

### 5.2 Setup inicial - Administrator User

**Formulario a completar:**

| Campo | Valor |
|-------|-------|
| **Username** | admin (defecto) |
| **Password** | (ingresa contraseña segura) |
| **Confirm Password** | (repite la contraseña) |
| **Notifications Email** | (opcional) |
| **System Identifier** | FreePBX16Lab (ej.) |

**Opciones de actualización:**
- **Automatic Module Updates:** Enabled
- **Automatic Security Updates:** Enabled
- **Send Security Emails:** Enabled
- **Check for Updates every:** Saturday Between 8am and 12pm

**Presiona:** `Setup System`

### 5.3 Seleccionar idioma y zona horaria

Se mostrará:
```
Please Select the default locales of the PBX
```

**Preselecciona:**
- **Sound Prompts Language:** Spanish
- **System Language:** Spanish (Spain)

**Presiona:** `Submit`

### 5.4 Sangoma Smart Firewall (Importante)

#### Pantalla 1: Introducción
```
Sangoma Smart Firewall is now enabled!
```

**Presiona:** `Continue`

#### Pantalla 2: ¿El cliente es de confianza?

```
Should the client you're using be trusted?
It is highly recommended that the client you're currently using 
(192.168.0.4/32) should be marked as Trusted.
```

**Presiona:** `Yes` (ya que accedes desde tu máquina)

#### Pantalla 3: ¿La red es de confianza?

```
Should your current network be trusted?
The network you are currently using (192.168.0.0/24) to manage 
this server isn't marked as Trusted.
```

**Presiona:** `Yes` (NAT privada es segura)

### 5.5 Dashboard Principal

Se abrirá el **Dashboard de FreePBX 16** mostrando:

- System Overview
- Asterisk version
- Call statistics
- System status
- Disk usage
- Uptime

**¡Instalación completada exitosamente!** ✅

---

## 6. IMPORTANTE: Cambiar la Contraseña de Root

**⚠️ PROBLEMA CONOCIDO:** La contraseña por defecto `SangomadDefaultPassword` **NO funciona** en la consola del sistema.

### 6.1 Resetear contraseña de root

Necesitas acceder por consola y cambiarla. **Opción A - Desde VirtualBox:**

1. Abre la **pantalla de la VM** (clic en la ventana de VirtualBox)
2. Presiona **Ctrl+Alt+F2** (cambiar a consola 2)
3. Intenta login:
   ```
   login: root
   Password: SangomadDefaultPassword
   ```

Si no funciona, necesitas resetear desde GRUB (ver **Troubleshooting**).

### 6.2 Una vez logueado

Cambia la contraseña:

```bash
passwd root
```

Ingresa una contraseña nueva (ej: `root@pbx123`)

Confirma y repite.

---

## 7. Crear Extensiones SIP (Anexos)

### 7.1 Acceder al panel de extensiones

En FreePBX:

1. **Admin** → **Applications** → **Extensions**
2. O busca en el menú izquierdo: **Extensions**
3. Selecciona la pestaña: **"SIP [chan_pjsip] Extensions"**

### 7.2 Crear primera extensión

**Haz clic en:** `+ Quick Create Extension`

Se abrirá el formulario **"Add PJSIP Extension":**

### 7.3 Completar formulario

| Campo | Valor |
|-------|-------|
| **User Extension** | 100 |
| **Display Name** | Alumno1 |
| **Secret** | (auto-generada) |
| **Username** | alumno1 |
| **Password For New User** | (auto-generada) |
| **Language Code** | Default |
| **Groups** | All Users |

**Campos opcionales (dejar vacíos):**
- Outbound CID
- Emergency CID

**Presiona:** `Submit`

### 7.4 Resultado

Se mostrará mensaje de éxito:
```
Extension 100 created successfully!
```

**Datos generados (IMPORTANTE - ANOTAR):**

```
Extension Number: 100
Display Name: Alumno1
Username: alumno1
Secret (Password): [generada automáticamente]
SIP Server: 192.168.0.3
Port: 5060
Protocol: PJSIP
```

### 7.5 Crear más extensiones

Repite el proceso con números diferentes:

- Extensión 101 → Alumno2
- Extensión 102 → Alumno3
- Extensión 103 → Alumno4

---

## 8. Configurar Softphone SIP (Linux/Ubuntu)

### 8.1 Instalar Linphone en Ubuntu

En una máquina Linux/Ubuntu:

```bash
sudo apt update
sudo apt install linphone
```

O descarga desde: [https://linphone.org/](https://linphone.org/)

### 8.2 Configurar cuenta SIP en Linphone

1. Abre **Linphone**
2. **Settings** (Configuración) → **Accounts** (Cuentas)
3. **Add Account** (Agregar cuenta)
4. **Server Selection:** SIP
5. Completa con datos de la extensión:

| Campo | Valor |
|-------|-------|
| **Username** | alumno1 |
| **Password** | [la generada en FreePBX] |
| **SIP Domain/Server** | 192.168.0.3 |
| **Port** | 5060 |

6. **Save** (Guardar)

### 8.3 Conectar y hacer llamadas

1. Linphone se conectará a FreePBX
2. Estado debe mostrar: **"Online"** o **"Connected"**
3. Ahora puedes:
   - Llamar a otras extensiones (ej: 101, 102)
   - Recibir llamadas
   - Configurar transferencias

---

## 9. Alternativas de Softphone

### Windows/Mac/Linux:
- **Zoiper:** [zoiper.com](https://zoiper.com) (pagado pero versión free disponible)
- **MicroSIP:** [microsip.org](http://microsip.org) (Windows)
- **X-Lite:** [counterpath.com](https://www.counterpath.com)

### Linux específicamente:
- **Linphone:** (Recomendado para educación)
- **Twinkle:** `sudo apt install twinkle`
- **PJSUA CLI:** `sudo apt install pjproject`

---

## 10. Troubleshooting

### Problema: No puedo acceder al panel web

**Solución:**
1. Verifica que la VM está encendida
2. Abre navegador: `https://192.168.0.3`
3. Acepta advertencia SSL (certificado autofirmado es normal)
4. Espera 3-5 minutos si recién bootea (FreePBX tarda en iniciar)

### Problema: Contraseña root no funciona

**Solución:**
1. Reinicia la VM
2. En GRUB, presiona `e` (editar)
3. Busca `linux16` o `linux` 
4. Agrega al final: `rd.break console=tty0`
5. Presiona **Ctrl+X**
6. En el prompt:
   ```bash
   mount -o remount,rw /sysroot
   chroot /sysroot
   passwd root
   ```
7. Ingresa nueva contraseña
8. `exit` y reinicia

### Problema: Extensión no se conecta desde Linphone

**Solución:**
1. Verifica que el `Secret` es correcto
2. Verifica que el **SIP Server** es la IP correcta (192.168.0.3)
3. Verifica el **Puerto: 5060**
4. En FreePBX, ve a **Connectivity** → **Trunks** y verifica estado

### Problema: Firewall bloqueó acceso web

**Solución:**
1. En FreePBX: **Connectivity** → **Firewall**
2. **Disable** o **Abort** el firewall
3. O abre puertos manualmente desde consola:
   ```bash
   ssh root@192.168.0.3
   systemctl stop firewalld
   ```

---

## 11. Próximos Pasos

Una vez configuradas las extensiones y Linphone:

1. **Hacer llamadas entre extensiones**
   - Extensión 100 llama a 101
   - Prueba bidireccional

2. **Configurar IVR (menú interactivo)**
   - **Applications** → **IVR**

3. **Crear colas de llamadas**
   - **Applications** → **Call Queues**

4. **Configurar voicemail**
   - **Applications** → **Voicemail**

5. **Agregar troncales SIP externos**
   - **Connectivity** → **Trunks**

---

## 12. Especificaciones Técnicas Finales

| Componente | Versión |
|-----------|---------|
| **FreePBX** | 16 (SNG7, 2306) |
| **Asterisk** | 20 LTS |
| **SO** | CentOS 7 |
| **MySQL** | MariaDB |
| **PHP** | 5.6+ |
| **Protocolo SIP** | PJSIP (moderno) |
| **Firewall** | Sangoma Smart Firewall (desactívalo si molesta) |

**Credenciales por defecto:**
```
Root (Cambiar obligatorio):
Usuario: root
Contraseña: SangomadDefaultPassword [NO FUNCIONA - CAMBIAR]

Admin web:
Usuario: admin
Contraseña: [la que estableciste en setup]
```

---

## 13. Contacto y Soporte

**Instructor:** pulentoski  
**Consultancy:** [EscudoNorte](https://escudonorte.cl)  
**Email:** pulentoski@escudonorte.cl

---

**Última actualización:** Septiembre 2026  
**Nivel:** Principiante  
**Tiempo total:** 40-50 minutos (instalación + configuración)  
**Dificultad:** Baja-Media
