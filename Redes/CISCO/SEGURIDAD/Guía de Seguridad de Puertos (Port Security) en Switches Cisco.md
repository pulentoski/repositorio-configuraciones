# 🔐 Cisco Port Security

## 📌 ¿Qué es Port Security?

**Port Security** es una característica de seguridad en switches Cisco que permite controlar qué dispositivos pueden conectarse a un puerto mediante el uso de direcciones MAC.

Su objetivo principal es evitar accesos no autorizados dentro de la red LAN.

---

# 🎯 ¿Para Qué Sirve?

Port Security se utiliza para:

- Restringir dispositivos conectados a un puerto.
- Limitar la cantidad de direcciones MAC permitidas.
- Evitar conexiones no autorizadas.
- Mitigar ataques de red como MAC Flooding.
- Aumentar la seguridad en redes LAN empresariales.

---

# ✅ Beneficios de Port Security

| Beneficio | Descripción |
|---|---|
| 🔒 Control de acceso | Permite decidir qué dispositivos pueden conectarse |
| 🛡 Mitigación de ataques | Reduce riesgos de ataques MAC Flooding |
| 📢 Monitoreo | Genera alertas y registros de seguridad |
| ⚡ Protección automática | Puede bloquear dispositivos no autorizados |
| 🧠 Administración sencilla | Permite aprendizaje automático de MAC |

---

# 🧠 Conceptos Importantes

| Concepto | Explicación |
|---|---|
| MAC Address | Dirección física única de un dispositivo |
| CAM Table | Tabla donde el switch almacena direcciones MAC |
| Sticky MAC | Aprendizaje automático de MAC autorizadas |
| Err-disabled | Estado donde el puerto queda deshabilitado |
| Access Port | Puerto destinado a un único dispositivo |

---

# ⚙️ Requisitos para Configurar Port Security

Antes de habilitar Port Security:

- El puerto debe estar en modo `access`.
- Se debe seleccionar la interfaz correcta.
- Definir la cantidad de MAC permitidas.
- Configurar la acción ante violaciones.

---

# 🔧 Tipos de Configuración

---

## 🔹 Configuración Básica

Habilita Port Security en una interfaz.

```bash
interface FastEthernet0/1

switchport mode access

switchport port-security
```

### 📌 Propósito

Activar mecanismos básicos de seguridad en el puerto.

---

## 🔹 Limitar Cantidad de MAC

```bash
switchport port-security maximum 2
```

### 📌 Propósito

Permitir únicamente cierta cantidad de dispositivos conectados.

---

## 🔹 Sticky MAC

```bash
switchport port-security mac-address sticky
```

### 📌 Propósito

Aprender automáticamente las direcciones MAC conectadas y guardarlas como autorizadas.

---

## 🔹 MAC Estática

```bash
switchport port-security mac-address 0011.2233.4455
```

### 📌 Propósito

Autorizar manualmente una dirección MAC específica.

---

# 🚨 Modos de Violación

Los modos de violación definen qué hará el switch cuando un dispositivo no autorizado intente conectarse.

---

## 🔹 Protect

```bash
switchport port-security violation protect
```

### 📌 Funcionamiento

- Bloquea tráfico no autorizado.
- No genera logs.
- El puerto continúa activo.

### 🎯 Uso recomendado

Ambientes donde se requiere continuidad operacional.

---

## 🔹 Restrict

```bash
switchport port-security violation restrict
```

### 📌 Funcionamiento

- Bloquea tráfico no autorizado.
- Genera alertas Syslog.
- Incrementa contador de violaciones.

### 🎯 Uso recomendado

Entornos empresariales con monitoreo de seguridad.

---

## 🔹 Shutdown

```bash
switchport port-security violation shutdown
```

### 📌 Funcionamiento

- Deshabilita automáticamente el puerto.
- Coloca interfaz en estado `err-disabled`.
- Requiere reactivación manual.

### 🎯 Uso recomendado

Ambientes críticos de alta seguridad.

---

# 🔄 Reactivar Puerto Bloqueado

```bash
shutdown
no shutdown
```

### 📌 Propósito

Habilitar nuevamente un puerto desactivado por seguridad.

---

# 💾 Guardar Configuración

```bash
copy running-config startup-config
```

### 📌 Propósito

Guardar la configuración permanentemente.

---

# 🔍 Comandos de Verificación

| Comando | Función |
|---|---|
| `show port-security` | Ver estado general |
| `show port-security interface FastEthernet0/1` | Ver configuración detallada |
| `show port-security address` | Ver MAC aprendidas |
| `show mac address-table` | Ver tabla MAC del switch |
| `show logging` | Revisar eventos y logs |

---

# 🧪 Ejemplo Completo

```bash
enable

configure terminal

interface FastEthernet0/1

switchport mode access

switchport port-security

switchport port-security maximum 2

switchport port-security mac-address sticky

switchport port-security violation restrict

end

copy running-config startup-config
```

---

# ⚔️ Protección Contra MAC Flooding

## 📌 ¿Qué es MAC Flooding?

Ataque donde un atacante envía múltiples direcciones MAC falsas para saturar la tabla CAM del switch.

---

## 🛡 ¿Cómo ayuda Port Security?

- Limita MAC por puerto.
- Bloquea dispositivos desconocidos.
- Reduce riesgo de sniffing.
- Evita saturación de la CAM Table.

---

# 🏢 Uso en Redes Empresariales

Port Security se implementa comúnmente en:

- Redes corporativas.
- Laboratorios Cisco.
- Instituciones educativas.
- Redes LAN empresariales.
- Infraestructura crítica.

---

# 📚 Tecnologías Relacionadas

- VLAN Security
- DHCP Snooping
- Dynamic ARP Inspection
- STP Security
- NAC (Network Access Control)

---
