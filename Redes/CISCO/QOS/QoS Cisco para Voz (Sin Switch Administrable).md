
# Guía Técnica: Configuración QoS Cisco para Voz (Sin Switch Administrable)

## 🧠 Lógica de la Configuración
QoS (Quality of Service) permite priorizar tráfico sensible, como voz (VoIP), frente a tráfico de datos.  
En este caso, al **no contar con un switch administrable**, la configuración QoS se aplica **directamente en el router**, clasificando y priorizando el tráfico basado en puertos UDP típicos de voz (RTP/SIP).

---

## ⚙️ Configuración del Router

### 1. Definir las clases de tráfico
Se identifican los flujos de voz y señalización:

```bash
class-map match-any VOZ
 match protocol rtp audio
 match access-group name VOZ-UDP

class-map match-any SIGNAL
 match protocol sip
 match access-group name SIP-UDP
```

---

### 2. Crear listas de acceso para identificar tráfico
```bash
ip access-list extended VOZ-UDP
 permit udp any any range 16384 32767

ip access-list extended SIP-UDP
 permit udp any any eq 5060
```

---

### 3. Definir la política de priorización
```bash
policy-map QOS-VOZ
 class VOZ
  priority 1500
 class SIGNAL
  bandwidth 256
 class class-default
  fair-queue
```

---

### 4. Aplicar la política en la interfaz WAN
```bash
interface GigabitEthernet0/0
 description Enlace hacia Internet
 service-policy output QOS-VOZ
```

---

## 📊 Verificación
```bash
show policy-map interface GigabitEthernet0/0
show class-map
show policy-map
```

---

## 🧩 Nota Técnica
- Esta configuración prioriza la salida del tráfico VoIP al proveedor o red externa.  
- Al no existir un switch administrable, **no se pueden marcar tramas a nivel 2 (CoS)**, por lo que la clasificación se realiza a **nivel 3/4 (IP/UDP)**.  
- Es útil en entornos domésticos, laboratorios o redes pequeñas donde el router actúa como gateway principal.

---
```
