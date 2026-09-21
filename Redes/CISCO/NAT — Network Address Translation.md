# 🌐 NAT — Network Address Translation

Guía técnica y educativa para comprender y configurar **NAT en routers Cisco IOS**, con especial énfasis en **PAT / NAT Overload**.

> 🎯 **Objetivo:** comprender cómo funciona NAT, identificar sus tres tipos y configurar correctamente PAT para permitir que múltiples equipos compartan una dirección IP pública.

---

# 1. 🔎 ¿Qué es NAT?

**NAT (Network Address Translation)** permite traducir direcciones IP entre una red interna y una red externa.

```text
Red privada                     Red pública

192.168.10.10  ───── NAT ─────► 203.0.113.10
```

Las principales direcciones privadas son:

| Rango            | Uso            |
| ---------------- | -------------- |
| `10.0.0.0/8`     | Redes privadas |
| `172.16.0.0/12`  | Redes privadas |
| `192.168.0.0/16` | Redes privadas |

---

# 2. 🧩 Inside y Outside

Antes de configurar NAT debemos indicar qué interfaces pertenecen a la red interna y externa.

```text
                INTERNET
                    │
                    │
              Gi0/1 │ OUTSIDE
                 ┌──┴──┐
                 │ R1  │
                 └──┬──┘
              Gi0/0 │ INSIDE
                    │
              RED INTERNA
             192.168.10.0/24
```

### Interfaz interna

```cisco
interface GigabitEthernet0/0
 ip nat inside
```

### Interfaz externa

```cisco
interface GigabitEthernet0/1
 ip nat outside
```

---

# 3. 📚 Tipos de NAT

| Tipo              | Traducción     | Uso principal            |
| ----------------- | -------------- | ------------------------ |
| 🔵 NAT Estática   | `1:1`          | Publicar servidores      |
| 🟢 NAT Dinámica   | `1:1` temporal | Utilizar un pool público |
| 🟠 PAT / Overload | `Muchos:1`     | Acceso a Internet        |

---

# 4. 🔵 NAT Estática

La NAT estática crea una relación permanente entre una IP privada y una IP pública.

```text
192.168.10.10  ◄────────►  203.0.113.10
```

### Configuración

```cisco
ip nat inside source static 192.168.10.10 203.0.113.10
```

### Uso típico

```text
Servidor Web
Servidor DNS
Servidor VPN
Servidor de correo
```

### Verificación

```cisco
show ip nat translations
```

📌 **No requiere ACL para definir la traducción.**

---

# 5. 🟢 NAT Dinámica

Utiliza un conjunto de direcciones públicas denominado **NAT Pool**.

```text
192.168.10.10 ──► 203.0.113.10
192.168.10.11 ──► 203.0.113.11
192.168.10.12 ──► 203.0.113.12
```

## 5.1 ACL

La ACL identifica qué direcciones internas pueden utilizar NAT.

```cisco
access-list 10 permit 192.168.10.0 0.0.0.255
```

## 5.2 Crear Pool

```cisco
ip nat pool PUBLIC_POOL 203.0.113.10 203.0.113.12 netmask 255.255.255.0
```

## 5.3 Asociar ACL + Pool

```cisco
ip nat inside source list 10 pool PUBLIC_POOL
```

### Flujo

```text
ACL
 ↓
Red interna
 ↓
NAT Pool
 ↓
IP pública
```

---

# 6. 🟠 PAT — NAT Overload

**PAT (Port Address Translation)** permite que múltiples equipos utilicen **una misma dirección IP pública**.

La diferencia entre las conexiones se realiza mediante los **puertos TCP/UDP**.

```text
192.168.10.10:50001 ─┐
192.168.10.11:50002 ─┤
192.168.10.12:50003 ─┼──► 203.0.113.10
192.168.10.13:50004 ─┘
```

### Relación

```text
Muchas IP privadas
        │
        ▼
   Una IP pública
        │
        ▼
 Diferentes puertos
```

📌 **PAT es la forma de NAT más utilizada para proporcionar acceso a Internet a redes privadas.**

---

# 7. 🛠️ Configuración de PAT

Ejemplo:

```text
LAN:        192.168.10.0/24
Router:     192.168.10.1
WAN:        GigabitEthernet0/1
IP pública: 203.0.113.1
```

---

## Paso 1 — Configurar Inside

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip nat inside
 no shutdown
```

---

## Paso 2 — Configurar Outside

```cisco
interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 ip nat outside
 no shutdown
```

---

## Paso 3 — Crear ACL

```cisco
access-list 10 permit 192.168.10.0 0.0.0.255
```

Esta ACL permite que:

```text
192.168.10.0/24
```

sea traducida.

---

## Paso 4 — Configurar PAT

```cisco
ip nat inside source list 10 interface GigabitEthernet0/1 overload
```

### 🔑 Comando fundamental

```cisco
ip nat inside source list <ACL> interface <INTERFAZ_WAN> overload
```

Ejemplo:

```cisco
ip nat inside source list 10 interface GigabitEthernet0/1 overload
```

---

# 8. 🧠 ¿Qué hace `overload`?

La palabra:

```text
overload
```

indica que **varias conexiones pueden utilizar simultáneamente una misma IP pública**.

Ejemplo:

```text
PC1
192.168.10.10:50001
        │
        ├────────► 203.0.113.1:30001
        │
PC2     │
192.168.10.11:50002
        │
        └────────► 203.0.113.1:30002
```

El router mantiene una tabla de traducciones para saber a qué equipo interno pertenece cada conexión.

---

# 9. 🔐 ACL para PAT

La ACL indica **qué direcciones pueden ser traducidas**.

### ACL Standard

```cisco
access-list 10 permit 192.168.10.0 0.0.0.255
```

### ACL nombrada

```cisco
ip access-list standard NAT-LAN
 permit 192.168.10.0 0.0.0.255
```

Luego:

```cisco
ip nat inside source list NAT-LAN interface GigabitEthernet0/1 overload
```

📌 Para PAT normalmente basta con una **ACL Standard** que identifique la red interna.

---

# 10. 🌐 PAT con una interfaz WAN

Esta es una de las configuraciones más habituales.

```text
              INTERNET
                  │
             203.0.113.1
                  │
             Gi0/1 OUTSIDE
               ┌─────┐
               │ R1  │
               └──┬──┘
             Gi0/0 │ INSIDE
                  │
          192.168.10.0/24
             │    │    │
            PC1  PC2  PC3
```

Configuración:

```cisco
access-list 10 permit 192.168.10.0 0.0.0.255

ip nat inside source list 10 interface GigabitEthernet0/1 overload
```

---

# 11. 🔄 PAT utilizando un Pool

PAT también puede utilizar un conjunto de direcciones públicas.

```cisco
access-list 10 permit 192.168.10.0 0.0.0.255

ip nat pool PUBLIC_POOL 203.0.113.10 203.0.113.12 netmask 255.255.255.0

ip nat inside source list 10 pool PUBLIC_POOL overload
```

La diferencia es:

```text
PAT con interfaz
        ↓
Utiliza la IP de la interfaz WAN

PAT con Pool
        ↓
Utiliza direcciones definidas en un NAT Pool
```

---

# 12. 📊 Comparación rápida

| Característica       |   Estática |     Dinámica |      PAT |
| -------------------- | ---------: | -----------: | -------: |
| Relación             |        1:1 |          1:1 | Muchos:1 |
| ACL                  |          ❌ |            ✅ |        ✅ |
| Pool                 |          ❌ |            ✅ | Opcional |
| Puertos              |          ❌ |            ❌ |        ✅ |
| Compartir IP pública |          ❌ |            ❌ |        ✅ |
| Uso habitual         | Servidores | Pool público | Internet |

---

# 13. 🔍 Verificación

### Ver traducciones

```cisco
show ip nat translations
```

### Ver estadísticas

```cisco
show ip nat statistics
```

### Ver ACL

```cisco
show access-lists
```

### Revisar configuración NAT

```cisco
show running-config | include ip nat
```

### Revisar interfaces

```cisco
show ip interface brief
```

---

# 14. 🧹 Limpiar traducciones

Para eliminar las traducciones dinámicas:

```cisco
clear ip nat translation *
```

📌 Las reglas NAT configuradas permanecen. Se eliminan las **traducciones dinámicas existentes**.

---

# 15. ⚠️ Errores frecuentes

### 1. No configurar Inside

```cisco
ip nat inside
```

### 2. No configurar Outside

```cisco
ip nat outside
```

### 3. ACL incorrecta

```cisco
show access-lists
```

### 4. No existe ruta hacia Internet

```cisco
show ip route
```

### 5. No existe ruta de retorno

El tráfico debe poder regresar hacia la red interna.

### 6. No se genera tráfico

PAT crea las traducciones cuando existe tráfico.

---

# 16. 🧩 Plantilla PAT

Para reutilizar en diferentes topologías:

```cisco
! ACL
access-list 10 permit <RED_INTERNA> <WILDCARD>

! INTERFAZ INSIDE
interface <INTERFAZ_LAN>
 ip nat inside

! INTERFAZ OUTSIDE
interface <INTERFAZ_WAN>
 ip nat outside

! PAT
ip nat inside source list 10 interface <INTERFAZ_WAN> overload
```

Ejemplo:

```cisco
access-list 10 permit 192.168.10.0 0.0.0.255

interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside

ip nat inside source list 10 interface GigabitEthernet0/1 overload
```

---

# 17. 📌 Resumen

```text
NAT
 │
 ├── 🔵 Estática
 │      └── 1 IP privada ↔ 1 IP pública
 │
 ├── 🟢 Dinámica
 │      └── IP privada ↔ IP de un Pool
 │
 └── 🟠 PAT / Overload
        └── Muchas IP privadas → 1 IP pública
```

### ⭐ Comando más importante

```cisco
ip nat inside source list 10 interface GigabitEthernet0/1 overload
```

### Recordar

```text
ACL
 ↓
Define qué red se traduce

ip nat inside
 ↓
Define la red interna

ip nat outside
 ↓
Define la red externa

overload
 ↓
Permite compartir la IP pública
```

---

## 🚀 Checklist de configuración PAT

```text
☐ Identificar interfaz LAN
☐ Identificar interfaz WAN
☐ Configurar ip nat inside
☐ Configurar ip nat outside
☐ Crear ACL
☐ Configurar PAT con overload
☐ Verificar tabla NAT
☐ Verificar estadísticas
☐ Comprobar routing
☐ Generar tráfico y comprobar traducción
```
