# 🔐 Guía de Seguridad de Puertos (Port Security) en Switches Cisco

## 📌 Descripción

Este repositorio contiene una guía práctica sobre la configuración de **Port Security** en switches Cisco.  
El objetivo es aprender a proteger puertos físicos restringiendo dispositivos mediante direcciones MAC autorizadas.

La implementación de Port Security ayuda a prevenir accesos no autorizados y ataques comunes en redes LAN como el **MAC Flooding**.

---

# 🧠 ¿Qué es Port Security?

**Port Security** es una funcionalidad de los switches Cisco que permite:

- Limitar dispositivos conectados por puerto.
- Restringir direcciones MAC permitidas.
- Detectar accesos no autorizados.
- Bloquear ataques de inundación de MAC.
- Generar alertas de seguridad.

---

# 🎯 Objetivos

- Configurar Port Security en switches Cisco.
- Restringir dispositivos por dirección MAC.
- Aplicar límites de conexiones por puerto.
- Configurar acciones ante violaciones de seguridad.
- Comprender modos de protección y mitigación.

---

# 🛡 Beneficios de Implementar Port Security

| Beneficio | Descripción |
|---|---|
| 🔒 Control de acceso | Permite definir qué dispositivos pueden conectarse |
| 🚫 Mitigación de ataques | Protege contra ataques MAC Flooding |
| 📢 Alertas de seguridad | Genera eventos Syslog ante violaciones |
| ⚡ Respuesta rápida | Puede bloquear automáticamente dispositivos no autorizados |

---

# ⚙️ Requisitos Previos

Antes de configurar Port Security:

- Tener acceso administrativo al switch.
- Identificar interfaces a proteger.
- Definir política de seguridad.
- Comprender modos de violación.

---

# 🖥 Topología Básica

```text
PC1 -------- Switch Cisco -------- PC2
                Fa0/1
