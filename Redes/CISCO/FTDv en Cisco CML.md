# 🔥 FTDv en Cisco CML — Guía rápida

Firewall **Cisco Secure Firewall Threat Defense Virtual** con administración web local (**FDM**), sin FMC.

`FTD 7.7.0` · `FX-OS 2.17.0`

---

## 🚀 Procedimiento

### 1️⃣ Agregar el nodo

Arrastrar **FTDv** desde el catálogo de nodos. No requiere editar el Day-0: trae IPs y credenciales preconfiguradas.

### 2️⃣ Cablear

```
[ ext-conn-0 ]
      │ G0/0
  [ ftdv-0 ]
      ├─ G0/1 ─────┐
      └─ Mgmt0/0 ──┤
                [ switch L2 ]
                     │
                [ host cliente ]
```

> ⚠️ **G0/1 y Mgmt0/0 van al mismo switch.** Es el único punto donde se falla: sin esto el cliente no alcanza la interfaz de gestión y el navegador no carga.

### 3️⃣ Esperar el arranque

4–6 minutos. Antes de eso el login rechaza credenciales válidas.

### 4️⃣ Entrar a FDM

Desde el cliente, navegador:

```
https://192.168.45.45
```

| Usuario | Contraseña |
|---|---|
| `admin` | `Cisc01@3` |

Aceptar el certificado autofirmado.

> ✅ **No se configura nada por consola.** El servidor web ya está activo de fábrica.

---

## 📍 Direccionamiento de fábrica

| Interfaz | IP | Función |
|---|---|---|
| G0/0 | DHCP | outside |
| G0/1 | 192.168.45.1/24 | gateway LAN |
| Mgmt0/0 | **192.168.45.45/24** | 🌐 FDM |
| Pool DHCP | .46 – .254 | clientes |

> 💡 FDM corre en **Mgmt0/0 (.45)**, no en la interfaz de datos. La `.1` responde ping pero no sirve el panel web.

---

## 🚀 Easy Setup

Se ejecuta una vez tras el primer login.

| Paso | Valor |
|---|---|
| Outside | IPv4 `DHCP` · IPv6 `Off` |
| NTP | zona local · servidores por defecto |
| Licencia | **Start 90-day evaluation** |

> 🎫 Cubre routing, NAT, ACL e interfaces. No cubre IPS, URL filtering ni Malware.
> Al vencer: *wipe* del nodo reinicia el contador.

> ⛔ No refrescar el navegador durante el asistente.

---

## 🎛️ Administración

| Sección | Contenido |
|---|---|
| Device → Interfaces | interfaces, subinterfaces, VLANs |
| Device → Routing | estático, OSPF, BGP |
| Policies → Access Control | reglas de filtrado |
| Policies → NAT | traducciones |
| Objects | redes, puertos, URLs |
| Monitoring → Events | tráfico permitido/bloqueado |
| Troubleshoot → Packet Tracer | 🔍 simulación de flujo |

> 🚨 **Nada se aplica hasta pulsar Deploy** → *Deploy Now*.

### Política inicial

| Regla | Acción |
|---|---|
| Trust Outbound Traffic | inside → outside ✅ |
| Default Action | Block all other ⛔ |

---

<details>
<summary>🧰 <b>Anexo: diagnóstico</b></summary>

### Nodo cliente recomendado

| Nodo | Shell | Navegador |
|---|---|---|
| `Desktop` | ✅ | ✅ **recomendado** |
| `Firefox` | ❌ | ✅ |
| `Alpine` | ✅ | ❌ |

Cliente colgado de Mgmt0/0 sin DHCP:
```bash
sudo ip addr add 192.168.45.100/24 dev eth0
sudo ip link set eth0 up
```

### Los tres prompts

| Prompt | Nivel | Acceso |
|---|---|---|
