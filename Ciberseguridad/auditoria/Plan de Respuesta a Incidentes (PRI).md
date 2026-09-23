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
| ⏱️ Corto plazo | Aislar rápido | Desconectar equipo de la red (no apagarlo) |
| 🕐 Largo plazo | Estabilizar | Bloquear IP en firewall, deshabilitar cuenta comprometida |

**⚠️ Importante:** Antes de contener, **preservar evidencia** (imagen de disco, captura de memoria, copia de logs).

### 🧹 Erradicación
**Objetivo:** Eliminar la **causa raíz**.

- 🦠 Eliminar malware y persistencias
- 🔐 Cambiar credenciales comprometidas
- 🩹 Parchar la vulnerabilidad explotada
- 🔍 Verificar que no quedan otros equipos infectados

### 🔄 Recuperación
**Objetivo:** Volver a operar **de forma segura**.

- 💾 Restaurar desde respaldo limpio
- 🧪 Validar integridad antes de reconectar
- 👀 Monitoreo reforzado (mínimo 30 días)
- ✅ Confirmar con usuarios que el servicio funciona

**✅ Correcto:** "Se restauró el servidor desde respaldo del 14/09, verificado con hash, y se parchó CVE explotada"
**❌ Incorrecto:** "Se reinstaló y listo" (sin saber cómo entró el atacante → volverá a entrar)

---

## 6️⃣ Fase 4: 📚 Actividad Post-Incidente

**Objetivo:** Que el incidente **no se repita**.

### 🗣️ Reunión de Lecciones Aprendidas
Realizarla **dentro de 2 semanas** tras el cierre:

1. ❓ ¿Qué pasó y en qué orden? (línea de tiempo)
2. ❓ ¿Qué funcionó bien?
3. ❓ ¿Qué falló o se demoró?
4. ❓ ¿Qué controles faltaban?
5. ❓ ¿Qué cambiamos en el PRI?

### 📄 Informe Final

- 🕐 Línea de tiempo completa
- 🎯 Causa raíz
- 📊 Impacto real (sistemas, usuarios, datos, horas caídas, costo)
- 🛠️ Acciones tomadas
- 📋 Mejoras comprometidas (con responsable y fecha)

---

## 7️⃣ Marco Legal en Chile ⚖️

Un PRI en Chile **debe considerar las obligaciones de reporte**:

| **Norma** | **¿A quién aplica?** | **Obligación** |
|---|---|---|
| **Ley 21.663** (Ley Marco de Ciberseguridad) | Servicios esenciales y operadores de importancia vital | Reportar al CSIRT Nacional (ANCI): alerta temprana en **3 horas**, segundo informe en **72 horas** (24 h para OIV en servicios esenciales), informe final en **15 días** |
| **Ley 21.719** (Protección de Datos Personales) | Quien trate datos personales | Notificar a la Agencia de Protección de Datos y, según el caso, a los titulares afectados, sin dilaciones indebidas |
| **Normativa sectorial** (CMF, etc.) | Banca, cooperativas, seguros | Reporte según norma específica del regulador |

**📌 Nota:** Verificar plazos vigentes en la normativa y reglamentos al momento de redactar el PRI.

---

## 8️⃣ Ejemplo: Cómo Aplicar a Cualquier Caso

### 📖 Escenario 1: Ransomware (Cooperativa)

**🔍 Detección:**
- 08:15 — Usuarios reportan archivos con extensión `.locked`
- 08:20 — EDR alerta cifrado masivo en servidor de archivos
- 08:30 — Se confirma nota de rescate → **Incidente confirmado**

**🚦 Clasificación:** 🔴 Crítica
- Servidor de archivos + BD de socios (5.200 registros con RUT) afectados
- Operación de atención detenida

**🧱 Contención:**
- 08:35 — Aislar segmento de red del servidor (VLAN en cuarentena)
- 08:40 — Deshabilitar cuenta de servicio usada por el atacante
- 08:45 — Captura de memoria e imagen de disco

**🧹 Erradicación:**
- Acceso inicial: RDP expuesto con credencial débil
- Cierre de RDP público, reseteo de credenciales, eliminación de persistencias

**🔄 Recuperación:**
- Restauración desde respaldo offline del día anterior
- Monitoreo reforzado 30 días

**⚖️ Reporte:** CSIRT Nacional (alerta temprana en 3 h) + Agencia de Protección de Datos (datos personales afectados)

**📚 Lecciones:** Implementar VPN con MFA, eliminar RDP público, reducir RPO a 4 horas

---

### 📖 Escenario 2: Phishing (Microempresa)

**🔍 Detección:**
- Empleado reporta correo sospechoso donde ingresó sus credenciales de correo

**🚦 Clasificación:** 🟡 Media
- 1 cuenta comprometida, sin evidencia de acceso a datos sensibles

**🧱 Contención:** Cambio de contraseña + cierre de sesiones activas
**🧹 Erradicación:** Revisión de reglas de reenvío creadas por el atacante (se elimina 1)
**🔄 Recuperación:** Activar MFA en la cuenta
**📚 Lecciones:** MFA obligatorio para toda la empresa + capacitación en phishing

---

### 🎯 El Punto Crítico

Un PRI **no es un documento teórico**. Funciona solo si:
1. **👥 Roles definidos:** cada persona sabe qué hacer
2. **⏱️ Tiempos claros:** severidad → plazo de respuesta
3. **📝 Todo registrado:** cada acción con hora y responsable
4. **🧪 Se prueba:** simulacros al menos una vez al año

---

## 9️⃣ Plantilla de Registro de Incidente 📝

```
🆔 ID Incidente:        INC-2026-001
📅 Fecha/hora detección:
👤 Reportado por:
📍 Sistemas afectados:
📋 Tipo de incidente:   [ ] Malware [ ] Phishing [ ] Fuga de datos
                        [ ] DDoS [ ] Acceso no autorizado [ ] Otro
🚦 Severidad:           [ ] Baja [ ] Media [ ] Alta [ ] Crítica
👥 Datos personales:    [ ] Sí [ ] No   → Cantidad aprox:
⚖️ Requiere reporte:    [ ] CSIRT Nacional [ ] Agencia Datos [ ] Regulador

🕐 LÍNEA DE TIEMPO:
  HH:MM — Acción — Responsable

🧱 Contención:
🧹 Erradicación (causa raíz):
🔄 Recuperación:
📚 Lecciones aprendidas:
✅ Fecha de cierre:
```

---

## 🔟 Checklist Final

Antes de entregar tu PRI:

- [ ] 🛠️ **Preparación**
  - [ ] 👥 Equipo de respuesta con roles y contactos
  - [ ] 📋 Inventario de activos críticos
  - [ ] 💾 Respaldos probados
  - [ ] 🎯 Playbooks por tipo de incidente
- [ ] 🔍 **Detección y Análisis**
  - [ ] 📡 Fuentes de detección identificadas
  - [ ] 🚦 Tabla de severidad con tiempos de respuesta
- [ ] 🧱 **Contención / Erradicación / Recuperación**
  - [ ] 🔒 Procedimiento de preservación de evidencia
  - [ ] 🧹 Pasos para identificar causa raíz
  - [ ] 🔄 Criterios para volver a operar
- [ ] 📚 **Post-Incidente**
  - [ ] 🗣️ Reunión de lecciones aprendidas
  - [ ] 📄 Formato de informe final
- [ ] ⚖️ **Legal**
  - [ ] Ley 21.663 y Ley 21.719 revisadas
  - [ ] Plazos de notificación documentados
- [ ] 🔗 ¿Cité marcos? (NIST SP 800-61, ISO/IEC 27035)

---

## 🎓 Conclusión: No Improvisar, Responder

**❌ El error común:** Reaccionar sin plan
- "Apaguemos todo" → Se pierde evidencia
- "Formateemos y listo" → El atacante vuelve a entrar
- "No le digamos a nadie" → Incumplimiento legal

**✅ Lo correcto:** Seguir fases definidas
- Detectar → Clasificar → Contener → Erradicar → Recuperar → Aprender
- Cada acción registrada, con responsable y hora
- Reportar dentro de los plazos legales

---

### 🎯 El Ciclo Completo

**🛠️ Preparar → 🔍 Detectar → 🧱 Contener → 🧹 Erradicar → 🔄 Recuperar → 📚 Aprender**

**⚠️ Un incidente sin plan = crisis. Un incidente con plan = procedimiento.**

---

## 📚 Referencias

- NIST SP 800-61 Rev.2 — *Computer Security Incident Handling Guide*
- NIST SP 800-61 Rev.3 — *Incident Response Recommendations and Considerations for Cybersecurity Risk Management*
- ISO/IEC 27035-1:2023 — *Information security incident management*
- Ley 21.663 — Ley Marco de Ciberseguridad (Chile)
- Ley 21.719 — Protección de Datos Personales (Chile)
- CSIRT Nacional / ANCI — https://www.csirt.gob.cl
