# Cálculo de Capacidad de Red con Overhead y QoS

## 1. Concepto
Al dimensionar el ancho de banda de una red no basta con sumar el consumo de las aplicaciones.  
Se debe contemplar **overhead** y **reserva para Calidad de Servicio (QoS)**.

- **Overhead (≈ 30%)**:  
  Representa cabeceras de protocolos (Ethernet, IP, TCP/UDP), retransmisiones y variaciones de tráfico.  
  No existe una norma fija que defina el 30%, pero es un **criterio de diseño recomendado** por ingenieros y fabricantes (Cisco, Juniper, ITU-T).

- **QoS (reserva extra)**:  
  Se aplica un **10–15% adicional** para asegurar rendimiento en aplicaciones críticas como **voz y video en tiempo real**.

---

## 2. Ejemplo de cálculo

**Escenario**:  
- 20 usuarios con datos (≈ 1 Mbps c/u).  
- 5 usuarios en videollamadas HD (≈ 2 Mbps c/u).  
- 2 líneas VoIP (≈ 0.1 Mbps c/u).

**Cálculo paso a paso**:
1. **Tráfico bruto**  
   - Datos: 20 × 1 Mbps = 20 Mbps  
   - Video: 5 × 2 Mbps = 10 Mbps  
   - Voz: 2 × 0.1 Mbps = 0.2 Mbps  
   - **Total = 30.2 Mbps**

2. **Agregar overhead (30%)**  
   ```
   30.2 × 1.3 = 39.26 Mbps
   ```

3. **Agregar reserva para QoS (10%)**  
   ```
   39.26 × 1.1 = 43.18 Mbps
   ```

✅ **Ancho de banda recomendado ≈ 45 Mbps**

---

## 3. Codecs de Voz

| Codec   | Bitrate (Kbps) | Comentario                |
|---------|---------------|---------------------------|
| G.711   | 64            | Calidad alta, consumo alto|
| G.729   | 8             | Calidad aceptable, bajo BW|
| Opus    | 6–510         | Flexible, usado en WebRTC |
| AMR-WB  | 12.65–23.85   | Eficiente, VoLTE          |

---

## 4. Codecs de Video

| Codec   | Bitrate típico (Mbps) | Comentario                     |
|---------|-----------------------|--------------------------------|
| H.264   | 1–4 (SD/HD)           | Amplio soporte, estándar       |
| H.265   | 0.5–2 (SD/HD)         | Más eficiente, menor bitrate   |
| VP8     | 1–2 (HD)              | Usado en WebRTC                |
| VP9     | 0.5–1.5 (HD)          | Mejor compresión que VP8       |
| AV1     | 0.3–1 (HD)            | Muy eficiente, más reciente    |

---

## 5. Métricas Clave de QoS
- **Throughput**: tasa efectiva de transmisión.  
- **Latencia**: tiempo de tránsito de un paquete.  
- **Jitter**: variación de la latencia.  
- **Packet loss**: pérdida de paquetes, crítico en voz/video.  
