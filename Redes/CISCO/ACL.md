# 📘 Listas de Control de Acceso (ACL)

---
# 🔐 Definición de ACL

Una **ACL (Access Control List)** es una lista de reglas que controlan el **tráfico permitido o denegado** a través de un dispositivo de red (como un router o firewall).  
Sirve para **filtrar paquetes** según criterios como dirección IP, protocolo o puerto, aumentando la **seguridad y control del tráfico** en la red.

---

## 🧩 Tipos de ACL

1. **ACL Estándar**  
   - Filtra solo por **IP de origen**.  
   - No distingue puertos ni protocolos.  
   - Números: **1–99** y **1300–1999**.

2. **ACL Extendida**  
   - Filtra por **IP de origen, IP de destino, protocolos (TCP, UDP, ICMP)** y **puertos**.  
   - Números: **100–199** y **2000–2699**.

3. **ACL Nombrada**  
   - Se crean con **nombres personalizados**.  
   - Pueden ser estándar o extendidas.  
   - Facilitan la lectura, edición y mantenimiento.

---

## 🎯 Clasificación según ubicación

- **Inbound (entrante):** Filtra el tráfico antes de que entre a la interfaz.  
- **Outbound (saliente):** Filtra el tráfico que sale por la interfaz.

---

## ⚙️ Función principal

Las ACL sirven para:
- **Restringir acceso** a redes o subredes.  
- **Controlar tráfico** por protocolo o puerto.  
- **Mejorar la seguridad** del enrutamiento y NAT.  
- **Definir qué direcciones** pueden ser traducidas o acceder a determinados recursos.
  
---
---

## 🔸 1. ACL Estándar

Filtra por **IP de origen solamente**.  
No permite especificar protocolos ni puertos.

**Numeración:**
- ACL estándar numeradas: **1–99** y **1300–1999**

---
---

### ✅ Ejemplo 1: Permitir una IP específica y denegar todo lo demás

Imaginemos que quieres permitir el tráfico solo desde la dirección IP `192.168.1.10` y bloquear todo lo demás.

```bash
access-list 10 permit host 192.168.1.10
access-list 10 deny any
```

**Explicación:**
- `access-list 10 permit host 192.168.1.10`: Permite que todo el tráfico proveniente de la IP 192.168.1.10 pase a través del router.  
- `access-list 10 deny any`: Niega todo el tráfico proveniente de cualquier otra IP.

---

### ✅ Permitir una red completa y denegar el resto

Si deseas permitir todo el tráfico proveniente de la red `192.168.1.0/24` pero bloquear el tráfico de otras redes, usarías:

```bash
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 deny any
```

**Explicación:**
- `access-list 10 permit 192.168.1.0 0.0.0.255`: Permite todo el tráfico proveniente de la red 192.168.1.0/24.  
- `access-list 10 deny any`: Bloquea el tráfico proveniente de cualquier otra red.

---

### ✅ Permitir múltiples redes

Para permitir tráfico desde varias redes dentro de la misma ACL:

```bash
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 permit 192.168.2.0 0.0.0.255
access-list 10 deny any
```

**Explicación:**
- `access-list 10 permit 192.168.1.0 0.0.0.255`: Permite el tráfico de la red 192.168.1.0/24.  
- `access-list 10 permit 192.168.2.0 0.0.0.255`: Permite el tráfico de la red 192.168.2.0/24.  
- `access-list 10 deny any`: Niega el tráfico proveniente de cualquier otra red.

---

### ✅ Permitir solo tráfico de un rango de direcciones IP

Permitir tráfico solo de un rango específico de IPs dentro de una red (máscara wildcard):

```bash
access-list 10 permit 192.168.1.1 0.0.0.19
access-list 10 deny any
```

**Explicación:**
- `access-list 10 permit 192.168.1.1 0.0.0.19`: Permite el tráfico de las IPs entre 192.168.1.1 y 192.168.1.20.  
- `access-list 10 deny any`: Niega el tráfico de todas las demás IPs.

---

### ✅ Permitir solo una IP de destino específica (en ACL estándar)

Aunque las ACL estándar solo filtran por IP de origen, a veces se usan junto con otras medidas (firewalls o rutas) para controlar el acceso.

```bash
access-list 10 permit 192.168.1.10
access-list 10 deny any
```

**Explicación:**
- Permite que la IP 192.168.1.10 tenga acceso.  
- Todo el resto del tráfico se bloquea.

---

## 🔸 2. ACL Extendida

Filtra por **IP de origen**, **IP de destino**, **tipo de protocolo (TCP, UDP, ICMP)** y **puertos**.  
Permite un filtrado más detallado.

**Numeración:**
- ACL extendidas numeradas: **100–199** y **2000–2699**

---

### ¿Qué es una ACL Extendida?

```bash
access-list 110 permit tcp 192.168.1.0 0.0.0.255 any eq 80
access-list 110 deny ip any any
```

**Explicación:**
- Permite tráfico TCP desde la red 192.168.1.0/24 hacia cualquier destino en el puerto 80 (HTTP).  
- Niega cualquier otro tráfico IP.

---

## 🔸 3. ACL Nombrada

Permite crear ACL con **nombres personalizados** en lugar de números, lo que facilita la lectura y edición.

### Ejemplo:

```bash
ip access-list extended BLOQUEO_HTTP
 deny tcp any any eq 80
 permit ip any any
```

**Explicación:**
- Deniega tráfico TCP HTTP (puerto 80).  
- Permite cualquier otro tráfico IP.

---

## 🔸 NAT y ACL trabajando juntos

Cuando usamos **NAT con sobrecarga (PAT)**, se utiliza una ACL estándar para definir qué direcciones IP pueden ser traducidas.

```bash
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/0 overload
```

**Interpretación:**
- Las IPs que pasen el filtro de la ACL 1 pueden ser traducidas.  
- Se traducen usando la IP de la interfaz G0/0 con puertos únicos para cada conexión.

---

### 🔍 Verificación de NAT y ACL

```bash
show ip nat translations
show access-lists
show running-config
```

---

## 🔸 Inside y Outside en NAT

Es fundamental definir qué interfaz pertenece al **lado interno (red privada)** y cuál al **lado externo (Internet)**.

```bash
interface FastEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip nat inside

interface Serial0/0
 ip address 200.10.10.1 255.255.255.252
 ip nat outside
```

**Explicación:**
- `ip nat inside`: interfaz conectada a la red privada.  
- `ip nat outside`: interfaz conectada a Internet u otra red pública.
