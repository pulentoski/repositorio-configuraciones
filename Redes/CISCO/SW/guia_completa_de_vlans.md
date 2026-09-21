# 🌐 Manual Técnico y Académico de VLANs

---

## 📌 SECCIÓN 1: ¿Qué es una VLAN y para qué se usa?

### 1. Definición Técnica
Una **VLAN** (*Virtual Local Area Network*) es una subred lógica independiente creada dentro de una misma infraestructura física de conmutación (Capa 2 del modelo OSI).

* Permite agrupar dispositivos de forma lógica, sin importar su ubicación física en el switch.
* Divide un **dominio de broadcast** único en múltiples dominios de difusión más pequeños.

```text
       [ Switch de Capa 2 ]
       /         |        \
  [VLAN 10]  [VLAN 20]  [VLAN 30]
   Ventas     Finanzas     I+D
```

### 2. ¿Para qué se utilizan?
* 🛡️ **Seguridad y Aislamiento:** Aisla el tráfico sensible. Los dispositivos de distintas VLANs no pueden comunicarse entre sí sin un dispositivo de Capa 3 (Router o Switch Multicapa).
* ⚡ **Optimización del Rendimiento:** Reduce el tráfico broadcast (*broadcast storms*) limitándolo únicamente a los miembros de esa subred lógica.
* ⚙️ **Flexibilidad Operativa:** Facilita la administración organizando la red por roles o departamentos y no por cableado físico.

### 3. Matriz Comparativa
| Característica | Red Plana (Sin VLANs) ❌ | Red Segmentada (Con VLANs) ✅ |
| :--- | :--- | :--- |
| **Dominio de Broadcast** | Uno solo para toda la red. | Múltiples dominios independientes. |
| **Seguridad** | Baja; todo el tráfico es visible. | Alta; aislamiento estricto por función. |
| **Escalabilidad** | Limitada; se degrada con muchos equipos. | Alta; fácil incorporación de subredes. |

> 🔬 **Regla de oro:** `1 VLAN = 1 Dominio de Broadcast = 1 Subred IP`

---

## 🏷️ SECCIÓN 2: Clasificación y Tipos de VLANs

### 1. Tipos de VLAN por Función
```text
                  ┌─── 💾 VLAN de Datos (Usuarios)
                  ├─── 📞 VLAN de Voz (VoIP)
  Tipos de VLANs ─┼─── 🔑 VLAN de Gestión (SVI)
                  ├─── 🚪 VLAN Nativa (Tráfico untagged en troncal)
                  └─── 🚫 VLAN Predeterminada (VLAN 1)
```

* 💾 **VLAN de Datos:** Transporta el tráfico de usuarios finales (navegación, correos).
* 📞 **VLAN de Voz:** Transporta el tráfico de Telefonía IP. Requiere **QoS** (*Quality of Service*) para garantizar prioridad.
* 🔑 **VLAN de Gestión:** Asignada exclusivamente a la administración remota de switches, routers y APs (SSH/SNMP).
* 🚪 **VLAN Nativa:** Procesa todo el tráfico que viaja por un enlace troncal sin etiqueta (*Untagged*). Debe cambiarse por seguridad.
* 🚫 **VLAN Predeterminada:** VLAN 1 en switches Cisco. No se puede borrar ni renombrar.

### 2. Rangos de Identificadores (VLAN ID)

| Rango | Rango de ID | Uso y Características |
| :--- | :--- | :--- |
| **Rango Normal** | `1 - 1005` | Redes corporativas estándar. Se guarda en la memoria del switch (`vlan.dat`). *(1002-1005 reservados)*. |
| **Rango Extendido** | `1006 - 4094` | Utilizado por Proveedores de Servicios (ISPs) y Data Centers. Guardado en `running-config`. |

---

## ⚙️ SECCIÓN 3: Configuración y Ejemplos Prácticos (Cisco IOS)

### 1. Creación de VLANs
```text
Switch# configure terminal
Switch(config)# vlan 10
Switch(config-vlan)# name Ventas
Switch(config-vlan)# exit

Switch(config)# vlan 20
Switch(config-vlan)# name Voz_IP
Switch(config-vlan)# exit
```

### 2. Configuración de Puerto de Acceso (Access Mode - Untagged)
Asigna un puerto final (PC, impresora) a una VLAN específica:
```text
Switch(config)# interface fastEthernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config-if)# no shutdown
```

### 3. Configuración de Puerto Troncal (Trunk Mode - Encapsulación 802.1Q / dot1q)
Permite transportar múltiples VLANs hacia otro switch o router etiquetando los marcos (*Tagged*):
```text
Switch(config)# interface gigabitEthernet 0/1
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 10,20
Switch(config-if)# switchport trunk native vlan 99
Switch(config-if)# no shutdown
```

### 4. Configuración de IP de Administración (SVI)
```text
Switch(config)# interface vlan 99
Switch(config-if)# ip address 192.168.99.2 255.255.255.0
Switch(config-if)# no shutdown
Switch(config)# ip default-gateway 192.168.99.1
```

### 🔍 Comandos de Verificación
* `show vlan brief` ➔ Muestra todas las VLANs creadas y sus puertos asignados.
* `show interfaces trunk` ➔ Muestra los puertos troncales activos y las VLANs permitidas/etiquetadas.
* `show interfaces status` ➔ Muestra el estado operativo de cada interfaz física.