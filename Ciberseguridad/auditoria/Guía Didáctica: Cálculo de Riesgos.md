# 📊 Guía Didáctica: Cálculo de Riesgos
## 🎯 Riesgo = Probabilidad × Impacto

---

## 📌 Introducción

En gestión de riesgos, necesitamos **cuantificar** qué tan grave es cada amenaza. Para esto usamos una fórmula simple que combina dos dimensiones:

- **¿Qué tan probable ocurra la amenaza?** → 📈 Probabilidad
- **¿Qué tan grave sería el impacto si ocurre?** → 💥 Impacto

Multiplicar ambas nos da el **Riesgo total**.

Esta guía te enseña cómo **calcular** y **justificar** riesgos en cualquier organización, usando criterios objetivos.

---

## 1️⃣ Los Tres Conceptos Clave

```
┌─────────────────────────────────────────────────────────┐
│  ⚠️ AMENAZA                                              │
│  (ej: robo de datos)                                    │
│                                                         │
│  ¿Qué tan probable?  →  📈 PROBABILIDAD (P)            │
│  ¿Qué tan grave?     →  💥 IMPACTO (I)                 │
│                                                         │
│  🎯 RIESGO = P × I                                      │
└─────────────────────────────────────────────────────────┘
```

### 📈 Probabilidad (P)
**¿Qué tan probable es que ocurra?**

- Depende de: vulnerabilidades, intentos previos, capacidad del atacante
- Escala: 1 (casi nunca) a 5 (casi seguro)

### 💥 Impacto (I)
**¿Qué tan grave sería si ocurre?**

- Depende de: datos afectados, operaciones perdidas, daño legal/reputacional
- Escala: 1 (leve) a 5 (catastrófico)

### 🎯 Riesgo (R)
**El resultado: P × I**

- Rango: 1 a 25
- Nos indica si debemos actuar ahora o puede esperar

---

## 2️⃣ ¿De Dónde Salen los Valores?

**Pregunta clave:** ¿Quién decide si Probabilidad es 3 o 4? ¿Es mi criterio personal?

**Respuesta:** ❌ No. Los valores vienen de **análisis de datos reales y patrones constantes**, no de opiniones.

### 🔍 El Criterio se Basa en Evidencia

**No es arbitrario:**
```
❌ "P = 4" NO significa "creo que es probable"
✅ "P = 4" significa: "Existen datos objetivos que muestran probabilidad alta"
```

### 📊 Fuentes de Datos Reales

| **Dato Real** | **Cómo Búscarlo** | **Ejemplo** |
|---|---|---|
| **🎯 Ataques históricos** | Reportes públicos, HAVEIBEENPWNED, INCIBE | "Sector cooperativo: 8 brechas en últimos 2 años" |
| **🚨 Intentos de ataque** | Logs de firewall, IDS, reportes de seguridad | "Intentos de fuerza bruta: 150/mes detectados" |
| **🔐 Vulnerabilidades** | Auditoría técnica, pentesting, escaneo | "Servidor expuesto en internet sin WAF" |
| **📋 Contexto organizacional** | Tamaño real, dependencias críticas | "5.000 usuarios en BD, datos financieros" |
| **⚖️ Regulaciones** | Leyes, estándares ISO | "Ley 21.719: datos personales = sanciones" |

### 📈 Cómo Construir Criterios (No Inventarlos)

**PASO 1: 🔍 Recopila datos reales**
- ¿Cuántos ataques ha habido en tu sector en los últimos 3 años?
- ¿Ha sufrido tu organización intentos de ataque? ¿Cuántos?
- ¿Qué vulnerabilidades encontró la auditoría?

**PASO 2: 📊 Analiza patrones constantes**
- No cuentes un evento aislado como "tendencia"
- Busca **frecuencia sostenida**: ¿Ocurre cada mes? ¿Cada trimestre?
- Pregunta: ¿Esto es excepcional o el patrón normal?

**PASO 3: 📋 Define rangos basado en datos**

✅ **Correcto (basado en datos):**
- **P=3** porque: 3–5 ataques/año en sector (búsqueda INCIBE)
- **P=4** porque: 8 intentos/12 meses contra tu org (logs verificados)
- **P=5** porque: Intentos activos ahora (logs tiempo real)

❌ **Incorrecto (arbitrario):**
- "P=3 porque creo que es probable" ❌
- "P=4 porque pasó hace 2 años" ❌

---

## 3️⃣ Escala de Medición (Basada en Datos)

**⚠️ Advertencia importante:** Los siguientes son ejemplos típicos. **Tu organización debe validarlos con datos reales de tu sector.**

### 📈 Probabilidad (P): 1–5

| **Nivel** | **¿Cuándo?** | **Datos que lo respaldan** |
|---|---|---|
| 1️⃣ | Muy baja | <1 ataque/año en sector + sin vulnerabilidades en auditoría |
| 2️⃣ | Baja | 1–2 ataques/año en sector + vulnerabilidades menores |
| 3️⃣ | Media | 3–5 ataques/año en sector + vulnerabilidades conocidas |
| 4️⃣ | Alta | 6–10 ataques/año en sector + intentos documentados contra tu org |
| 5️⃣ | Muy alta | >10 ataques/año en sector O intentos activos ahora mismo |

**🔍 Cómo obtener estos datos:**
- Reportes públicos (INCIBE, HAVEIBEENPWNED, CNI)
- Logs de tu firewall/IDS (últimos 12 meses)
- Reportes de auditorías y pentesting

### 💥 Impacto (I): 1–5

| **Nivel** | **¿Cuándo?** | **Datos que lo respaldan** |
|---|---|---|
| 1️⃣ | Muy bajo | <50 usuarios, datos no clasificados |
| 2️⃣ | Bajo | 50–500 usuarios, datos internos (no regulados) |
| 3️⃣ | Medio | 500–5.000 usuarios, datos personales (protección requerida) |
| 4️⃣ | Alto | 5.000–50.000 usuarios, datos financieros O sistemas críticos caídos |
| 5️⃣ | Muy alto | >50.000 usuarios, operaciones paralizadas, violación legal segura |

**🔍 Cómo obtener estos datos:**
- Inventario de activos real (usuarios en BD, tipos de datos)
- Análisis de criticidad (cuál sistema no puede fallar)
- Leyes aplicables (qué dice sobre daño a X usuarios)

**📌 Nota:** Los números (50, 500, 5.000) son EJEMPLOS. **Reemplázalos con números reales de tu sector.**

---

## 4️⃣ Cómo Calcular

### PASO 1: 🎯 Identifica la amenaza
Define claramente: *"¿Cuál es la amenaza específica?"*

**Ejemplos:**
- 🔓 Fuga de datos de clientes
- 📵 Interrupción del servicio por DDoS
- 🚫 Acceso no autorizado a base de datos
- 🦠 Infección por malware

### PASO 2: 📈 Estima Probabilidad (Basado en Datos Reales)

**¿Qué buscar?**
1. 🎯 Ataques documentados en tu SECTOR (últimos 3 años)
2. 🚨 Intentos de ataque contra TU organización (logs, reportes)
3. 🔐 Vulnerabilidades encontradas en AUDITORÍA (resultados técnicos)

**✅ Ejemplo correcto:**
- Búsqueda INCIBE: 8 brechas en sector cooperativo últimos 2 años
- Logs de firewall: 120 intentos de acceso débil/mes
- Auditoría técnica: servidor expuesto, sin MFA, credenciales débiles
- Patrón constante: ✅ SÍ, probabilidad alta
- **Conclusión: P = 4** ✓

**❌ Ejemplo incorrecto:**
- "Hace 3 años pasó algo parecido" → Evento aislado, no es patrón
- "Creo que podría pasar" → Opinión, no datos
- "Lo vi en las noticias" → Anécdota, no contexto de tu org

### PASO 3: 💥 Estima Impacto (Basado en Datos Reales)

**¿Qué buscar?**
1. 📊 Número EXACTO de usuarios en sistemas críticos
2. 📋 Tipo y sensibilidad de datos (inventario de activos real)
3. ⚖️ Regulaciones que aplican (leyes, estándares)
4. 🔴 Criticidad del sistema (¿operación se paraliza sin él?)

**✅ Ejemplo correcto:**
- BD clientes: 3.500 registros verificados
- Datos: RUT, emails, historiales de transacciones (datos financieros)
- Regulación: Ley 21.719 + regulación financiera → sanciones garantizadas
- Criticidad: Sistema de pagos → operación depende de él
- Impacto garantizado si falla
- **Conclusión: I = 5** ✓

**❌ Ejemplo incorrecto:**
- "Podría afectar a muchos usuarios" → Vago, sin número
- "Es importante para la empresa" → Genérico, sin especificar qué
- "Causa daño" → Sin cuantificar

### PASO 4: 🧮 Multiplica
**R = P × I = 4 × 5 = 20**

### PASO 5: 📊 Clasifica

| **Riesgo** | **Rango** | **Significa** |
|---|---|---|
| 🟢 Bajo | 1–5 | Monitorear |
| 🟡 Medio | 6–9 | Mejorar controles |
| 🟠 Alto | 10–16 | Intervenir pronto |
| 🔴 Crítico | 17–25 | Intervenir ya |

**Resultado: Riesgo 20 → 🔴 Crítico → Acción inmediata**

---

## 5️⃣ Matriz Visual

```
        💥 IMPACTO (I)
    1    2    3    4    5
1   1    2    3    4    5
2   2    4    6    8   10
3   3    6    9   12   15  ← P=3, I=5 = 15 (Crítico)
4   4    8   12   16   20  ← P=4, I=5 = 20 (Crítico)
5   5   10   15   20   25

📈
P
R
O
B
.
```

🟢 (1–5): Bajo  
🟡 (6–9): Medio  
🟠 (10–16): Alto  
🔴 (17–25): Crítico

---

## 6️⃣ Ejemplo: Cómo Aplicar a Cualquier Caso

### 📖 Escenario 1: Fuga de Datos (Empresa de Servicios)

**⚠️ Amenaza:** Fuga de base de datos de clientes

**📈 Probabilidad = 4 porque (DATOS REALES):**
- 🔍 Auditoría técnica: servidor en puerto 3306 expuesto sin WAF
- 📊 Logs de seguridad: intentos de SQL injection cada 2–3 días (patrón constante)
- 🎯 Sector: búsqueda INCIBE muestra 12 brechas por inyección SQL en empresas similares últimos 18 meses
- 🔐 Contexto: sin MFA = credenciales robadas = acceso

**💥 Impacto = 5 porque (DATOS REALES):**
- 📋 Inventario BD: 8.764 registros de clientes verificados
- 📊 Tipos de datos: RUT, emails, direcciones, historiales de transacciones
- ⚖️ Regulación: Ley 21.719 aplica → violación = multas + daño reputacional
- 🔴 Criticidad: 95% de ingresos dependen del procesamiento de esas transacciones

**🧮 Cálculo:** R = 4 × 5 = **20 (🔴 Crítico)**

**📝 Justificación:** Probabilidad ALTA porque hay intentos constantes y vulnerabilidad abierta; Impacto CRÍTICO porque afecta miles de usuarios con datos regulados.

---

### 📖 Escenario 2: Caída de Sistema (Microempresa)

**⚠️ Amenaza:** Interrupción del servicio por DDoS

**📈 Probabilidad = 2 porque (DATOS REALES):**
- 🔍 Logs de firewall últimos 12 meses: CERO intentos de DDoS detectados
- 🎯 Sector: búsqueda reportes públicos muestra ataques DDoS son raros en microempresas (<5% del sector)
- 🔐 Contexto: empresa pequeña, sin presencia política/pública, sin competidores agresivos

**💥 Impacto = 3 porque (DATOS REALES):**
- 📊 Usuarios activos: 145 empleados internos + 50 clientes
- 📋 Datos: información operativa interna (no regulada por ley específica)
- 🔐 Críticidad: sistema importante pero no paraliza operación (pueden trabajar offline 4–8 horas)
- 📈 Histórico: caída similar en 2023 = pérdida estimada $800 USD

**🧮 Cálculo:** R = 2 × 3 = **6 (🟡 Medio)**

**📝 Justificación:** Probabilidad BAJA porque no hay evidencia de este tipo de ataques; Impacto MEDIO porque no afecta datos regulados.

---

### 🎯 El Punto Crítico

Los números **NO son arbitrarios**. Dependen de:
1. **📊 Datos reales:** búsquedas en INCIBE, logs, reportes públicos
2. **📈 Patrones constantes:** no contar eventos aislados hace 2 años
3. **📋 Contexto específico:** números exactos de usuarios, datos reales inventariados
4. **⚖️ Regulaciones:** qué dice la ley sobre tu contexto específico

---

## 7️⃣ Checklist Final (Datos Reales)

Antes de entregar tu análisis de riesgos:

- [ ] ✅ ¿Amenaza claramente definida?
- [ ] 📈 **¿P basada en DATOS REALES?**
  - [ ] 🔍 Búsqueda de ataques en sector (INCIBE, reportes públicos)
  - [ ] 📊 Logs de intentos contra tu organización (últimos 12 meses)
  - [ ] 🔐 Auditoría técnica con vulnerabilidades documentadas
  - [ ] ❓ ¿Son eventos aislados o patrones constantes?
- [ ] 💥 **¿I basada en DATOS REALES?**
  - [ ] 📊 Número exacto de usuarios (inventario verificado)
  - [ ] 📋 Tipos de datos en inventario de activos (clasificación real)
  - [ ] ⚖️ Ley aplicable específica (no genérica)
  - [ ] 🔴 Criticidad de sistema (¿se paraliza la operación?)
- [ ] 🧮 ✅ ¿Cálculo visible? (R = P × I = resultado)
- [ ] 📊 ✅ ¿Clasificación correcta? (Bajo/Medio/Alto/Crítico según rango)
- [ ] 📋 ✅ ¿Usé criterios documentados de la organización? (no opinión personal)
- [ ] 🔗 ✅ ¿Cité normas y fuentes? (INCIBE, auditoría, logs, regulaciones)

---

## 8️⃣ Cómo Documentar Criterios (Basado en Datos del Sector)

Cada organización debe documentar en su **Política de Riesgos o SGSI** qué significa cada número. **Esos números deben venir de análisis de datos reales de tu sector.**

### 📝 Ejemplo: Cómo Construir Criterios (Paso a Paso)

**PASO 1: 🔍 Investigar el sector**
- Buscar en INCIBE, HAVEIBEENPWNED, reportes públicos: ¿Cuántos ataques de tipo X hay por año en tu sector?
- Resultado: "En sector cooperativo chileno, últimos 3 años: 8 brechas documentadas"

**PASO 2: 📊 Establecer rangos basados en esos datos**
- Si hay 8 brechas en 3 años = ~2-3 por año
- P=3 significa "3-5 ataques/año en el sector" → Probabilidad moderada
- P=4 significa "6-10 ataques/año en el sector" → Probabilidad alta

**PASO 3: 📋 Documentar en la Política**

```
📈 PROBABILIDAD (basado en análisis sectorial):
- P=1: <1 ataque por año en sector (fuente: INCIBE 2022-2024)
- P=2: 1-3 ataques por año en sector
- P=3: 3-6 ataques por año en sector
- P=4: 6-10 ataques por año en sector
- P=5: >10 ataques por año en sector O intentos activos contra nuestra org

💥 IMPACTO (basado en regulaciones y contexto):
- I=1: <50 usuarios (dato de nuestra org) + datos no clasificados (inventario)
- I=2: 50-500 usuarios + datos internos
- I=3: 500-5.000 usuarios + datos personales (Ley 21.719 aplica)
- I=4: 5.000-50.000 usuarios + datos financieros
- I=5: >50.000 usuarios O paralización operativa garantizada
```

---

**📌 Punto clave:** Los criterios **NO se inventan**. Vienen de:
1. ✅ Análisis de datos públicos de brechas en tu sector
2. ✅ Análisis de intentos reales contra tu organización (logs)
3. ✅ Inventario real de usuarios y datos en tu organización
4. ✅ Análisis de regulaciones aplicables

**⚠️ Si no tienes datos, NO asignes números. Busca primero.**

---

## 🎓 Conclusión: No Inventar, Analizar

**❌ El error común:** Asignar números sin datos
- "Creo que P=4" → Incorrecto
- "Pasó algo hace 2 años" → Incorrecto
- "Podría ser grave" → Incorrecto

**✅ Lo correcto:** Respaldar cada número con datos reales
- P=4 porque: Análisis INCIBE muestra 8 ataques/año en el sector + logs propios muestran 150 intentos/mes
- I=5 porque: Inventario real = 5.000 usuarios + datos financieros + Ley 21.719 aplica

---

### 🎯 La Fórmula Completa

**🎯 Riesgo = Probabilidad × Impacto**

Donde:
- **📈 Probabilidad** = Análisis de datos históricos + patrones constantes del sector + intentos contra tu org
- **💥 Impacto** = Inventario real de usuarios + tipos de datos + regulaciones aplicables

**⚠️ Números sin análisis de datos = Opinión, no evaluación de riesgos.**
