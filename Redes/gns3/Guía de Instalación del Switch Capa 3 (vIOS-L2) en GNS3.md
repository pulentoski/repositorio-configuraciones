# Guía de Instalación del Switch Capa 3 (vIOS-L2) en GNS3

Esta guía detalla los pasos para importar, configurar y desplegar una imagen de **Switch Cisco Multicapa (Capa 3) / vIOS-L2** en el simulador de red **GNS3**.

---

## 1. Introducción y Requisitos

Para practicar características avanzadas de Capa 2 y Capa 3 (Seguridad L2, VLANs, Troncales, EtherChannel, SVI, DHCP Snooping, Enrutamiento Inter-VLAN), se utiliza la imagen virtualizada oficial de Cisco **vIOS-L2** (Virtual IOS Layer 2).

### Información de la Imagen Utillizada

* **Nombre del archivo original / descarga:** `vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E`
* **Formato de disco:** Virtual Machine Disk (`.vmdk`)
* **Versión de IOS:** 15.2(4)0.55.E
* **Enlace de referencia de descarga:** [https://upw.io/75g/vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E](https://upw.io/75g/vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E)

---

## 2. Métodos de Instalación en GNS3

Existen dos opciones principales para agregar este switch en GNS3:
1. **Método A (Recomendado):** Importando el archivo de plantilla `.gns3a` (Appliance).
2. **Método B (Manual):** Creando un nuevo nodo QEMU manualmente.

---

### Método A: Instalación Automática mediante Appliance (`.gns3a`)

1. **Descargar la plantilla:**
   * Ve a la web oficial de GNS3 Marketplace y descarga la plantilla **Cisco vIOS-L2** (`cisco-vios-l2.gns3a`).
2. **Importar en GNS3:**
   * Abre GNS3.
   * Ve a **File** $
ightarrow$ **Import appliance**.
   * Selecciona el archivo `cisco-vios-l2.gns3a` descargado.
3. **Selección del Servidor:**
   * Selecciona ejecutar el appliance en la **GNS3 VM** (altamente recomendado para rendimiento QEMU).
4. **Asociación del Archivo `.vmdk`:**
   * En la lista de versiones, busca la versión correspondiente o haz clic en **Import**.
   * Selecciona el archivo descargado: `vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E`.
   * El sistema verificará el archivo y procederá con la instalación.
5. **Finalización:**
   * Haz clic en **Next** hasta finalizar. El switch aparecerá disponible en el panel izquierdo bajo el icono de Switches.

---

### Método B: Instalación Manual como QEMU VM

Si prefieres realizar el procedimiento manualmente sin usar la plantilla `.gns3a`:

1. **Abrir Preferencias de GNS3:**
   * Dirígete a **Edit** $
ightarrow$ **Preferences** (o `Ctrl + Shift + P`).
   * En el menú lateral, ve a **QEMU** $
ightarrow$ **QEMU VMs**.
   * Haz clic en el botón **New**.

2. **Configuración del Appliance:**
   * **Name:** Asigna un nombre al nodo (ejemplo: `Cisco vIOS-L2 15.2`).
   * **Type:** Selecciona `Default`.
   * **RAM:** Asigna un mínimo de **512 MB** o **1024 MB** (1 GB recomendado para labs grandes).
   * **Console type:** Selecciona `telnet`.
   * **Disk Image:** Selecciona **Existing image** si ya la habías usado, o **New image** y busca el archivo `vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E`.

3. **Ajuste de Puertos y Símbolo (Edición del Nodo):**
   * Selecciona el nodo recién creado y haz clic en **Edit**.
   * En la pestaña **Network**:
     * **Adapters:** Cambia la cantidad de adaptadores a **8** o **16** (según la cantidad de puertos GigabitEthernet que requieras).
     * **Type:** Selecciona `e1000`.
     * **Custom adapter name format:** Configura `Gi0/{port}` para que las interfaces se nombren como `GigabitEthernet0/0`, `GigabitEthernet0/1`, etc.
   * En la pestaña **General settings**:
     * **Symbol:** Cambia el icono a `/symbols/multilayer_switch.svg` o el icono de Switch L3.
     * **Category:** Asigna la categoría `Switches`.
   * Haz clic en **Apply** y **OK**.

---

## 3. Primer Inicio y Verificación

1. Arrastra el nuevo nodo **Cisco vIOS-L2** desde la barra de herramientas al lienzo de GNS3.
2. Haz clic derecho sobre el nodo y presiona **Start**.
3. Haz doble clic en el nodo para abrir la consola Telnet/PuTTY.

### Comandos de Verificación en la Consola Cisco IOS

Una vez cargado el sistema operativo, ejecuta los siguientes comandos para confirmar que las funciones de Capa 2 y Capa 3 están disponibles:

#### 1. Verificar Versión e Imagen del IOS
```text
Switch# show version
```
*Debes verificar que muestre la versión `15.2` y la plataforma `vIOS-L2`.*

#### 2. Verificar Interfaces Disponibles
```text
Switch# show ip interface brief
```
*Confirmará las interfaces GigabitEthernet activas (`Gi0/0`, `Gi0/1`, etc.).*

#### 3. Verificar Capacidad Multicapa (Habilitar Enrutamiento IP)
Por defecto, el switch actúa en modo Capa 2 pura. Para habilitar las capacidades de **Switch Capa 3 (Routing Inter-VLAN / SVIs)**:

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

#### 5. Verificar la Tabla de Enrutamiento
```text
Switch# show ip route
```
*Confirmará que el switch está operando como dispositivo Capa 3 al mostrar las redes directamente conectadas.*

---

## 4. Solución de Problemas Comunes

| Problema | Causa Probable | Solución |
| :--- | :--- | :--- |
| **El switch no arranca o entra en bucle de reinicio** | RAM insuficiente asignada al nodo QEMU. | Aumentar la memoria RAM a 1024 MB en las propiedades de la VM QEMU en GNS3. |
| **No reconoce el comando `ip routing`** | La imagen cargada no es un vIOS-L2 o se está usando un modelo L2 básico. | Confirmar mediante `show version` que la imagen corresponda al archivo `vios_l2-adventerprisek9-m.vmdk...`. |
| **Nombres de interfaz extraños (`e0/0` en lugar de `Gi0/0`)** | Formato de adaptador no configurado en la plantilla. | En Preferencias de GNS3 $
ightarrow$ QEMU VMs $
ightarrow$ Edit $
ightarrow$ Network, configurar *Custom adapter name format* a `Gi0/{port}`. |
