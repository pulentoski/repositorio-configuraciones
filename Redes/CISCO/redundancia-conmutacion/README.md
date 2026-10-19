# 🔁 Redundancia y Conmutación en Redes

Repositorio técnico y educativo del módulo **Redundancia y Conmutación en Redes (21 horas)**, con configuraciones en **Cisco IOS** y notas de uso real en la industria.

> 🎯 **Objetivo:** comprender y configurar los mecanismos que entregan **alta disponibilidad** en redes conmutadas: prevención de bucles, gestión de VLANs, agregación de enlaces y redundancia de gateway.

---

# 📂 Contenido

| #  | Unidad                                                                 | Protocolos                     |
| -- | ---------------------------------------------------------------------- | ------------------------------ |
| 01 | [🌳 Protocolos de Árbol de Expansión](01-spanning-tree/README.md)      | STP · RSTP · MSTP              |
| 02 | [🏷️ Gestión de VLANs](02-gestion-vlans/README.md)                      | VTP · GVRP / MVRP              |
| 03 | [🔗 Agregación de Enlaces](03-etherchannel/README.md)                  | EtherChannel · LACP · PAgP     |
| 04 | [🛡️ Redundancia de Primer Salto](04-fhrp/README.md)                    | HSRP · VRRP · GLBP             |

---

# 🧭 Mapa del módulo

```text
            REDUNDANCIA Y CONMUTACIÓN
                        │
   ┌──────────────┬─────┴────────┬──────────────┐
   │              │              │              │
 CAPA 2         CAPA 2         CAPA 2         CAPA 3
 Bucles         VLANs          Enlaces        Gateway
   │              │              │              │
 STP            VTP          EtherChannel     FHRP
 RSTP           GVRP           LACP           HSRP
 MSTP           MVRP           PAgP           VRRP
                                              GLBP
```

---

# 🏭 Estándar vs Propietario

| Protocolo | Tipo                   | Estado en la industria         |
| --------- | ---------------------- | ------------------------------ |
| STP       | IEEE 802.1D            | ⚠️ Obsoleto para producción    |
| RSTP      | IEEE 802.1w            | ✅ Recomendado                  |
| MSTP      | IEEE 802.1s            | ✅ Recomendado (multivendor)    |
| VTP       | Cisco                  | ⚠️ Usar con precaución          |
| GVRP      | IEEE 802.1Q (GARP)     | ❌ Reemplazado por MVRP         |
| LACP      | IEEE 802.3ad / 802.1AX | ✅ Estándar universal           |
| PAgP      | Cisco                  | ⚠️ En desuso                    |
| HSRP      | Cisco                  | ✅ Muy utilizado                |
| VRRP      | RFC 5798               | ✅ Estándar multivendor         |
| GLBP      | Cisco                  | ⚠️ Poco utilizado               |

---

# 🧪 Topología base de referencia

```text
                 INTERNET / WAN
                   │        │
              ┌────┴─┐    ┌─┴────┐
              │  R1  │    │  R2  │      ◄── FHRP
              └───┬──┘    └──┬───┘
                  │          │
              ┌───┴──┐    ┌──┴───┐
              │ DSW1 ╞════╡ DSW2 │      ◄── EtherChannel
              └─┬──┬─┘    └─┬──┬─┘
                │   ╲      ╱   │
                │    ╲    ╱    │        ◄── STP / RSTP / MSTP
                │     ╲  ╱     │
              ┌─┴──┐   ╳    ┌──┴─┐
              │ASW1│  ╱ ╲   │ASW2│      ◄── VTP
              └─┬──┘        └──┬─┘
                │              │
             VLAN 10        VLAN 20
```

---

## 🚀 Recomendación de estudio

```text
☐ 01 — Spanning Tree
☐ 02 — Gestión de VLANs
☐ 03 — EtherChannel
☐ 04 — FHRP
☐ Integrar todo en la topología base
```
