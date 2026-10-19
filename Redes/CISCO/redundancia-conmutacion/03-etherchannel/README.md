# 🔗 EtherChannel — LACP · PAgP

Guía técnica y educativa para comprender y configurar **agregación de enlaces en switches Cisco IOS**, con énfasis en **LACP** como estándar de la industria.

> 🎯 **Objetivo:** comprender cómo EtherChannel agrupa enlaces físicos, configurar LACP y PAgP correctamente y elegir el criterio de balanceo adecuado.

---

# 1. 🔎 ¿Qué es EtherChannel?

**EtherChannel** agrupa varios enlaces físicos en **un único enlace lógico** (Port-Channel).

```text
Sin EtherChannel                     Con EtherChannel

 ┌─────┐           ┌─────┐           ┌─────┐            ┌─────┐
 │ SW1 ├───────────┤ SW2 │           │ SW1 ╞════Po1═════╡ SW2 │
 │     ├─────✖─────┤     │           │     │  4 x 1 Gbps │     │
 │     ├─────✖─────┤     │           │     │ = 4 Gbps    │     │
 │     ├─────✖─────┤     │           └─────┘             └─────┘
 └─────┘           └─────┘
  STP bloquea 3 enlaces             STP ve un solo enlace
```

### Beneficios

| Beneficio            | Descripción                                        |
| -------------------- | -------------------------------------------------- |
| Ancho de banda       | Suma la capacidad de los enlaces                   |
| Redundancia          | Si cae un enlace, el tráfico sigue por los demás   |
| Compatible con STP   | STP trata el Port-Channel como un solo puerto      |
| Configuración única  | Se configura la interfaz lógica                    |

📌 Se pueden agrupar hasta **8 enlaces activos** (LACP admite 8 adicionales en standby).

---

# 2. 📚 Tipos de EtherChannel

| Tipo         | Protocolo | Estándar         | Modos               |
| ------------ | --------- | ---------------- | ------------------- |
| 🟢 LACP      | Dinámico  | IEEE 802.3ad / 802.1AX | Active / Passive |
| 🔵 PAgP      | Dinámico  | Cisco            | Desirable / Auto    |
| ⚪ Estático   | Ninguno   | —                | On                  |

---

# 3. ⚖️ Balanceo de carga

EtherChannel **no reparte tramas una por una**. Aplica un **hash** sobre campos del encabezado y asigna cada flujo a un enlace.

```text
Flujo A (IP 10.1.1.10 → 10.2.2.20) ──hash──► Enlace 1
Flujo B (IP 10.1.1.11 → 10.2.2.20) ──hash──► Enlace 2
Flujo C (IP 10.1.1.12 → 10.2.2.20) ──hash──► Enlace 3
```

📌 **Un solo flujo nunca supera la velocidad de un enlace físico.**

### Criterios disponibles

| Método            | Campos utilizados               | Uso recomendado                 |
| ----------------- | ------------------------------- | ------------------------------- |
| `src-mac`         | MAC origen                      | Tráfico capa 2                  |
| `dst-mac`         | MAC destino                     | Tráfico capa 2                  |
| `src-dst-mac`     | MAC origen + destino            | Capa 2 general                  |
| `src-ip`          | IP origen                       | Muchos clientes                 |
| `dst-ip`          | IP destino                      | Muchos servidores               |
| `src-dst-ip`      | IP origen + destino             | ✅ Recomendado general           |
| `src-dst-port`    | Puertos L4 origen + destino     | Pocos hosts, muchos flujos      |

### Configuración

```cisco
port-channel load-balance src-dst-ip
```

📌 El balanceo es **global** en el switch y **no necesita coincidir** en ambos extremos.

---

# 4. 🟢 LACP (IEEE 802.3ad)

## 4.1 Modos

| Modo        | Comportamiento                                   |
| ----------- | ------------------------------------------------ |
| **Active**  | Inicia la negociación enviando LACPDU            |
| **Passive** | Responde, pero no inicia                         |

### Combinaciones

| SW1 \ SW2   | Active | Passive |
| ----------- | :----: | :-----: |
| **Active**  |   ✅   |    ✅    |
| **Passive** |   ✅   |    ❌    |

## 4.2 Configuración

```cisco
interface range GigabitEthernet0/1 - 2
 switchport mode trunk
 channel-group 1 mode active
 exit

interface Port-channel1
 switchport mode trunk
```

En el otro switch:

```cisco
interface range GigabitEthernet0/1 - 2
 switchport mode trunk
 channel-group 1 mode passive
```

### Parámetros opcionales

```cisco
lacp system-priority 100
interface GigabitEthernet0/1
 lacp port-priority 100
```

📌 La prioridad define qué puertos quedan **activos** cuando existen más de 8.

> 🏭 **Nota industrial:** LACP es el **estándar universal** de la industria. Funciona entre Cisco, Juniper, Aruba, Huawei, servidores Linux (bonding modo 802.3ad), VMware e hipervisores. Es la opción por defecto en diseños actuales.

---

# 5. 🔵 PAgP (Cisco)

## 5.1 Modos

| Modo          | Comportamiento                         |
| ------------- | -------------------------------------- |
| **Desirable** | Inicia la negociación                  |
| **Auto**      | Responde, pero no inicia               |

### Combinaciones

| SW1 \ SW2     | Desirable | Auto |
| ------------- | :-------: | :--: |
| **Desirable** |    ✅      |  ✅   |
| **Auto**      |    ✅      |  ❌   |

## 5.2 Configuración

```cisco
interface range GigabitEthernet0/3 - 4
 switchport mode trunk
 channel-group 2 mode desirable
```

En el otro switch:

```cisco
interface range GigabitEthernet0/3 - 4
 switchport mode trunk
 channel-group 2 mode auto
```

> 🏭 **Nota industrial:** PAgP es **propietario de Cisco** y está **en desuso** frente a LACP. Solo se encuentra en redes Cisco antiguas.

---

# 6. ⚪ Modo On (estático)

```cisco
channel-group 3 mode on
```

| Ventaja                  | Riesgo                                                |
| ------------------------ | ----------------------------------------------------- |
| Sin negociación          | No detecta errores de cableado ni de configuración   |
| Compatible con todo      | Puede crear bucles si un extremo no está agrupado     |

📌 `on` solo funciona con `on` en el otro extremo. **No combina con LACP ni PAgP.**

---

# 7. 🧩 Requisitos de compatibilidad

Todos los puertos del grupo deben coincidir en:

```text
☐ Velocidad y dúplex
☐ Modo (access / trunk)
☐ VLAN de acceso o VLANs permitidas
☐ VLAN nativa
☐ Mismo tipo de medio
```

Si no coinciden, el puerto queda **suspendido** (`s`).

---

# 8. 🌐 EtherChannel capa 3

Entre switches multicapa o routers, el Port-Channel puede tener IP.

```cisco
interface range GigabitEthernet0/1 - 2
 no switchport
 channel-group 10 mode active
 exit

interface Port-channel10
 no switchport
 ip address 10.0.0.1 255.255.255.252
```

---

# 9. 📊 Comparación rápida

| Característica     |       LACP |      PAgP |      On |
| ------------------ | ---------: | --------: | ------: |
| Estándar           |          ✅ |         ❌ |       — |
| Negociación        |          ✅ |         ✅ |       ❌ |
| Multivendor        |          ✅ |         ❌ |       ✅ |
| Detecta errores    |          ✅ |         ✅ |       ❌ |
| Enlaces standby    |          ✅ |         ❌ |       ❌ |
| Estado industria   |   Estándar |  En desuso | Evitar |

---

# 10. 🔍 Verificación

### Resumen

```cisco
show etherchannel summary
```

```text
Flags:  D - down   P - bundled in port-channel
        I - stand-alone   s - suspended
        S - Layer2   U - in use   R - Layer3

Group  Port-channel  Protocol    Ports
------+-------------+-----------+------------------
1      Po1(SU)       LACP        Gi0/1(P) Gi0/2(P)
```

### Detalle

```cisco
show etherchannel port-channel
```

### Balanceo

```cisco
show etherchannel load-balance
```

### LACP

```cisco
show lacp neighbor
show lacp sys-id
```

### PAgP

```cisco
show pagp neighbor
```

---

# 11. ⚠️ Errores frecuentes

### 1. Passive + Passive o Auto + Auto

No se forma el canal.

### 2. Mezclar LACP con PAgP

```text
Port-channel en estado (SD)
```

### 3. Parámetros distintos entre puertos

Puerto en estado `s` (suspended).

### 4. Configurar solo la interfaz física

Los cambios deben aplicarse en `interface Port-channel`.

### 5. Esperar que un solo flujo use todo el ancho de banda

El hash asigna cada flujo a **un** enlace.

---

# 12. 🧩 Plantilla LACP

```cisco
! BALANCEO
port-channel load-balance src-dst-ip

! INTERFACES FÍSICAS
interface range <INTERFACES>
 switchport mode trunk
 channel-group <N> mode active

! INTERFAZ LÓGICA
interface Port-channel<N>
 switchport mode trunk
 switchport trunk allowed vlan <VLANS>
```

---

# 13. 📌 Resumen

```text
ETHERCHANNEL
 │
 ├── 🟢 LACP 802.3ad
 │      └── Active / Passive · estándar universal
 │
 ├── 🔵 PAgP
 │      └── Desirable / Auto · Cisco · en desuso
 │
 └── ⚪ On
        └── Estático · sin negociación
```

### ⭐ Comando más importante

```cisco
channel-group 1 mode active
```

---

## 🚀 Checklist EtherChannel

```text
☐ Verificar compatibilidad de puertos
☐ Elegir protocolo (LACP)
☐ Configurar channel-group en ambos extremos
☐ Configurar interfaz Port-channel
☐ Definir balanceo de carga
☐ Verificar con show etherchannel summary
☐ Desconectar un enlace y comprobar continuidad
```
