# 🚨 Guía Didáctica: Plan de Respuesta a Incidentes (PRI)
## 🛡️ Basado en NIST SP 800-61 / ISO/IEC 27035

---

## 📌 Introducción

Tarde o temprano, **toda organización sufre un incidente de seguridad**. La diferencia entre una molestia y una catástrofe está en **cómo se responde**.

Un **Plan de Respuesta a Incidentes (PRI)** es el documento que define **qué hacer, quién lo hace y en qué orden** cuando algo sale mal:

- **¿Cómo detectamos el incidente?** → 🔍 Detección
- **¿Cómo evitamos que se propague?** → 🧱 Contención
- **¿Cómo eliminamos la causa?** → 🧹 Erradicación
- **¿Cómo volvemos a operar?** → 🔄 Recuperación
- **¿Qué aprendimos?** → 📚 Lecciones aprendidas

Esta guía te enseña a **construir un PRI** con fases estándar, roles claros y plazos definidos, no improvisados.

---

## 1️⃣ Conceptos Clave

```
┌─────────────────────────────────────────────────────────┐
│  📍 EVENTO                                               │
│  (ej: un login fallido)                                 │
│        ↓ ¿afecta confidencialidad, integridad o         │
│          disponibilidad?                                │
│  ⚠️ INCIDENTE                                            │
│  (ej: 500 logins fallidos + 1 exitoso desde otro país)  │
│        ↓ ¿se activa el PRI?                             │
│  🚨 RESPUESTA                                            │
│  (equipo, fases, comunicación, registro)                │
└─────────────────────────────────────────────────────────┘
```

### 📍 Evento
**Cualquier ocurrencia observable** en un sistema o red.
- Ejemplo: un usuario ingresa, un correo llega, un servicio se reinicia
- La mayoría son normales y **no requieren respuesta**

### ⚠️ Incidente
**Evento (o conjunto de eventos) que compromete** la confidencialidad, integridad o disponibilidad de la información.
- Ejemplo: ransomware, fuga de datos, acceso no autorizado, DDoS

### 🚨 Respuesta a Incidentes
**Proceso organizado** para manejar el incidente y minimizar el daño.
- Tiene fases, responsables y plazos
- Se documenta de principio a fin

---

## 2️⃣ Los Marcos de Referencia

**Pregunta clave:** ¿Invento mis propias fases?

**Respuesta:** ❌ No. Se usan **marcos estándar** reconocidos internacionalmente.

### 📊 NIST SP 800-61 vs ISO/IEC 27035

| **NIST SP 800-61 Rev.2** | **ISO/IEC 27035** | **¿Qué se hace?** |
|---|---|---|
| 🛠️ Preparación | Planificar y preparar | Políticas, equipo, herramientas |
| 🔍 Detección y Análisis | Detección y reporte + Evaluación y decisión | Identificar, validar y clasificar |
| 🧱 Contención, Erradicación y Recuperación | Respuestas | Aislar, eliminar, restaurar |
| 📚 Actividad Post-Incidente | Lecciones aprendidas | Informe, mejoras, cierre |

**📌 Nota:** NIST SP 800-61 **Rev.3 (2025)** alinea la respuesta con las funciones del **CSF 2.0** (Gobernar, Identificar, Proteger, Detectar, Responder, Recuperar). Las fases de la Rev.2 siguen siendo la base didáctica más usada.

### 🔁 El Ciclo de Vida (NIST)

```
   ┌──────────────┐     ┌────────────────────┐
   │ 🛠️ PREPARACIÓN │ ──→ │ 🔍 DETECCIÓN Y     │
   └──────────────┘     │    ANÁLISIS         │
          ↑              └────────────────────┘
          │                    ↓        ↑
          │              ┌────────────────────┐
          │              │ 🧱 CONTENCIÓN       │
          │              │ 🧹 ERRADICACIÓN     │
          │              │ 🔄 RECUPERACIÓN     │
          │              └────────────────────┘
          │                        ↓
          │              ┌────────────────────┐
          └───────────── │ 📚 POST-INCIDENTE   │
                         └────────────────────┘
```

**🔑 Es un ciclo:** lo aprendido en un incidente **mejora la preparación** para el siguiente.

---

## 3️⃣ Fase 1: 🛠️ Preparación

**Objetivo:** Estar listos **antes** de que ocurra el incidente.

### 👥 Equipo de Respuesta (CSIRT interno)

| **Rol** | **Responsabilidad** | **Ejemplo** |
|---|---|---|
| 🎖️ Líder de incidentes | Coordina y toma decisiones | Jefe de TI / CISO |
| 🔧 Analista técnico | Investiga, contiene, erradica | Administrador de redes |
| 📢 Comunicaciones | Informa a clientes, prensa, autoridad | Gerencia / RR.PP. |
| ⚖️ Legal / Cumplimiento | Evalúa obligaciones legales | Asesor legal / DPO |
| 👔 Dirección | Aprueba decisiones críticas | Gerente general |

### 🧰 Recursos Necesarios

- 📞 **Lista de contactos** actualizada (internos, proveedores, CSIRT Nacional)
- 📋 **Inventario de activos** (qué sistemas existen y cuáles son críticos)
- 💾 **Respaldos** probados y fuera de línea
- 🔍 **Herramientas:** SIEM, IDS/IPS, EDR, logs centralizados
- 📝 **Formularios** de registro de incidentes
- 🎯 **Playbooks** por tipo de incidente (ransomware, phishing, fuga de datos)

**✅ Correcto:** "Los respaldos se prueban cada mes; última restauración exitosa: 03/09"
**❌ Incorrecto:** "Tenemos respaldos" (sin saber si funcionan)

---

## 4️⃣ Fase 2: 🔍 Detección y Análisis

**Objetivo:** Confirmar que **es un incidente**, entender su alcance y **clasificar su severidad**.

### 📡 Fuentes de Detección

| **Fuente** | **Ejemplo** |
|---|---|
| 🖥️ SIEM / IDS | Alerta Suricata: tráfico hacia IP maliciosa conocida |
| 📊 Logs | 300 intentos de login fallidos en 10 minutos |
| 👤 Usuarios | "No puedo abrir mis archivos, todos terminan en .locked" |
| 🌐 Terceros | CSIRT Nacional avisa que tus credenciales aparecen filtradas |

### 🧪 Preguntas de Análisis

1. ❓ ¿Qué pasó exactamente?
2. ❓ ¿Cuándo empezó? (primer indicador)
3. ❓ ¿Qué sistemas y datos están afectados?
4. ❓ ¿Sigue activo?
5. ❓ ¿Hay datos personales comprometidos?

### 🚦 Clasificación de Severidad

Se reutiliza la lógica de **Riesgo = Probabilidad × Impacto**, pero aplicada al incidente **en curso**:

| **Severidad** | **Criterio** | **Tiempo de respuesta** |
|---|---|---|
| 🟢 Baja | Afecta 1 equipo, sin datos sensibles | < 72 horas |
| 🟡 Media | Varios equipos o servicio degradado | < 24 horas |
| 🟠 Alta | Servicio crítico caído o datos personales expuestos | < 4 horas |
| 🔴 Crítica | Operación paralizada, datos masivos, obligación legal | **Inmediato** |

**📌 Nota:** Los tiempos son EJEMPLOS. **Cada organización debe definirlos según sus servicios críticos.**

**✅ Correcto:** "Severidad Alta: servidor de pagos cifrado, 3.500 registros con RUT afectados"
**❌ Incorrecto:** "Parece grave" (sin alcance ni datos)

---

## 5️⃣ Fase 3: 🧱 Contención, 🧹 Erradicación y 🔄 Recuperación

### 🧱 Contención
**Objetivo:** Detener la propagación **sin destruir evidencia**.

| **Tipo** | **Acción** | **Ejemplo** |
|---|---|---|
| ⏱️ Corto plazo | Aislar rápido | Desconectar equipo
