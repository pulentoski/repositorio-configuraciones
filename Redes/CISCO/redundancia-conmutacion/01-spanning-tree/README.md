# 🌳 Spanning Tree — STP · RSTP · MSTP

Guía técnica y educativa para comprender y configurar **Spanning Tree en switches Cisco IOS**, desde el STP clásico hasta **RSTP** y **MSTP**.

> 🎯 **Objetivo:** comprender por qué se forman bucles en capa 2, cómo los evita Spanning Tree y configurar correctamente las versiones modernas del protocolo.

---

# 1. 🔎 ¿Por qué existen los bucles?

La redundancia física en capa 2 crea caminos cerrados. Ethernet **no tiene TTL**, por lo que una trama puede circular indefinidamente.

```text
          ┌──────┐
          │ SW1  │
          └┬────┬┘
           │    │
     ┌─────┘    └─────┐
     │                │
 ┌───┴──┐         ┌───┴──┐
 │ SW2  ├─────────┤ SW3  │
 └──────┘         └──────┘

  Broadcast ──► SW1 ──► SW2 ──► SW3 ──► SW1 ──► ...
```

### Consecuencias de un bucle

| Problema                      | Efecto                                     |
| ----------------------------- | ------------------------------------------ |
| Tormenta de broadcast         | CPU y enlaces al 100 %                     |
| Inestabilidad de tabla MAC    | La MAC "salta" entre puertos               |
| Tramas duplicadas             | Los hosts reciben múltiples copias         |

📌 **Spanning Tree bloquea lógicamente enlaces redundantes, manteniéndolos disponibles como respaldo.**

---

# 2. 📚 Versiones de Spanning Tree

| Versión           | Estándar     | Instancias             | Convergencia   |
| ----------------- | ------------ | ---------------------- | -------------- |
| 🔵 STP            | IEEE 802.1D  | 1 para todas las VLANs | 30 – 50 s      |
| 🔵 PVST+          | Cisco        | 1 por VLAN             | 30 – 50 s      |
| 🟢 RSTP           | IEEE 802.1w  | 1 para todas las VLANs | < 1 s – pocos s |
| 🟢 Rapid PVST+    | Cisco        | 1 por VLAN             | < 1 s – pocos s |
| 🟠 MSTP           | IEEE 802.1s  | Instancias agrupadas   | < 1 s – pocos s |

---

# 3. 🔵 STP Clásico (IEEE 802.1D)

## 3.1 BPDU

Los switches intercambian **BPDU (Bridge Protocol Data Units)** cada **2 segundos** para construir el árbol.

## 3.2 Bridge ID

```text
Bridge ID = Prioridad (4 bits) + Extended System ID (12 bits = VLAN) + MAC (48 bits)

Ejemplo VLAN 10:
32768 + 10 = 32778 . 0011.2233.4455
```

📌 La prioridad por defecto es **32768** y solo admite **múltiplos de 4096**.

## 3.3 Algoritmo STA

```text
1. Elegir Root Bridge        ──► Menor Bridge ID
2. Elegir Root Ports         ──► Menor costo hacia el Root (1 por switch no raíz)
3. Elegir Designated Ports   ──► 1 por segmento
4. Bloquear el resto         ──► Non-Designated
```

### Desempate

```text
1. Menor Root Path Cost
2. Menor Bridge ID del emisor
3. Menor Port ID del emisor
```

### Costos (802.1D revisado)

| Velocidad | Costo |
| --------- | ----: |
| 10 Mbps   |   100 |
| 100 Mbps  |    19 |
| 1 Gbps    |     4 |
| 10 Gbps   |     2 |

## 3.4 Ejemplo de elección

```text
             ┌────────────┐
             │ SW1  ROOT  │  Prioridad 4096
             └─┬───────┬──┘
           DP  │       │  DP
               │       │
           RP  │       │  RP
          ┌────┴─┐   ┌─┴────┐
          │ SW2  ├───┤ SW3  │
          └──────┘DP ▲ ✖    └──────┘
                     │
                Puerto bloqueado
```

## 3.5 Roles de puerto

| Rol                 | Función                                       |
| ------------------- | --------------------------------------------- |
| Root Port (RP)      | Mejor camino hacia el Root Bridge             |
| Designated (DP)     | Reenvía tráfico en el segmento                |
| Non-Designated      | Bloqueado para evitar bucles                  |

## 3.6 Estados de puerto

| Estado        | Recibe BPDU | Aprende MAC | Reenvía | Duración   |
| ------------- | :---------: | :---------: | :-----: | ---------- |
| Blocking      |      ✅      |      ❌      |    ❌    | 20 s (Max Age) |
| Listening     |      ✅      |      ❌      |    ❌    | 15 s       |
| Learning      |      ✅      |      ✅      |    ❌    | 15 s       |
| Forwarding    |      ✅      |      ✅      |    ✅    | —          |
| Disabled      |      ❌      |      ❌      |    ❌    | —          |

```text
Blocking ──20s──► Listening ──15s──► Learning ──15s──► Forwarding
                        └──────── 30 – 50 segundos ────────┘
```

## 3.7 Configuración

```cisco
spanning-tree mode pvst
spanning-tree vlan 10 priority 4096
```

O de forma automática:

```cisco
spanning-tree vlan 10 root primary
spanning-tree vlan 10 root secondary
```

> 🏭 **Nota industrial:** los tiempos de convergencia de **30 a 50 segundos** del STP clásico son **inaceptables en producción**. Una caída de ese tiempo interrumpe VoIP, sesiones y aplicaciones. Hoy se utiliza **RSTP / Rapid PVST+ o MSTP**.

---

# 4. 🟢 RSTP (IEEE 802.1w)

RSTP mantiene la lógica de elección de STP, pero converge en **milisegundos a pocos segundos** gracias al mecanismo **Proposal / Agreement** entre switches vecinos.

## 4.1 Diferencias con STP

| Característica          | STP 802.1D              | RSTP 802.1w                     |
| ----------------------- | ----------------------- | ------------------------------- |
| Convergencia            | 30 – 50 s               | < 1 s – pocos s                 |
| Detección de falla      | Max Age 20 s            | 3 Hellos perdidos (6 s)         |
| Generación de BPDU      | Solo el Root            | Cada switch                     |
| Transición              | Por temporizadores      | Handshake Proposal / Agreement  |
| Puertos de respaldo     | No                      | Alternate / Backup              |

## 4.2 Nuevos estados

| STP 802.1D                     | RSTP 802.1w    |
| ------------------------------ | -------------- |
| Disabled / Blocking / Listening | **Discarding** |
| Learning                       | **Learning**   |
| Forwarding                     | **Forwarding** |

## 4.3 Nuevos roles

| Rol           | Función                                              |
| ------------- | ---------------------------------------------------- |
| Root          | Mejor camino al Root Bridge                          |
| Designated    | Reenvía en el segmento                               |
| **Alternate** | Camino alternativo al Root (reemplaza al Root Port)  |
| **Backup**    | Respaldo de un Designated en el mismo segmento       |
| Disabled      | Puerto administrativamente apagado                   |

```text
          ROOT
         ┌────┐
         │SW1 │
         └┬──┬┘
          │  │
       RP │  │ ALT ◄── Si cae el RP, pasa a Forwarding de inmediato
         ┌┴──┴┐
         │SW2 │
         └────┘
```

## 4.4 Tipos de enlace

| Tipo              | Descripción                       | Convergencia rápida |
| ----------------- | --------------------------------- | :-----------------: |
| **Edge**          | Conecta a hosts (PortFast)        |          ✅          |
| **Point-to-Point** | Switch ↔ switch, full-duplex     |          ✅          |
| Shared            | Half-duplex (hub)                 |          ❌          |

## 4.5 Configuración

```cisco
spanning-tree mode rapid-pvst
spanning-tree vlan 10,20 root primary
```

### Puerto Edge (hacia hosts)

```cisco
interface GigabitEthernet0/5
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
```

### Enlace Point-to-Point

```cisco
interface GigabitEthernet0/1
 spanning-tree link-type point-to-point
```

📌 **BPDU Guard** apaga el puerto Edge si recibe una BPDU, evitando que un switch no autorizado altere la topología.

---

# 5. 🟠 MSTP (IEEE 802.1s)

PVST+ crea **una instancia por VLAN**: con 500 VLANs son 500 árboles. MSTP agrupa VLANs en **pocas instancias**, optimizando CPU y memoria.

```text
VLAN 10, 20, 30 ──► Instancia 1 ──► Root: DSW1
VLAN 40, 50, 60 ──► Instancia 2 ──► Root: DSW2
Resto           ──► Instancia 0 (IST)
```

## 5.1 Región MST

Dos switches pertenecen a la misma región solo si coinciden **los tres** parámetros:

| Parámetro               | Ejemplo       |
| ----------------------- | ------------- |
| Nombre de región        | `EMPRESA`     |
| Número de revisión      | `1`           |
| Mapeo VLAN → instancia  | `1: 10,20,30` |

📌 **IST (Instancia 0)** existe siempre y se comunica con switches fuera de la región.

## 5.2 Balanceo con MSTP

```text
            ┌──────┐          ┌──────┐
            │ DSW1 │          │ DSW2 │
            │Root  │          │Root  │
            │MST 1 │          │MST 2 │
            └──┬───┘          └───┬──┘
       MST1 ✅ │ ╲              ╱ │ ✅ MST2
               │  ╲ MST2 ✖    ╱  │
               │   ╲  MST1 ✖ ╱   │
            ┌──┴───┐        ┌──┴───┐
            │ ASW1 │        │ ASW2 │
            └──────┘        └──────┘
```

Ambos enlaces trabajan: cada instancia usa un camino distinto.

## 5.3 Configuración

```cisco
spanning-tree mode mst

spanning-tree mst configuration
 name EMPRESA
 revision 1
 instance 1 vlan 10,20,30
 instance 2 vlan 40,50,60
 exit

spanning-tree mst 1 priority 4096
spanning-tree mst 2 priority 8192
```

En el segundo switch de distribución:

```cisco
spanning-tree mst 1 priority 8192
spanning-tree mst 2 priority 4096
```

---

# 6. 📊 Comparación rápida

| Característica      | STP     | RSTP     | PVST+   | Rapid PVST+ | MSTP        |
| ------------------- | ------- | -------- | ------- | ----------- | ----------- |
| Estándar            | ✅       | ✅        | ❌       | ❌           | ✅           |
| Convergencia rápida | ❌       | ✅        | ❌       | ✅           | ✅           |
| Instancias          | 1       | 1        | Por VLAN | Por VLAN   | Agrupadas   |
| Balanceo por VLAN   | ❌       | ❌        | ✅       | ✅           | ✅           |
| Uso de recursos     | Bajo    | Bajo     | Alto    | Alto        | Bajo        |
| Uso habitual        | Legado  | Básico   | Legado  | Cisco       | Multivendor |

---

# 7. 🔍 Verificación

### Estado general

```cisco
show spanning-tree
```

### Por VLAN

```cisco
show spanning-tree vlan 10
```

### Resumen y modo

```cisco
show spanning-tree summary
```

### Root Bridge

```cisco
show spanning-tree root
```

### MSTP

```cisco
show spanning-tree mst configuration
show spanning-tree mst
```

### Interfaces

```cisco
show spanning-tree interface GigabitEthernet0/1 detail
```

---

# 8. ⚠️ Errores frecuentes

### 1. Root Bridge elegido al azar

El switch con la MAC más baja (a menudo el más antiguo) queda como Root. Definir siempre la prioridad.

```cisco
spanning-tree vlan 10 root primary
```

### 2. Modos distintos entre switches

```cisco
show spanning-tree summary
```

### 3. PortFast en enlaces entre switches

Puede generar bucles temporales. Usar PortFast **solo hacia hosts**.

### 4. Regiones MST que no coinciden

Nombre, revisión o mapeo diferente separan la región.

### 5. Prioridad no múltiplo de 4096

```text
% Bridge Priority must be in increments of 4096
```

---

# 9. 🧩 Plantilla Rapid PVST+

```cisco
! MODO
spanning-tree mode rapid-pvst

! ROOT
spanning-tree vlan <VLANS> root primary

! PUERTOS HACIA HOSTS
interface range <INTERFACES_ACCESO>
 spanning-tree portfast
 spanning-tree bpduguard enable

! ENLACES ENTRE SWITCHES
interface range <INTERFACES_TRONCALES>
 spanning-tree link-type point-to-point
```

# 10. 🧩 Plantilla MSTP

```cisco
spanning-tree mode mst

spanning-tree mst configuration
 name <REGION>
 revision <N>
 instance 1 vlan <VLANS_GRUPO_1>
 instance 2 vlan <VLANS_GRUPO_2>
 exit

spanning-tree mst 1 root primary
spanning-tree mst 2 root secondary
```

---

# 11. 📌 Resumen

```text
SPANNING TREE
 │
 ├── 🔵 STP 802.1D
 │      └── 30 – 50 s · obsoleto
 │
 ├── 🟢 RSTP 802.1w
 │      └── Proposal/Agreement · Edge · P2P
 │
 └── 🟠 MSTP 802.1s
        └── VLANs agrupadas en instancias · regiones
```

### ⭐ Comandos más importantes

```cisco
spanning-tree mode rapid-pvst
spanning-tree vlan 10 root primary
spanning-tree portfast
```

---

## 🚀 Checklist Spanning Tree

```text
☐ Elegir versión (Rapid PVST+ o MSTP)
☐ Definir Root Bridge primario y secundario
☐ Configurar PortFast en puertos de acceso
☐ Activar BPDU Guard
☐ Verificar roles y estados
☐ Verificar región MST (si aplica)
☐ Simular caída de enlace y medir convergencia
```
