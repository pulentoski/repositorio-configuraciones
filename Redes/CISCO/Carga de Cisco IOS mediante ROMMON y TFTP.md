# 🌐 Carga de Cisco IOS mediante ROMMON y TFTP

## 📌 Descripción

Procedimiento para instalar o recuperar una imagen Cisco IOS (`.bin`) utilizando el modo ROMMON y un servidor TFTP alojado en un computador.

⚠️ Este procedimiento elimina completamente el contenido actual de la memoria flash del router.

---

# 📌 Concepto

El modo ROMMON no puede leer archivos directamente desde el PC.

Por ello, el computador debe actuar como un servidor TFTP temporal para compartir la imagen IOS.

Flujo:

```plaintext
PC con TFTP  --->  Router Cisco
```

---

# Requisitos

- Cable consola.
- Cable Ethernet.
- Imagen IOS `.bin`.
- Software TFTP.
- Conectividad entre el PC y el router.

---

# Software TFTP Recomendado

## Windows

- Tftpd64
- Tftpd32
- SolarWinds TFTP Server

---

# Paso 1: Configurar el Servidor TFTP

Crear carpeta TFTP:

```plaintext
C:\TFTP-Root\
```

Copiar la imagen IOS dentro de la carpeta:

```plaintext
2600.bin
```

---

# Paso 2: Configurar IP del PC

Ejemplo:

| Dispositivo | Dirección IP |
|---|---|
| PC TFTP | `192.168.20.100` |
| Router Cisco | `192.168.20.1` |

---

# Paso 3: Conectar Router y PC

Opciones:

- Cable Ethernet directo.
- Switch intermedio.

---

# Paso 4: Ingresar a ROMMON

Reiniciar el router e interrumpir el arranque.

## Combinaciones Break

| Software | Combinación |
|---|---|
| PuTTY / Tera Term / HyperTerminal | `Ctrl + Break` |
| Laptop sin Break | `Fn + Pause/Break` |
| SecureCRT | `Ctrl + Shift + 6` luego `b` |
| Minicom | `Ctrl + A` luego `F` |
| macOS screen | `Ctrl + A` luego `Ctrl + \` |

Prompt esperado:

```plaintext
rommon 1 >
```

---

# Paso 5: Configurar Parámetros de Red

```plaintext
rommon 1 > IP_ADDRESS=192.168.20.1
rommon 2 > IP_SUBNET_MASK=255.255.255.0
rommon 3 > DEFAULT_GATEWAY=192.168.20.100
rommon 4 > TFTP_SERVER=192.168.20.100
rommon 5 > TFTP_FILE=2600.bin
```

---

# Paso 6: Descargar la IOS

```plaintext
rommon 6 > tftpdnld
```

El router mostrará:

```plaintext
IP ADDRESS: 192.168.20.1
IP SUBNET MASK: 255.255.255.0
DEFAULT GATEWAY: 192.168.20.100
TFTP SERVER: 192.168.20.100
TFTP FILE: 2600.bin
```

---

# Paso 7: Confirmar Instalación

```plaintext
Invoke this command for disaster recovery only.
WARNING: all existing data in all partitions on flash will be lost!
Do you wish to continue? y/n:
```

Responder:

```plaintext
y
```

---

# Paso 8: Esperar la Transferencia

El router:

- Descargará la IOS desde el PC.
- Borrará la memoria flash.
- Instalará la nueva imagen.

⚠️ No apagar el equipo durante el proceso.

---

# Paso 9: Reiniciar el Router

```plaintext
rommon > reset
```

o

```plaintext
rommon > boot
```

---

# ✅ Resultado

El router iniciará utilizando la nueva imagen IOS instalada desde el servidor TFTP del computador.

---

# 📌 Comando Utilizado

## `tftpdnld`

Permite descargar una imagen IOS desde un servidor TFTP directamente a la memoria flash del router utilizando ROMMON.

Uso común:

- IOS corrupta.
- Flash vacía.
- Recuperación de desastres.
- Restauración manual de IOS.

---
