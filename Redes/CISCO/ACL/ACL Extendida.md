## 🔸 2. ACL Extendida

Las **ACL extendidas** permiten filtrar el tráfico por:
- IP de **origen**
- IP de **destino**
- **Tipo de protocolo** (TCP, UDP, ICMP, etc.)
- **Número de puerto**

Esto permite un **control más preciso** del tráfico de red.

**Numeración:**
- ACL extendidas numeradas: **100–199** y **2000–2699**

---

### 🧱 Ejemplo básico

```bash
access-list 110 permit tcp 192.168.1.0 0.0.0.255 any eq 80
access-list 110 deny ip any any
```

**Explicación:**
- Permite tráfico TCP desde la red 192.168.1.0/24 hacia cualquier destino en el puerto **80 (HTTP)**.  
- Niega cualquier otro tráfico IP.

---

### 🧱 Ejemplo 1: Permitir solo tráfico SSH

Permite que los dispositivos de la red interna se conecten a cualquier destino solo por el puerto **22 (SSH)**:

```bash
access-list 120 permit tcp 192.168.10.0 0.0.0.255 any eq 22
access-list 120 deny ip any any
```

**Explicación:**
- Permite conexiones TCP de origen 192.168.10.0/24 hacia cualquier destino en el puerto SSH.  
- Bloquea el resto del tráfico.

---

### 🧱 Ejemplo 2: Permitir solo tráfico Telnet

```bash
access-list 121 permit tcp 192.168.10.0 0.0.0.255 any eq 23
access-list 121 deny ip any any
```

**Explicación:**
- Permite solo el tráfico TCP en el puerto **23 (Telnet)** desde la red 192.168.10.0/24.

---

### 🧱 Ejemplo 3: Permitir SSH y Telnet, pero negar todo lo demás

```bash
access-list 122 permit tcp 192.168.10.0 0.0.0.255 any eq 22
access-list 122 permit tcp 192.168.10.0 0.0.0.255 any eq 23
access-list 122 deny ip any any
```

**Explicación:**
- Se permite solo tráfico en los puertos **22 (SSH)** y **23 (Telnet)**.  
- Se deniega cualquier otro tráfico.

---

### 🧱 Ejemplo 4: Permitir HTTP y HTTPS solamente

```bash
access-list 123 permit tcp any any eq 80
access-list 123 permit tcp any any eq 443
access-list 123 deny ip any any
```

**Explicación:**
- Permite el tráfico web (HTTP y HTTPS).  
- Niega todo lo demás.

---

### 🧱 Ejemplo 5: Bloquear ICMP (ping)

```bash
access-list 124 deny icmp any any
access-list 124 permit ip any any
```

**Explicación:**
- Bloquea todo el tráfico ICMP (ping).  
- Permite el resto del tráfico IP.

---

### 🧱 Ejemplo 6: Permitir acceso a un servidor específico

```bash
access-list 125 permit tcp any host 192.168.20.10 eq 80
access-list 125 deny ip any any
```

**Explicación:**
- Permite conexiones HTTP solo hacia el servidor **192.168.20.10**.  
- Niega cualquier otro acceso.

---

### 🧱 Ejemplo 7: Permitir una red específica hacia otra red

```bash
access-list 126 permit ip 192.168.1.0 0.0.0.255 10.10.10.0 0.0.0.255
access-list 126 deny ip any any
```

**Explicación:**
- Permite comunicación entre las redes **192.168.1.0/24** y **10.10.10.0/24**.  
- Bloquea el resto del tráfico.

---

### 💡 Aplicación de la ACL en la interfaz

Una vez creada, se aplica en una interfaz específica:

```bash
interface GigabitEthernet0/0
 ip access-group 120 in
```

**Explicación:**
- Aplica la ACL extendida número **120** en la dirección **entrante (in)** de la interfaz G0/0.
