## 🔸 1. ACL Estándar

Las **ACL estándar** se utilizan para **filtrar tráfico basándose únicamente en la dirección IP de origen**.  
No permiten especificar protocolos ni puertos.

**Numeración:**
- ACL estándar numeradas: **1–99** y **1300–1999**

---

### 📘 Características principales

- Filtran **solo por IP de origen**.  
- Son más simples y ligeras que las extendidas.  
- Se aplican normalmente **cerca del destino** para evitar bloqueos innecesarios.  
- Pueden usarse también con NAT (para definir qué direcciones serán traducidas).

---

### 🧱 Ejemplo básico

```bash
access-list 10 deny 192.168.1.100
access-list 10 permit any
```

**Explicación:**
- Bloquea el tráfico proveniente de la IP 192.168.1.100.  
- Permite el resto del tráfico.

---

### 🧱 Ejemplo 1: Permitir una IP específica y denegar todo lo demás

Permite el tráfico solo desde la dirección IP **192.168.1.10** y bloquea el resto.

```bash
access-list 10 permit host 192.168.1.10
access-list 10 deny any
```

**Explicación:**
- `access-list 10 permit host 192.168.1.10`: Permite el tráfico de esa IP.  
- `access-list 10 deny any`: Bloquea todo lo demás.

---

### 🧱 Ejemplo 2: Permitir una red completa y denegar el resto

Permite todo el tráfico proveniente de la red **192.168.1.0/24** y bloquea el resto.

```bash
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 deny any
```

**Explicación:**
- Permite tráfico desde la red 192.168.1.0/24.  
- Niega el resto del tráfico.

---

### 🧱 Ejemplo 3: Permitir múltiples redes

Permite tráfico desde varias redes específicas.

```bash
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 permit 192.168.2.0 0.0.0.255
access-list 10 deny any
```

**Explicación:**
- Se permiten las redes 192.168.1.0/24 y 192.168.2.0/24.  
- Se bloquean todas las demás.

---

### 🧱 Ejemplo 4: Permitir solo un rango de IPs dentro de una red

Usando una **máscara wildcard** se puede definir un rango de direcciones.

```bash
access-list 10 permit 192.168.1.1 0.0.0.19
access-list 10 deny any
```

**Explicación:**
- Permite solo las IPs desde 192.168.1.1 hasta 192.168.1.20.  
- Bloquea el resto.

---

### 🧱 Ejemplo 5: Bloquear una IP específica y permitir el resto

```bash
access-list 10 deny host 192.168.1.50
access-list 10 permit any
```

**Explicación:**
- Bloquea el tráfico de 192.168.1.50.  
- Permite todo el resto.

---

### 🧱 Ejemplo 6: Usar ACL estándar con NAT

```bash
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/0 overload
```

**Explicación:**
- Las IPs que coincidan con la ACL 1 pueden ser traducidas (NAT).  
- Se usa la IP pública de la interfaz G0/0.

---

### 💡 Aplicación de la ACL en la interfaz

Una vez creada la ACL, se aplica en una interfaz y dirección específica:

```bash
interface GigabitEthernet0/1
 ip access-group 10 in
```

**Explicación:**
- Aplica la ACL número 10 en la dirección **entrante (in)** de la interfaz G0/1.
