# 🛡️ FHRP — First Hop Redundancy Protocols

Guía técnica y educativa para comprender y configurar **redundancia de gateway en routers y switches multicapa Cisco IOS**, con **HSRP**, **VRRP** y **GLBP**.

> 🎯 **Objetivo:** comprender cómo entregar a los hosts una puerta de enlace virtual tolerante a fallos y configurar correctamente los tres protocolos FHRP.

---

# 1. 🔎 El problema del gateway único

Los hosts tienen configurado **un solo default gateway**. Si ese router falla, la red queda sin salida aunque exista otro router disponible.

```text
          INTERNET
          │      │
      ┌───┴┐   ┌─┴──┐
      │ R1 │   │ R2 │
      │ ✖  │   │    │
      └──┬─┘   └─┬──┘
   .1    │       │    .2
         └───┬───┘
             │
      PC: Gateway 192.168.10.1  ──► Sin salida
```

---

# 2. 🧠 Concepto FHRP

FHRP crea un **router virtual** con una **IP virtual** y una **MAC virtual** compartidas por varios routers físicos.

```text
          INTERNET
          │      │
      ┌───┴┐   ┌─┴──┐
      │ R1 │   │ R2 │
      │ACT │   │STB │
      └──┬─┘   └─┬──┘
   .2    │       │    .3
         └───┬───┘
       IP virtual .1
       MAC virtual
             │
      PC: Gateway 192.168.10.1
```

📌 Si el router activo cae, el otro asume la IP y MAC virtual. **El host no nota el cambio.**

---

# 3. 📚 Protocolos FHRP

| Protocolo | Estándar  | Roles                 | Balanceo             |
| --------- | --------- | --------------------- | -------------------- |
| 🔵 HSRP   | Cisco     | Active / Standby      | Por grupo            |
| 🟢 VRRP   | RFC 5798  | Master / Backup       | Por grupo            |
| 🟠 GLBP   | Cisco     | AVG / AVF             | ✅ Nativo             |

---

# 4. 🔵 HSRP — Hot Standby Router Protocol

## 4.1 Componentes

| Elemento       | Descripción                                          |
| -------------- | ---------------------------------------------------- |
| Active         | Reenvía el tráfico del gateway virtual               |
| Standby        | Monitorea al Active y lo reemplaza si falla          |
| IP virtual     | Gateway configurado en los hosts                     |
| Prioridad      | 0 – 255 (por defecto **100**). Mayor gana            |
| Preempt        | Permite recuperar el rol Active al volver            |

### MAC virtual

| Versión  | MAC                    | Grupos     |
| -------- | ---------------------- | ---------- |
| HSRPv1   | `0000.0C07.ACxx`       | 0 – 255    |
| HSRPv2   | `0000.0C9F.Fxxx`       | 0 – 4095   |

### Temporizadores

```text
Hello: 3 s       Hold: 10 s
```

## 4.2 Configuración

Topología:

```text
R1 Gi0/0: 192.168.10.2   Prioridad 110
R2 Gi0/0: 192.168.10.3   Prioridad 100
IP virtual: 192.168.10.1
```

### R1

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.2 255.255.255.0
 standby version 2
 standby 1 ip 192.168.10.1
 standby 1 priority 110
 standby 1 preempt
```

### R2

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.3 255.255.255.0
 standby version 2
 standby 1 ip 192.168.10.1
 standby 1 priority 100
 standby 1 preempt
```

## 4.3 Preemption

```text
Sin preempt                          Con preempt

R1 cae  ──► R2 Active                R1 cae  ──► R2 Active
R1 vuelve ──► R2 sigue Active        R1 vuelve ──► R1 recupera Active
```

📌 HSRP **no tiene preempt por defecto**.

## 4.4 Tracking de interfaces

Si el enlace WAN del Active cae, el router sigue vivo en la LAN y mantiene el rol, enviando tráfico a un camino muerto. **Tracking** reduce la prioridad automáticamente.

```text
           ✖ WAN
      ┌────┴┐     ┌─────┐
      │ R1  │     │ R2  │
      │110→90│    │ 100 │  ──► R2 pasa a Active
      └──┬──┘     └──┬──┘
         └─────┬─────┘
```

```cisco
track 1 interface GigabitEthernet0/1 line-protocol

interface GigabitEthernet0/0
 standby 1 track 1 decrement 20
```

📌 Para que el Standby tome el control, **ambos routers deben tener `preempt`**.

### Tracking por alcanzabilidad (IP SLA)

```cisco
ip sla 1
 icmp-echo 8.8.8.8 source-interface GigabitEthernet0/1
 frequency 5
ip sla schedule 1 life forever start-time now

track 2 ip sla 1 reachability

interface GigabitEthernet0/0
 standby 1 track 2 decrement 20
```

## 4.5 Balanceo con múltiples grupos

```text
VLAN 10 ──► Grupo 10 ──► Active: R1
VLAN 20 ──► Grupo 20 ──► Active: R2
```

```cisco
! R1
interface Vlan10
 standby 10 ip 192.168.10.1
 standby 10 priority 110
 standby 10 preempt
interface Vlan20
 standby 20 ip 192.168.20.1
 standby 20 priority 90
 standby 20 preempt
```

📌 Alinear el Active HSRP con el **Root Bridge STP** de cada VLAN.

---

# 5. 🟢 VRRP — Virtual Router Redundancy Protocol

Protocolo **estándar** (RFC 3768 v2 / RFC 5798 v3), funcionalmente similar a HSRP.

## 5.1 Diferencias con HSRP

| Característica           | HSRP                    | VRRP                        |
| ------------------------ | ----------------------- | --------------------------- |
| Estándar                 | Cisco                   | ✅ IETF                      |
| Roles                    | Active / Standby        | **Master / Backup**         |
| Prioridad por defecto    | 100                     | 100                         |
| Preempt por defecto      | ❌                       | ✅                           |
| IP virtual = IP real     | ❌                       | ✅ (owner, prioridad 255)    |
| Hello                    | 3 s                     | 1 s                         |
| MAC virtual              | `0000.0C9F.Fxxx`        | `0000.5E00.01xx`            |
| Multicast                | 224.0.0.102 (v2)        | 224.0.0.18                  |

## 5.2 Configuración (VRRPv2)

### R1

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.2 255.255.255.0
 vrrp 1 ip 192.168.10.1
 vrrp 1 priority 110
```

### R2

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.3 255.255.255.0
 vrrp 1 ip 192.168.10.1
```

## 5.3 Configuración (VRRPv3 — IOS XE)

```cisco
fhrp version vrrp v3

interface GigabitEthernet0/0
 vrrp 1 address-family ipv4
  address 192.168.10.1 primary
  priority 110
  track 1 decrement 20
```

> 🏭 **Nota industrial:** VRRP es la opción en **entornos multivendor** (Cisco + Fortinet, Juniper, Linux con keepalived, etc.).

---

# 6. 🟠 GLBP — Gateway Load Balancing Protocol

HSRP y VRRP dejan **un router ocioso** por grupo. GLBP permite que **todos los routers reenvíen tráfico** usando **una sola IP virtual**.

## 6.1 Roles

| Rol    | Función                                                             |
| ------ | ------------------------------------------------------------------- |
| **AVG** (Active Virtual Gateway)    | Responde los ARP y asigna una MAC virtual distinta a cada host |
| **AVF** (Active Virtual Forwarder)  | Reenvía el tráfico de su MAC virtual (hasta 4 por grupo)       |

```text
                ┌───────────────┐
                │ R1  AVG + AVF1│  MAC .0001
                └───────┬───────┘
                        │        ┌───────────┐
                        ├────────┤ R2  AVF2  │  MAC .0002
                        │        └───────────┘
       IP virtual 192.168.10.1
                        │
     ┌──────────┬───────┴──┬──────────┐
    PC1        PC2        PC3        PC4
  ARP→.0001  ARP→.0002  ARP→.0001  ARP→.0002
```

### Métodos de balanceo

| Método            | Comportamiento                             |
| ----------------- | ------------------------------------------ |
| `round-robin`     | Alterna MACs en cada respuesta ARP (defecto) |
| `weighted`        | Según el peso de cada AVF                  |
| `host-dependent`  | Mismo host siempre recibe la misma MAC     |

## 6.2 Configuración

### R1

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.2 255.255.255.0
 glbp 1 ip 192.168.10.1
 glbp 1 priority 110
 glbp 1 preempt
 glbp 1 load-balancing round-robin
```

### R2

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.3 255.255.255.0
 glbp 1 ip 192.168.10.1
 glbp 1 load-balancing round-robin
```

> 🏭 **Nota industrial:** GLBP es **poco usado** en entornos modernos. Es propietario de Cisco, tiene soporte limitado en plataformas nuevas y su balanceo por ARP es poco predecible. Se prefiere **HSRP/VRRP con múltiples grupos**, o **arquitecturas de capa 3 pura** (routing hasta el acceso, ECMP, VXLAN/EVPN con anycast gateway).

---

# 7. 📊 Comparación rápida

| Característica      |       HSRP |       VRRP |       GLBP |
| ------------------- | ---------: | ---------: | ---------: |
| Estándar            |          ❌ |          ✅ |          ❌ |
| Roles               | Act / Stby | Mstr / Bkp |  AVG / AVF |
| Routers activos     |          1 |          1 |  Hasta 4   |
| Preempt por defecto |          ❌ |          ✅ |          ❌ |
| Balanceo nativo     |          ❌ |          ❌ |          ✅ |
| Tracking            |          ✅ |          ✅ |  ✅ (weight) |
| Uso habitual        | Redes Cisco | Multivendor | Poco usado |

---

# 8. 🔍 Verificación

### HSRP

```cisco
show standby brief
show standby
```

```text
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0       1    110 P Active  local           192.168.10.3    192.168.10.1
```

### VRRP

```cisco
show vrrp brief
show vrrp
```

### GLBP

```cisco
show glbp brief
show glbp
```

### Tracking

```cisco
show track
```

### Desde el host

```text
arp -a
```

Debe mostrar la **MAC virtual** asociada al gateway.

---

# 9. ⚠️ Errores frecuentes

### 1. Hosts apuntan a la IP real del router

El gateway de los hosts debe ser la **IP virtual**.

### 2. Número de grupo distinto entre routers

### 3. Versiones HSRP diferentes

HSRPv1 y v2 no interoperan.

### 4. Tracking sin preempt

La prioridad baja, pero el otro router no asume el rol.

### 5. Decremento insuficiente

```text
110 - 5 = 105 > 100  ──► No hay cambio
```

### 6. Active FHRP distinto al Root Bridge STP

Genera tráfico subóptimo entre switches de distribución.

---

# 10. 🧩 Plantilla HSRP

```cisco
! TRACKING
track 1 interface <INTERFAZ_WAN> line-protocol

! GRUPO HSRP
interface <INTERFAZ_LAN>
 ip address <IP_REAL> <MASCARA>
 standby version 2
 standby <GRUPO> ip <IP_VIRTUAL>
 standby <GRUPO> priority <PRIORIDAD>
 standby <GRUPO> preempt
 standby <GRUPO> track 1 decrement <VALOR>
```

---

# 11. 📌 Resumen

```text
FHRP
 │
 ├── 🔵 HSRP (Cisco)
 │      └── Active / Standby · preempt manual · tracking
 │
 ├── 🟢 VRRP (RFC 5798)
 │      └── Master / Backup · estándar multivendor
 │
 └── 🟠 GLBP (Cisco)
        └── AVG / AVF · balanceo nativo · poco usado
```

### ⭐ Comando más importante

```cisco
standby 1 ip 192.168.10.1
```

---

## 🚀 Checklist FHRP

```text
☐ Definir IP virtual y grupo
☐ Configurar prioridad en el router principal
☐ Activar preempt
☐ Configurar tracking del enlace WAN
☐ Configurar gateway virtual en los hosts
☐ Verificar con show standby brief
☐ Apagar el router Active y comprobar continuidad (ping -t)
☐ Restaurar y verificar preemption
```
