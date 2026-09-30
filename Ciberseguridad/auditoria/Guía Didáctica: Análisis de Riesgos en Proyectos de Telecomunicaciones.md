# 📊 Guía Didáctica: Análisis de Riesgos en Proyectos de Telecomunicaciones
## 🎯 Riesgo = Probabilidad × Impacto

---

## 📌 Introducción

El análisis de riesgos en telecomunicaciones es la **evaluación sistemática** de los obstáculos, amenazas y contratiempos que pueden surgir durante la **planificación, diseño e implementación** de un proyecto de red, junto con las estrategias para mitigarlos.

A diferencia de un análisis de ciberseguridad (donde la amenaza es un atacante), aquí el riesgo es **todo lo que pueda hacer fallar el proyecto**: equipos que fallan, interferencias, permisos que se atrasan, proveedores que no entregan o requisitos que cambian.

Para cuantificarlo combinamos dos dimensiones:

- **¿Qué tan probable es que ocurra el evento?** → 📈 Probabilidad
- **¿Cuánto daño le hace al proyecto si ocurre?** → 💥 Impacto

---

## 1️⃣ Las 4 Bases del Análisis de Riesgos

```
┌──────────────────────────────────────────────────────────┐
│ 1. 🔍 IDENTIFICAR   → ¿Qué puede fallar en el proyecto?  │
│ 2. 🧮 EVALUAR       → P × I para cada riesgo             │
│ 3. 📊 PRIORIZAR     → Ordenar por nivel de riesgo        │
│ 4. 🛡️ MITIGAR       → Plan para bajar P, I o ambos       │
└──────────────────────────────────────────────────────────┘
```

### 🔗 Relación con PPDIOO

| **Fase** | **Rol en el análisis de riesgos** |
|---|---|
| 🧭 Preparar | Identificar riesgos de negocio, presupuesto y alcance |
| 🗺️ Planear | Identificar y evaluar riesgos técnicos, de recursos y plazos |
| 📐 Diseñar | Mitigar por diseño (redundancia, holguras, margen de enlace) |
| 🔧 Implementar | Riesgos de terreno, proveedores, pruebas de aceptación |
| 📡 Operar | Monitorear riesgos residuales (fallas, SLA) |
| 📈 Optimizar | Reevaluar el registro de riesgos con datos reales |

---

## 2️⃣ Categorías de Riesgo en Telecomunicaciones

| **Categoría** | **Ejemplos** |
|---|---|
| 🔌 **Técnico / Hardware** | Falla de OLT, switch core, fuentes de poder, transceptores |
| 📶 **Radioeléctrico** | Interferencias electromagnéticas, obstrucción de zona de Fresnel, desvanecimiento por lluvia |
| 🔄 **Interoperabilidad** | ONT de un fabricante no compatible con OLT de otro, versiones de firmware, protocolos propietarios |
| 📋 **Requisitos / Alcance** | Cambios del cliente, nuevas zonas de cobertura, mayor ancho de banda exigido |
| 🚚 **Proveedores / Logística** | Retraso en entrega de equipos, stock de fibra, quiebre de stock |
| 🏗️ **Obra civil / Terreno** | Permisos municipales, uso de postes, servidumbres, canalizaciones |
| ⚖️ **Regulatorio** | Autorizaciones SUBTEL, concesiones, Ley de Torres, normativa de espectro |
| 👷 **Recursos humanos** | Falta de técnicos certificados (fusión, radioenlaces), rotación del equipo |
| 🌦️ **Ambiental** | Clima, vientos, sismos, cortes eléctricos en sitios remotos |

---

## 3️⃣ ¿De Dónde Salen los Valores?

**Pregunta clave:** ¿Quién decide si la Probabilidad es 3 o 4?

**Respuesta:** ❌ No es opinión. Los valores vienen de **datos técnicos, históricos y de terreno**.

```
❌ "P = 4" NO significa "creo que se va a atrasar"
✅ "P = 4" significa: "En 6 de 10 proyectos similares ocurrió + el site survey lo confirma"
```

### 📊 Fuentes de Datos Reales

| **Dato Real** | **Cómo Obtenerlo** | **Ejemplo** |
|---|---|---|
| 📁 **Proyectos anteriores** | Informes de cierre, lecciones aprendidas | "4 de 8 despliegues FTTH se atrasaron por permisos" |
| 🔌 **Confiabilidad de equipos** | Fichas técnicas (MTBF, AFR), garantías | "OLT con MTBF de 200.000 h" |
| 📶 **Mediciones de terreno** | Site survey, análisis de espectro, línea de vista | "Canal 5.8 GHz con 7 redes vecinas detectadas" |
| 🚚 **Proveedores** | Cotizaciones, lead time, historial de entregas | "Lead time ONT: 10–14 semanas" |
| 🏛️ **Trámites** | Tiempos históricos municipales y SUBTEL | "Permiso de uso de postes: 45–90 días" |
| 📟 **Operación** | Tickets NOC, registros de fallas | "3 cortes de energía/mes en el sitio" |
| ⚖️ **Normativa** | Ley 18.168, Ley 20.599, normativa SUBTEL | "Torre requiere autorización previa" |

### 📈 Cómo Construir Criterios (No Inventarlos)

**PASO 1: 🔍 Recopilar datos reales**
- ¿En cuántos proyectos similares ocurrió este problema?
- ¿Qué muestran las mediciones de terreno y las fichas técnicas?
- ¿Cuánto demoran realmente proveedores y trámites?

**PASO 2: 📊 Analizar patrones**
- Un atraso aislado no es tendencia
- Buscar **frecuencia sostenida**: ¿pasa en la mayoría de los proyectos o fue excepcional?

**PASO 3: 📋 Definir rangos basados en datos**

✅ **Correcto:**
- **P=3** porque: ocurrió en 3 de 10 proyectos similares (informes de cierre)
- **P=4** porque: site survey detectó obstrucción parcial de Fresnel en 2 de 5 enlaces
- **P=5** porque: el proveedor ya informó retraso de despacho

❌ **Incorrecto:**
- "P=3 porque siempre hay problemas con los proveedores" ❌
- "P=4 porque una vez llovió y se cayó el enlace" ❌

---

## 4️⃣ Escala de Medición

**⚠️ Advertencia:** Son rangos de ejemplo. **Cada proyecto debe ajustarlos con datos propios y del sector.**

### 📈 Probabilidad (P): 1–5

| **Nivel** | **¿Cuándo?** | **Datos que lo respaldan** |
|---|---|---|
| 1️⃣ Muy baja | <5% de proyectos similares | Sin evidencia en terreno, equipo con alto MTBF |
| 2️⃣ Baja | 5–20% | Ocurrió en casos puntuales, condiciones controladas |
| 3️⃣ Media | 20–40% | Condiciones de riesgo presentes (ej: espectro compartido) |
| 4️⃣ Alta | 40–70% | Evidencia directa en site survey, cotizaciones o historial |
| 5️⃣ Muy alta | >70% o ya ocurriendo | Proveedor confirmó atraso, interferencia medida activa |

### 💥 Impacto (I): 1–5

El impacto en un proyecto es **multidimensional**. Se evalúa cada dimensión y se toma **la más alta**.

| **Nivel** | **Plazo** | **Costo** | **Servicio / Clientes** | **Regulatorio / Contractual** |
|---|---|---|---|---|
| 1️⃣ Muy bajo | <1 semana | <2% presupuesto | Sin efecto | Ninguno |
| 2️⃣ Bajo | 1–2 semanas | 2–5% | Afecta pruebas internas | Ninguno |
| 3️⃣ Medio | 2–4 semanas | 5–10% | <500 clientes o calidad degradada | Hito contractual en riesgo |
| 4️⃣ Alto | 1–3 meses | 10–20% | 500–5.000 clientes sin servicio | Multas por SLA |
| 5️⃣ Muy alto | >3 meses | >20% | >5.000 clientes o red core caída | Incumplimiento normativo SUBTEL, proyecto inviable |

**📌 Nota:** Los valores (500, 5.000, 10%) son EJEMPLOS. **Reemplazarlos por los del proyecto real** (presupuesto, contrato, clientes proyectados).

---

## 5️⃣ Cómo Calcular

### PASO 1: 🎯 Identificar el riesgo
Redactarlo como **causa → evento → efecto**:
> "Debido a *[causa]*, puede ocurrir *[evento]*, lo que provocaría *[efecto en el proyecto]*."

**Ejemplo:** "Debido a la saturación de la banda 5.8 GHz, puede haber interferencia en el radioenlace troncal, lo que provocaría pérdida de paquetes en 800 clientes."

### PASO 2: 📈 Estimar Probabilidad
1. 📁 Historial de proyectos similares
2. 📶 Mediciones y site survey
3. 🔌 Fichas técnicas (MTBF/AFR) y cotizaciones

### PASO 3: 💥 Estimar Impacto
1. ⏱️ Días de atraso en la ruta crítica (carta Gantt)
2. 💰 Sobrecosto en % del presupuesto
3. 👥 Clientes o servicios afectados
4. ⚖️ Multas, SLA o incumplimiento normativo

### PASO 4: 🧮 Multiplicar
**R = P × I**

### PASO 5: 📊 Clasificar

| **Riesgo** | **Rango** | **Acción en el proyecto** |
|---|---|---|
| 🟢 Bajo | 1–5 | Aceptar y monitorear |
| 🟡 Medio | 6–9 | Plan de mitigación en el diseño |
| 🟠 Alto | 10–16 | Mitigar antes de implementar, asignar responsable |
| 🔴 Crítico | 17–25 | No avanzar de fase sin mitigación aprobada |

---

## 6️⃣ Matriz Visual

```
            💥 IMPACTO (I)
        1    2    3    4    5
    1   1    2    3    4    5   ← Falla OLT (P=1, I=5)
    2   2    4    6    8   10
📈  3   3    6    9   12   15
P   4   4    8   12   16   20   ← Permisos postes (P=4, I=4)
    5   5   10   15   20   25
```

🟢 (1–5) Bajo · 🟡 (6–9) Medio · 🟠 (10–16) Alto · 🔴 (17–25) Crítico

---

## 7️⃣ Desarrollo de Estrategias de Mitigación

Una vez priorizado, cada riesgo recibe una estrategia:

| **Estrategia** | **Qué hace** | **Ejemplo en telecom** |
|---|---|---|
| 🚫 **Evitar** | Elimina la causa | Cambiar de 5.8 GHz no licenciado a banda licenciada |
| 🔽 **Mitigar** | Baja P o I | Redundancia 1+1, UPS, stock de repuestos, holgura en cronograma |
| 🔁 **Transferir** | Traspasa el riesgo | Contrato con multas al proveedor, seguro, subcontratar obra civil |
| ✅ **Aceptar** | Se asume con monitoreo | Riesgos bajos con plan de contingencia |

### 📉 Riesgo Residual
Después de mitigar, **recalcular P × I**. Ese es el riesgo residual que se acepta.

```
Riesgo inicial:  P=4 × I=3 = 12 🟠
Mitigación:      cambio a banda licenciada 23 GHz
Riesgo residual: P=1 × I=3 = 3 🟢
```

---

## 8️⃣ Ejemplos Aplicados

### 📖 Escenario 1: Despliegue FTTH GPON (ISP regional)

**⚠️ Riesgo:** Debido a la tramitación de uso de postes con la distribuidora eléctrica, puede atrasarse el tendido de fibra, lo que retrasaría la puesta en servicio.

**📈 Probabilidad = 4 porque:**
- 📁 Historial: 5 de 8 despliegues anteriores tuvieron atraso por permisos
- 🏛️ Tiempo real de tramitación: 60–90 días vs 30 planificados
- 📋 Postes de 2 sectores con factibilidad aún pendiente

**💥 Impacto = 4 porque:**
- ⏱️ Atraso estimado: 6–8 semanas en ruta crítica
- 👥 1.200 clientes preventa sin servicio en fecha comprometida
- 💰 Pérdida de ingresos proyectada: 12% del flujo del primer año

**🧮 Cálculo:** R = 4 × 4 = **16 (🟠 Alto)**

**🛡️ Mitigación:** Iniciar trámites en fase Preparar, priorizar sectores con factibilidad aprobada, evaluar canalización subterránea en tramos críticos.

---

### 📖 Escenario 2: Radioenlace punto a punto (sector rural)

**⚠️ Riesgo:** Debido a la ocupación de la banda 5.8 GHz, puede haber interferencia en el enlace troncal, lo que degradaría el servicio.

**📈 Probabilidad = 4 porque:**
- 📶 Análisis de espectro: 7 redes activas en el canal, piso de ruido −78 dBm
- 🔍 Site survey: torre compartida con otros 2 WISP
- 📁 Historial: enlaces similares con reclamos por intermitencia

**💥 Impacto = 3 porque:**
- 👥 450 clientes dependen del enlace
- 📉 Degradación de throughput, no caída total
- ⚖️ Sin multas contractuales, pero sí reclamos y bajas

**🧮 Cálculo:** R = 4 × 3 = **12 (🟠 Alto)**

**🛡️ Mitigación:** Migrar a banda licenciada o aumentar margen de desvanecimiento con antenas de mayor ganancia. Riesgo residual: P=1 → R = 3 🟢.

---

### 📖 Escenario 3: Falla de hardware en OLT (puesta en marcha)

**⚠️ Riesgo:** Debido a una falla de hardware, puede caer la OLT principal, dejando sin servicio a los clientes conectados.

**📈 Probabilidad = 1 porque:**
- 🔌 Ficha técnica: AFR 1,2% anual
- 🔧 Equipo nuevo con garantía y pruebas de burn-in
- 📟 Sin fallas registradas en equipos del mismo modelo

**💥 Impacto = 5 porque:**
- 👥 3.200 clientes en una sola OLT sin redundancia
- ⏱️ Reposición del proveedor: 15 días
- ⚖️ Multas por SLA con clientes corporativos

**🧮 Cálculo:** R = 1 × 5 = **5 (🟢 Bajo)**

**📝 Observación:** Aunque el riesgo es bajo, el impacto es máximo. Se recomienda **mitigar igual** (tarjeta de respaldo o OLT en stock), porque es un punto único de falla.

---

## 9️⃣ Registro de Riesgos (Plantilla)

| ID | Riesgo (causa → evento → efecto) | Categoría | Fase PPDIOO | P | I | R | Nivel | Estrategia | Responsable | R residual |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Permisos de postes → atraso tendido → puesta en servicio tardía | Obra civil | Preparar | 4 | 4 | 16 | 🟠 | Mitigar | Jefe de proyecto | 8 |
| R02 | Espectro saturado → interferencia → degradación | Radioeléctrico | Diseñar | 4 | 3 | 12 | 🟠 | Evitar | Ing. RF | 3 |
| R03 | Falla OLT → caída → clientes sin servicio | Hardware | Diseñar | 1 | 5 | 5 | 🟢 | Mitigar | Ing. red | 2 |

---

## 🔟 Checklist Final

- [ ] ✅ ¿Riesgo redactado como causa → evento → efecto?
- [ ] 🏷️ ¿Categoría y fase PPDIOO asignadas?
- [ ] 📈 **¿P basada en datos?**
  - [ ] 📁 Historial de proyectos similares
  - [ ] 📶 Mediciones / site survey
  - [ ] 🔌 Fichas técnicas, cotizaciones, lead times
- [ ] 💥 **¿I basada en datos?**
  - [ ] ⏱️ Días de atraso en ruta crítica
  - [ ] 💰 Sobrecosto en % del presupuesto
  - [ ] 👥 Clientes/servicios afectados
  - [ ] ⚖️ SLA, contrato o normativa aplicable
- [ ] 🧮 ¿Cálculo visible? (R = P × I)
- [ ] 📊 ¿Clasificación correcta?
- [ ] 🛡️ ¿Estrategia y responsable definidos?
- [ ] 📉 ¿Riesgo residual recalculado?
- [ ] 🔗 ¿Fuentes citadas? (informes, mediciones, fichas técnicas, normativa)

---

## 🎓 Conclusión: No Inventar, Medir

**❌ Error común:**
- "Creo que el proveedor se va a atrasar" → Opinión
- "Una vez falló un enlace" → Evento aislado
- "Podría afectar a varios clientes" → Sin cuantificar

**✅ Lo correcto:**
- P=4 porque: 5 de 8 proyectos previos se atrasaron + lead time cotizado de 14 semanas
- I=4 porque: 6 semanas de atraso en ruta crítica + 1.200 clientes comprometidos

### 🎯 La Fórmula Completa

**🎯 Riesgo = Probabilidad × Impacto**

- **📈 Probabilidad** = Historial de proyectos + mediciones de terreno + datos técnicos de equipos y proveedores
- **💥 Impacto** = Atraso + sobrecosto + clientes afectados + consecuencias contractuales y regulatorias

**⚠️ Un riesgo sin datos es una suposición. Un riesgo sin mitigación es un problema anunciado.**
