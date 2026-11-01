# Guía de Instalación del Switch Capa 3 (vIOS-L2) en GNS3

Esta guía detalla los pasos para importar, configurar y desplegar una imagen de **Switch Cisco Multicapa (Capa 3) / vIOS-L2** en el simulador de red **GNS3**.

---

## 1. Introducción y Requisitos

Para practicar características avanzadas de Capa 2 y Capa 3 (Seguridad L2, VLANs, Troncales, EtherChannel, SVI, DHCP Snooping, Enrutamiento Inter-VLAN), se utiliza la imagen virtualizada oficial de Cisco **vIOS-L2** (Virtual IOS Layer 2).

### Información de la Imagen Utilizada

* **Nombre del archivo:** `vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E`
* **Tamaño:** ~96,9 MB
* **Formato de disco:** Virtual Machine Disk (`.vmdk`)
* **Versión de IOS:** 15.2(4)0.55.E
* **Enlace de referencia de descarga:** [https://upw.io/75g/vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E](https://upw.io/75g/vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E)

### Entorno probado

| Componente | Valor |
| :--- | :--- |
| Sistema anfitrión | Linux (Ubuntu) |
| Binario QEMU | `/bin/qemu-system-x86_64` (v8.2.2) |
| Ubicación de la imagen | `~/Documentos/ios/` |
| Servidor | Local (sin GNS3 VM) |

---

## 2. Métodos de Instalación en GNS3

Existen dos opciones principales para agregar este switch en GNS3:
1. **Método A:** Importando el archivo de plantilla `.gns3a` (Appliance).
2. **Método B (usado en este lab):** Creando un nuevo nodo QEMU manualmente.

---

### Método A: Instalación Automática mediante Appliance (`.gns3a`)

1. **Descargar la plantilla:**
   * Ve a la web oficial de GNS3 Marketplace y descarga la plantilla **Cisco vIOS-L2** (`cisco-vios-l2.gns3a`).
2. **Importar en GNS3:**
   * Abre GNS3.
   * Ve a **File** → **Import appliance**.
   * Selecciona el archivo `cisco-vios-l2.gns3a` descargado.
3. **Selección del Servidor:**
   * Selecciona ejecutar el appliance en la **GNS3 VM** (recomendado para rendimiento QEMU) o en el servidor local si tu equipo es Linux.
4. **Asociación del Archivo `.vmdk`:**
   * En la lista de versiones, busca la versión correspondiente o haz clic en **Import**.
   * Selecciona el archivo `vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E`.
   * El sistema verificará el archivo y procederá con la instalación.
5. **Finalización:**
   * Haz clic en **Next** hasta finalizar. El switch aparecerá disponible en el panel izquierdo bajo el icono de Switches.

---

### Método B: Instalación Manual como QEMU VM

#### Paso 1 — Crear la plantilla

1. Ve a **Edit** → **Preferences** (`Ctrl + Shift + P`).
2. En el menú lateral, ve a **QEMU** → **Qemu VMs** y haz clic en **New**.

#### Paso 2 — Nombre de la VM

* **Name:** `SW-CAPA-3-CISCO`
* **This is a legacy ASA VM:** sin marcar.

#### Paso 3 — Binario QEMU y memoria

* **Qemu binary:** `/bin/qemu-system-x86_64 (v8.2.2)`
* **RAM:** `512 MB`

#### Paso 4 — Tipo de consola

* **Console type:** `telnet`

#### Paso 5 — Imagen de disco

* Selecciona **New Image** → **Browse...**
* Busca el archivo en `~/Documentos/ios/vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E`.
* Haz clic en **Finish**.

> GNS3 puede preguntar si copiar la imagen al directorio de imágenes por defecto. Se recomienda aceptar.

---

#### Paso 6 — Editar la plantilla

Selecciona `SW-CAPA-3-CISCO` en la lista y haz clic en **Edit**.

##### Pestaña General settings

| Campo | Valor |
| :--- | :--- |
| Template name | `SW-CAPA-3-CISCO` |
| Default name format | `{name}-{0}` |
| Symbol | `:/symbols/qemu_guest.svg` (opcional: `multilayer_switch.svg`) |
| Category | `Switches` |
| RAM | `512 MB` |
| vCPUs | `1` |
| Qemu binary | `/bin/qemu-system-x86_64 (v8.2.2)` |
| Boot priority | `HDD` |
| On close | `Power off the VM` |
| Console type | `telnet` |

##### Pestaña Network

| Campo | Valor |
| :--- | :--- |
| Adapters | `8` |
| First port name | *(vacío)* |
| Name format | `Ethernet{0}` (ver nota) |
| Segment size | `0` |
| Type | `Intel Gigabit Ethernet (e1000)` |
| Replicate network connection states in Qemu | ✅ |
| Use the legacy networking mode | ❌ |

> **Nota sobre nombres de interfaz:** el *Name format* solo cambia la etiqueta que muestra GNS3, no el nombre dentro del IOS. vIOS-L2 agrupa los puertos de a 4 (`Gi0/0`–`Gi0/3`, `Gi1/0`–`Gi1/3`). Para que las etiquetas de GNS3 coincidan con el IOS, usa:
> * **Name format:** `Gi{1}/{0}`
> * **Segment size:** `4`

##### Pestaña Advanced

| Campo | Valor |
| :--- | :--- |
| Options | `-no-kvm` |
| Use as a linked base VM | ✅ |
| Activate CPU throttling | ❌ |
| Process priority | `Normal` |
| TPM / UEFI | ❌ |

> **Sobre `-no-kvm`:** desactiva la aceleración por hardware (KVM) y usa emulación TCG. Es necesario cuando el anfitrión no tiene KVM disponible (virtualización deshabilitada en BIOS, o GNS3 corriendo dentro de otra VM). El switch funciona, pero el arranque es más lento (varios minutos). Si tu equipo soporta KVM (`kvm-ok` o `ls /dev/kvm`), elimina esta opción.

Haz clic en **Apply** y **OK**.

---

## 3. Primer Inicio y Verificación

1. Arrastra el nodo **SW-CAPA-3-CISCO** desde la categoría Switches al lienzo.
2. Clic derecho sobre el nodo → **Start**.
3. Doble clic para abrir la consola Telnet. Espera a que termine el arranque (con `-no-kvm` puede tardar bastante).

### Comandos de Verificación en la Consola Cisco IOS

#### 1. Verificar Versión e Imagen del IOS
```text
Switch# show version
```
*Debe mostrar la versión `15.2` y la plataforma `vIOS-L2`.*

#### 2. Verificar Interfaces Disponibles
```text
Switch# show ip interface brief
```
*Con 8 adaptadores se verán `Gi0/0`–`Gi0/3` y `Gi1/0`–`Gi1/3`.*

#### 3. Habilitar Enrutamiento IP (Capa 3)
```text
Switch# configure terminal
Switch(config)# ip routing
```

#### 4. Probar Creación de VLANs e Interfaz SVI
```text
Switch(config)# vlan 10
Switch(config-vlan)# name VENTAS
Switch(config-vlan)# exit

Switch(config)# interface vlan 10
Switch(config-if)# ip address 192.168.10.1 255.255.255.0
Switch(config-if)# no shutdown
```
*La SVI quedará `up/up` solo cuando al menos un puerto activo pertenezca a la VLAN 10.*

#### 5. Verificar la Tabla de Enrutamiento
```text
Switch# show ip route
```

---

## 4. Solución de Problemas Comunes

| Problema | Causa Probable | Solución |
| :--- | :--- | :--- |
| **El switch no arranca o entra en bucle de reinicio** | RAM insuficiente. | Subir la RAM a 768 MB o 1024 MB en **General settings**. |
| **Arranque extremadamente lento** | Uso de `-no-kvm` (emulación sin aceleración). | Habilitar virtualización (VT-x/AMD-V) en BIOS y quitar `-no-kvm` de **Advanced → Options**. |
| **Error "KVM acceleration can't be used"** | KVM no disponible en el anfitrión. | Agregar `-no-kvm` en **Advanced → Options**. |
| **No reconoce el comando `ip routing`** | La imagen no es vIOS-L2. | Confirmar con `show version`. |
| **Etiquetas en GNS3 (`Ethernet0`) no coinciden con el IOS (`Gi0/0`)** | Name format por defecto. | **Network** → Name format `Gi{1}/{0}`, Segment size `4`. |
| **SVI en estado `down/down`** | Ningún puerto activo asignado a la VLAN. | Asignar un puerto con `switchport access vlan 10` y conectar un host. |
