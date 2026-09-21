# 🌳 Manual Técnico y Académico de Spanning Tree Protocol (STP)

## 📌 SECCIÓN 1: ¿Qué es STP y para qué se usa?

### 1. Definición Técnica
**Spanning Tree Protocol (STP)** es un protocolo de Capa 2 del modelo OSI (estandarizado en **IEEE 802.1D**) diseñado para mantener una topología de red libre de bucles (*loops*) en entornos con enlaces redundantes.

* Desactiva de forma lógica las rutas redundantes para evitar bucles.
* Si un enlace principal falla, STP habilita automáticamente la ruta de respaldo (*failover*).

```
        [ Switch Raíz (Root Bridge) ]
               /            \
    (Forwarding)            (Forwarding)
             /                \
     [ Switch A ] ---------- [ Switch B ]
                     ❌ (Blocking)
```

### 2. ¿Para qué se utiliza?

* 🔄 **Prevención de Bucles en Capa 2:** Evita que las tramas circulen infinitamente entre switches.
* ⚡ **Eliminación de Tormentas de Broadcast:** Impide que los mensajes de difusión masiva (ej. peticiones ARP) saturen los procesadores de los switches y colapsen el ancho de banda.
* 🛡️ **Protección contra Inestabilidad de Tabla MAC:** Previene que las direcciones MAC cambien constantemente de puerto (*MAC database instability*) debido a tramas duplicadas.
* 🔁 **Redundancia Transparente:** Proporciona alta disponibilidad sin requerir intervención manual si un cable o puerto físico se desconecta.

### 3. El Problema: Bucle de Capa 2 vs. Capa 3

| Característica | Capa 3 (IP) 🌐 | Capa 2 (Ethernet) 🔌 |
| :--- | :--- | :--- |
| **Mecanismo Anti-Bucle** | TTL (*Time to Live*) en cabecera IP. | **No existe TTL** en tramas Ethernet. |
| **Comportamiento en Bucle** | El paquete se descarta cuando TTL = 0. | La trama circula **infinitamente** hasta colapsar la red. |
| **Solución** | Enrutamiento dinámico. | **Spanning Tree Protocol (STP)**. |

> 🔬 **Regla de oro:** `En Capa 2, la redundancia física requiere STP para evitar el colapso por bucles.`

---

## 🏷️ SECCIÓN 2: Elección de Roles, Estados y Costos

### 1. Algoritmo Spanning Tree (STA)

STP construye un árbol lógico calculando las mejores rutas hacia un switch central llamado **Root Bridge** (Puente Raíz).

```
               1. Elección del Root Bridge (Menor BID)
                                │
               2. Selección de Root Ports (RP)
                                │
          3. Selección de Designated Ports (DP)
                                │
      4. Bloqueo de Puertos Redundantes (Alternate/Blocking)
```

#### A. Bridge ID (BID)
El identificador único de cada switch en STP. Consta de:
* **Prioridad:** Valor por defecto `32768` (modificable en incrementos de 4096).
* **Dirección MAC:** Usada como desempate si las prioridades son iguales.
> **Ganador del Root Bridge:** El switch con el **BID MÁS BAJO**.

#### B. Roles de los Puertos
* 👑 **Root Port (RP):** Puerto de un switch no-raíz con la ruta de menor costo hacia el Root Bridge.
* 🟢 **Designated Port (DP):** Puerto en estado de reenvío (*Forwarding*) que atiende a un segmento de red. Todos los puertos del Root Bridge son DP.
* 🔴 **Alternate / Blocking Port (AP):** Puerto bloqueado lógicamente para romper el bucle.

---

### 2. Estados del Puerto en STP Tradicional (802.1D)

| Estado | Recibe BPDUs? | Aprende MACs? | Reenvía Datos? | Tiempo |
| :--- | :---: | :---: | :---: | :--- |
| 🚫 **Blocking** | ✅ Sí | ❌ No | ❌ No | Indefinido |
| 👂 **Listening** | ✅ Sí | ❌ No | ❌ No | 15 Segundos |
| 🎓 **Learning** | ✅ Sí | ✅ Sí | ❌ No | 15 Segundos |
| 🟢 **Forwarding**| ✅ Sí | ✅ Sí | ✅ Sí | Indefinido |
| ❌ **Disabled** | ❌ No | ❌ No | ❌ No | Manual |

* **Tiempo total de convergencia en 802.1D:** ~30 a 50 segundos.
* **Rapid STP (RSTP - 802.1w):** Reduce la convergencia a **menos de 2 segundos** unificando estados a *Discarding*, *Learning* y *Forwarding*.

---

## ⚙️ SECCIÓN 3: Configuración y Ejemplos Prácticos (Cisco IOS)

### 1. Configuración del Modo STP

Cisco soporta varios modos de STP. El recomendado para convergencia rápida por VLAN es **PVST+** o **Rapid PVST+**.

```text
Switch# configure terminal
! Activar Rapid PVST+ para convergencia rápida por VLAN
Switch(config)# spanning-tree mode rapid-pvst
```

---

### 2. Manipulación de la Elección del Root Bridge

Para garantizar estabilidad, **nunca** dejes la elección del Root Bridge al azar o por valores por defecto.

```text
! Opción A: Configurar prioridad explícita (Múltiplos de 4096)
Switch(config)# spanning-tree vlan 10 priority 4096

! Opción B: Usar comandos macro de Cisco
Switch(config)# spanning-tree vlan 10 root primary
Switch(config)# spanning-tree vlan 20 root secondary
```

---

### 3. Optimización para Puertos de Acceso (PortFast y BPDU Guard)

Para evitar que los puertos conectados a PCs o servidores esperen 30 segundos antes de pasar a *Forwarding*, se activa **PortFast**. Para evitar ataques o switches no autorizados, se acompaña con **BPDU Guard**.

```text
! Configuración en la interfaz del usuario final
Switch(config)# interface fastEthernet 0/10
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
! Pasa a Forwarding inmediatamente
Switch(config-if)# spanning-tree portfast
! Si recibe una BPDU (ej. un usuario conecta un switch), apaga el puerto
Switch(config-if)# spanning-tree bpduguard enable
Switch(config-if)# exit

! Habilitar PortFast globalmente en todos los puertos de acceso
Switch(config)# spanning-tree portfast default
```

---

### 🔍 Comandos de Verificación y Diagnóstico

* `show spanning-tree` ➔ Muestra el estado global de STP, el Root Bridge y el rol de cada puerto.
* `show spanning-tree vlan 10` ➔ Muestra los detalles de STP específicos para una VLAN.
* `show spanning-tree summary` ➔ Muestra un resumen de los modos y puertos activos en PortFast.
* `show interfaces status err-disabled` ➔ Muestra puertos desactivados por protección (ej. BPDU Guard).