# 🏷️ Gestión de VLANs — VTP · GVRP / MVRP

Guía técnica y educativa para comprender y configurar la **propagación de VLANs en switches Cisco IOS**, con énfasis en **VTP** y sus riesgos reales en producción.

> 🎯 **Objetivo:** comprender cómo se distribuyen las VLANs entre switches, configurar VTP de forma segura e identificar por qué GVRP fue reemplazado por MVRP.

---

# 1. 🔎 ¿Por qué propagar VLANs?

Sin un protocolo de propagación, cada VLAN debe crearse **manualmente en cada switch**.

```text
Sin VTP                          Con VTP

SW1: vlan 10, 20, 30             SW1 (Server): vlan 10, 20, 30
SW2: vlan 10, 20, 30                   │
SW3: vlan 10, 20, 30                   ├──► SW2 (Client)
SW4: vlan 10, 20, 30                   ├──► SW3 (Client)
                                       └──► SW4 (Client)
```

📌 La propagación **solo viaja por enlaces troncales (802.1Q)**.

---

# 2. 📚 Protocolos de propagación

| Protocolo | Estándar        | Estado                       |
| --------- | --------------- | ---------------------------- |
| 🔵 VTP    | Cisco           | ⚠️ Usar con precaución        |
| 🟢 GVRP   | IEEE 802.1Q (GARP) | ❌ Obsoleto                 |
| 🟠 MVRP   | IEEE 802.1ak    | ✅ Reemplazo estándar de GVRP |

---

# 3. 🔵 VTP — VLAN Trunking Protocol

## 3.1 Modos de operación

| Modo            | Crea / borra VLANs | Sincroniza | Reenvía anuncios | Guarda en `vlan.dat` |
| --------------- | :----------------: | :--------: | :--------------: | :------------------: |
| **Server**      |         ✅          |     ✅      |        ✅         |          ✅           |
| **Client**      |         ❌          |     ✅      |        ✅         |  ✅ (v3) / ❌ (v1-v2) |
| **Transparent** |    ✅ (locales)     |     ❌      |        ✅         |          ✅           |
| **Off** (v3)    |    ✅ (locales)     |     ❌      |        ❌         |          ✅           |

```text
          ┌─────────────┐
          │ SW1  SERVER │  Crea VLAN 30
          └──────┬──────┘
                 │ Anuncio VTP (rev 5)
          ┌──────┴───────┐
          │ SW2 TRANSPAR.│  No la aplica, solo reenvía
          └──────┬───────┘
                 │
          ┌──────┴──────┐
          │ SW3  CLIENT │  Aplica VLAN 30
          └─────────────┘
```

## 3.2 Dominio VTP

Los switches solo intercambian información si comparten:

```text
☐ Mismo nombre de dominio (sensible a mayúsculas)
☐ Misma versión
☐ Misma contraseña (si existe)
☐ Enlace troncal entre ellos
```

## 3.3 Versiones

| Característica                      | V1 | V2 | V3 |
| ----------------------------------- | :-: | :-: | :-: |
| VLANs normales (1 – 1005)           | ✅ | ✅ | ✅ |
| VLANs extendidas (1006 – 4094)      | ❌ | ❌ | ✅ |
| Token Ring                          | ❌ | ✅ | ✅ |
| Transparent reenvía sin revisar versión | ❌ | ✅ | ✅ |
| Primary Server                      | ❌ | ❌ | ✅ |
| Modo Off                            | ❌ | ❌ | ✅ |
| Contraseña oculta                   | ❌ | ❌ | ✅ |
| Propaga instancias MST              | ❌ | ❌ | ✅ |

📌 **VTPv3** es la única versión recomendable si se decide usar VTP.

## 3.4 Configuración

### Server

```cisco
vtp domain EMPRESA
vtp version 2
vtp mode server
vtp password Inacap2026
```

### Client

```cisco
vtp domain EMPRESA
vtp version 2
vtp mode client
vtp password Inacap2026
```

### Transparent

```cisco
vtp mode transparent
```

### VTPv3 con Primary Server

```cisco
vtp domain EMPRESA
vtp version 3
vtp mode server
vtp password Inacap2026 hidden
end
vtp primary vlan
```

📌 `vtp primary` se ejecuta en **modo privilegiado (EXEC)**, no en configuración global.

---

# 4. 🚨 Alerta real: Revision Number y borrado masivo

Cada cambio en un Server incrementa el **Configuration Revision Number**. Los switches **aceptan siempre la base de datos con el número más alto**, aunque esté vacía.

### Escenario del desastre

```text
1. Un switch usado en laboratorio tiene:
      Dominio: EMPRESA · Revisión: 87 · Modo: Server · VLANs: 1

2. Se conecta a producción con un troncal:
      Producción: Revisión 12 · VLANs: 10, 20, 30, 40, 50

3. 87 > 12  ──► Toda la red adopta la base de datos del switch nuevo

4. Resultado:
      VLANs 10–50 eliminadas
      Puertos de acceso quedan inactivos
      Caída total de la red
```

```text
   SW LAB (rev 87)                 PRODUCCIÓN (rev 12)
   ┌──────────┐    troncal    ┌──────────┐
   │ VLAN 1   ├───────────────► VLAN 1   │
   └──────────┘                │ 10 ✖    │
                               │ 20 ✖    │
                               │ 30 ✖    │
                               └──────────┘
```

> ⚠️ **Un Client también puede propagar** su base de datos si tiene un Revision Number mayor (VTP v1/v2).

## 4.1 Cómo resetear el Revision Number

### Opción 1 — Cambiar a Transparent

```cisco
vtp mode transparent
vtp mode client
```

### Opción 2 — Cambiar el nombre de dominio

```cisco
vtp domain RESET
vtp domain EMPRESA
```

### Verificar

```cisco
show vtp status
```

```text
Configuration Revision : 0
```

## 4.2 Buenas prácticas

```text
☐ Resetear la revisión de TODO switch antes de conectarlo
☐ Usar contraseña de dominio
☐ Preferir VTPv3 (solo el Primary Server puede modificar)
☐ Considerar modo Transparent u Off en la mayoría de los switches
```

> 🏭 **Nota industrial:** muchas organizaciones operan VTP en **Transparent / Off** y gestionan las VLANs mediante **automatización** (Ansible, plantillas) para eliminar este riesgo.

---

# 5. 🟢 GVRP — GARP VLAN Registration Protocol

GVRP es el equivalente **estándar IEEE 802.1Q** a VTP. Utiliza **GARP** (Generic Attribute Registration Protocol) para registrar y propagar VLANs dinámicamente.

```text
SW1 declara VLAN 10
      │  Join (GARP)
      ▼
SW2 registra VLAN 10 en el troncal
      │  Join
      ▼
SW3 registra VLAN 10
```

### Diferencias con VTP

| Característica        | VTP                   | GVRP                     |
| --------------------- | --------------------- | ------------------------ |
| Estándar              | Cisco                 | IEEE 802.1Q              |
| Modelo                | Servidor / Cliente    | Declaración por puerto   |
| Revision Number       | ✅ (riesgo de borrado) | ❌                        |
| Poda (pruning)        | VTP Pruning           | Implícita por registro   |
| Multivendor           | ❌                     | ✅                        |

### Configuración (equipos que aún lo soportan)

```text
! Sintaxis genérica de switches multivendor
gvrp
interface <TRONCAL>
 gvrp
```

> 🏭 **Nota industrial:** GVRP está **obsoleto y descontinuado** por su lentitud y alto consumo de recursos. Fue reemplazado por **MVRP (Multiple VLAN Registration Protocol, IEEE 802.1ak)**, basado en **MRP**, más eficiente y escalable. Cisco IOS moderno soporta MVRP en algunas plataformas.

### MVRP en Cisco (plataformas compatibles)

```cisco
mvrp global
interface GigabitEthernet0/1
 switchport mode trunk
 mvrp
```

---

# 6. 📊 Comparación rápida

| Característica          | VTP v1/v2 |  VTP v3 |   GVRP |   MVRP |
| ----------------------- | --------: | ------: | -----: | -----: |
| Estándar                |         ❌ |       ❌ |      ✅ |      ✅ |
| VLANs extendidas        |         ❌ |       ✅ |      ✅ |      ✅ |
| Riesgo de borrado       |   🔴 Alto | 🟡 Bajo | 🟢 No | 🟢 No |
| Multivendor             |         ❌ |       ❌ |      ✅ |      ✅ |
| Estado                  |    Legado |  Vigente | Obsoleto | Vigente |

---

# 7. 🔍 Verificación

### Estado VTP

```cisco
show vtp status
```

### Contraseña VTP

```cisco
show vtp password
```

### Contadores

```cisco
show vtp counters
```

### VLANs

```cisco
show vlan brief
```

### Troncales

```cisco
show interfaces trunk
```

---

# 8. ⚠️ Errores frecuentes

### 1. Dominio con mayúsculas distintas

`Empresa` ≠ `EMPRESA`

### 2. Contraseña diferente

```text
MD5 digest checksum mismatch
```

### 3. No existe troncal

```cisco
show interfaces trunk
```

### 4. Crear VLANs en un Client

```text
VTP VLAN configuration not allowed when device is in CLIENT mode.
```

### 5. Conectar un switch sin resetear la revisión

Ver **sección 4**.

---

# 9. 🧩 Plantilla VTP

```cisco
! SERVER
vtp domain <DOMINIO>
vtp version <2|3>
vtp mode server
vtp password <CLAVE>

! CLIENT
vtp domain <DOMINIO>
vtp version <2|3>
vtp mode client
vtp password <CLAVE>

! TRONCAL
interface <INTERFAZ>
 switchport mode trunk
```

---

# 10. 📌 Resumen

```text
GESTIÓN DE VLANs
 │
 ├── 🔵 VTP (Cisco)
 │      ├── Server · Client · Transparent · Off
 │      └── ⚠️ Revision Number alto = borrado masivo
 │
 ├── 🟢 GVRP (802.1Q)
 │      └── ❌ Obsoleto
 │
 └── 🟠 MVRP (802.1ak)
        └── ✅ Reemplazo estándar
```

### ⭐ Comando más importante

```cisco
show vtp status
```

---

## 🚀 Checklist VTP

```text
☐ Definir dominio y versión
☐ Configurar contraseña
☐ Definir Server y Clients
☐ Verificar troncales
☐ Resetear revisión en switches nuevos
☐ Crear VLAN en Server y verificar propagación
☐ Comparar Revision Number en todos los switches
```
