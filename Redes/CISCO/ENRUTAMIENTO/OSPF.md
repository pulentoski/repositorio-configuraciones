# 📘 OSPF: Configuración, Wildcard Mask y Autenticación

Guía de referencia para configurar **OSPFv2** en routers Cisco IOS, entender y calcular **wildcard masks**, y proteger el intercambio de rutas mediante **autenticación**.

---

## 🗺️ Contenido

1. ¿Qué es OSPF?
2. Conceptos clave
3. Wildcard mask: qué es y cómo se calcula
4. Configuración básica
5. Autenticación OSPF
6. Autenticación por interfaz vs. por área
7. Ejemplo completo: dos routers con MD5
8. Requisitos de adyacencia
9. Verificación
10. Diagnóstico de fallas
11. Área 0 y Router ID
12. Buenas prácticas
13. Resumen de comandos

---

## 1. 📖 ¿Qué es OSPF?

**OSPF (Open Shortest Path First)** es un protocolo de enrutamiento dinámico de tipo **Link-State (estado de enlace)**.

🧭 **Idea central:** cada router OSPF mantiene una copia del **mapa completo** de la red (la LSDB). Con ese mapa calcula por su cuenta el camino más corto hacia cada destino, de forma similar a un GPS que conoce todas las calles.

| Característica | Valor |
|---|---|
| Tipo | Link-State |
| Algoritmo | Dijkstra / SPF (Shortest Path First) |
| Métrica | Costo, basado en el ancho de banda |
| Diseño | Jerárquico, por áreas |
| Área principal | Área 0 (backbone) |
| Distancia administrativa (Cisco) | 110 |

### 📊 Cálculo del costo

```text
Costo = Ancho de banda de referencia / Ancho de banda de la interfaz
Referencia por defecto = 100 Mbps
```

| Interfaz | Cálculo | Costo |
|---|---|---|
| Ethernet (10 Mbps) | 100 / 10 | 10 |
| FastEthernet (100 Mbps) | 100 / 100 | 1 |
| GigabitEthernet (1000 Mbps) | 100 / 1000 | 1 (mínimo posible) |

> ⚠️ Con la referencia por defecto, FastEthernet y GigabitEthernet obtienen el mismo costo. En redes modernas se ajusta con `auto-cost reference-bandwidth 10000`, usando el mismo valor en todos los routers del dominio.

---

## 2. 🧠 Conceptos clave

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Process ID** | Número local del proceso OSPF. No necesita coincidir entre routers | `router ospf 1` |
| **Router ID** | Identificador único del router en el dominio OSPF (formato IPv4) | `1.1.1.1` |
| **Área** | Grupo lógico de redes que comparten la misma LSDB | `area 0` |
| **LSDB** | Base de datos con el "mapa" de la topología | `show ip ospf database` |
| **LSA** | Anuncio de estado de enlace; las piezas que forman la LSDB | — |
| **Vecino** | Router OSPF directamente conectado con el que se intercambia información | `show ip ospf neighbor` |
| **Wildcard mask** | Máscara que indica qué bits de una dirección deben coincidir | `0.0.0.255` |

### 🤝 Estados de una vecindad

Dos routers pasan por varios estados antes de quedar sincronizados:

```text
DOWN → INIT → 2-WAY → EXSTART → EXCHANGE → LOADING → FULL ✅
```

| Estado | Qué significa |
|---|---|
| DOWN | No se han recibido paquetes Hello |
| INIT | Se recibió un Hello, pero el vecino aún no nos reconoce |
| 2-WAY | Ambos se reconocen. En redes multiacceso se elige DR/BDR |
| EXSTART / EXCHANGE | Se negocia y se intercambia un resumen de la LSDB |
| LOADING | Se solicitan los LSA faltantes |
| **FULL** | LSDB sincronizada. La vecindad está operativa |

> 💡 Si la autenticación no coincide, los Hellos se descartan y la vecindad **no avanza de DOWN**. El vecino simplemente no aparece.

---

## 3. 🎭 Wildcard Mask

### 3.1 ¿Qué es?

La **wildcard mask** le indica al router **qué bits de una dirección debe comparar y cuáles puede ignorar**. En OSPF se usa en el comando `network` para decidir en qué interfaces se activa el protocolo.

| Bit en la wildcard | Significado |
|---|---|
| **0** | El bit **debe coincidir** |
| **1** | El bit **se ignora** (puede ser cualquier valor) |

🧭 **Idea central:** funciona como un filtro de búsqueda. Buscar `192.168.1.*` significa "los tres primeros octetos deben ser exactos, el último puede ser cualquiera". En wildcard, eso se escribe `0.0.0.255`.

> ⚠️ **No confundir con la máscara de subred.** Son lógicamente opuestas:
> - Máscara de subred → `1` = parte de red, `0` = parte de host.
> - Wildcard → `0` = debe coincidir, `1` = se ignora.

### 3.2 ¿Cómo se calcula?

**Método rápido: restar la máscara a 255.255.255.255**

```text
  255.255.255.255
- Máscara de subred
-------------------
= Wildcard mask
```

**Ejemplo 1 — Red /24**

```text
  255.255.255.255
- 255.255.255.0
-------------------
    0.  0.  0.255   → Wildcard: 0.0.0.255
```

**Ejemplo 2 — Red /26**

```text
  255.255.255.255
- 255.255.255.192
-------------------
    0.  0.  0. 63   → Wildcard: 0.0.0.63
```

**Ejemplo 3 — Enlace punto a punto /30**

```text
  255.255.255.255
- 255.255.255.252
-------------------
    0.  0.  0.  3   → Wildcard: 0.0.0.3
```

**Ejemplo 4 — Red /20 (el cálculo afecta al tercer octeto)**

```text
  255.255.255.255
- 255.255.240.0
-------------------
    0.  0. 15.255   → Wildcard: 0.0.15.255
```

### 3.3 Visto en binario

Red `192.168.1.64/26`:

```text
Máscara /26 : 11111111.11111111.11111111.11000000 = 255.255.255.192
Wildcard    : 00000000.00000000.00000000.00111111 = 0.0.0.63
              └─────── deben coincidir ───────┘└ignora┘
```

Cada bit de la wildcard es la **inversión** del bit correspondiente en la máscara.

Con este resultado:

```bash
network 192.168.1.64 0.0.0.63 area 0
```

OSPF se activa en toda interfaz cuya IP esté entre **192.168.1.64 y 192.168.1.127**.

### 3.4 Casos especiales

| Wildcard | Efecto | Uso típico |
|---|---|---|
| `0.0.0.0` | Debe coincidir la IP exacta | Activar OSPF en **una sola interfaz** |
| `255.255.255.255` | Coincide con cualquier IP | Activar OSPF en **todas** las interfaces (no recomendado) |

```bash
! Solo la interfaz con IP 192.168.1.1
network 192.168.1.1 0.0.0.0 area 0
```

> 💡 Usar `0.0.0.0` con la IP exacta de la interfaz es la forma más precisa y evita activar OSPF por accidente en interfaces no deseadas.

### 3.5 Tabla de referencia

| Prefijo | Máscara de subred | Wildcard | Hosts útiles |
|---|---|---|---|
| /8 | 255.0.0.0 | 0.255.255.255 | 16.777.214 |
| /16 | 255.255.0.0 | 0.0.255.255 | 65.534 |
| /20 | 255.255.240.0 | 0.0.15.255 | 4.094 |
| /24 | 255.255.255.0 | 0.0.0.255 | 254 |
| /25 | 255.255.255.128 | 0.0.0.127 | 126 |
| /26 | 255.255.255.192 | 0.0.0.63 | 62 |
| /27 | 255.255.255.224 | 0.0.0.31 | 30 |
| /28 | 255.255.255.240 | 0.0.0.15 | 14 |
| /29 | 255.255.255.248 | 0.0.0.7 | 6 |
| /30 | 255.255.255.252 | 0.0.0.3 | 2 |
| /32 | 255.255.255.255 | 0.0.0.0 | 1 (host) |

### 3.6 Comprobación rápida

¿El comando `network 10.0.0.0 0.0.255.255 area 0` activa OSPF en estas interfaces?

| IP de la interfaz | ¿Coincide? | Motivo |
|---|---|---|
| 10.0.5.1 | ✅ Sí | Los dos primeros octetos (10.0) coinciden |
| 10.0.200.9 | ✅ Sí | Los dos primeros octetos (10.0) coinciden |
| 10.1.0.1 | ❌ No | El segundo octeto es 1, no 0 |

---

## 4. ⚙️ Configuración básica

```bash
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
```

| Comando | Qué hace |
|---|---|
| `router ospf 1` | Inicia el proceso OSPF con Process ID 1 (valor local) |
| `router-id 1.1.1.1` | Asigna manualmente el identificador del router |
| `network 10.0.0.0 0.0.0.255 area 0` | Activa OSPF en interfaces de 10.0.0.0/24 y las asigna al Área 0 |
| `network 192.168.1.0 0.0.0.255 area 0` | Activa OSPF en interfaces de 192.168.1.0/24 y las asigna al Área 0 |

> 💡 El comando `network` **no anuncia una red directamente**: activa OSPF en las interfaces que coinciden. Luego OSPF anuncia la red configurada en esas interfaces.

### Alternativa: activar OSPF desde la interfaz

```bash
interface GigabitEthernet0/0
 ip ospf 1 area 0
```

Este método evita el cálculo de wildcard y deja explícito qué interfaz participa en OSPF.

---

## 5. 🔐 Autenticación OSPF

Sin autenticación, cualquier equipo conectado a un segmento OSPF podría formar vecindad y **inyectar rutas falsas**. La autenticación verifica que los mensajes provienen de un vecino que conoce la clave configurada.

### Tipos de autenticación en OSPFv2

| Tipo | Nombre | Seguridad | Comentario |
|---|---|---|---|
| 0 | Null | ❌ Ninguna | Comportamiento por defecto |
| 1 | Simple password | ⚠️ Muy baja | La clave viaja en texto plano; visible con Wireshark |
| 2 | MD5 | 🟡 Media | Clave no viaja; se envía un hash del mensaje + clave |
| — | HMAC-SHA (key chain) | ✅ Alta | Disponible en IOS 15.4(1)T y posteriores (RFC 5709) |

### 5.1 Tipo 1 — Contraseña simple

```bash
interface GigabitEthernet0/0
 ip ospf authentication
 ip ospf authentication-key MiClavePlana
```

> ⚠️ La contraseña viaja **sin protección** dentro del paquete. Cualquier captura de tráfico la revela. No se recomienda en entornos productivos.

### 5.2 Tipo 2 — MD5

```bash
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

| Elemento | Descripción |
|---|---|
| `1` | Key ID. Debe coincidir en ambos extremos |
| `md5` | Algoritmo utilizado |
| `ClaveSecreta` | Clave compartida entre vecinos |

🧭 **Cómo funciona:** el router calcula un resumen (hash) del paquete OSPF junto con la clave y lo adjunta. El receptor repite el cálculo con su propia clave; si ambos resultados coinciden, el mensaje es válido y no fue alterado.

> ⚠️ **MD5 no cifra el paquete ni la clave.** Solo aporta autenticación e integridad. El contenido OSPF sigue siendo visible en una captura, pero la clave no.

### 5.3 HMAC-SHA con key chain (recomendado si el IOS lo soporta)

```bash
key chain OSPF-KEYS
 key 1
  key-string ClaveSegura
  cryptographic-algorithm hmac-sha-256
!
interface GigabitEthernet0/0
 ip ospf authentication key-chain OSPF-KEYS
```

---

## 6. 📊 Autenticación por interfaz vs. por área

### 6.1 Por interfaz

El requerimiento y la clave se configuran directamente en cada interfaz.

```bash
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

### 6.2 Por área

El requerimiento se define en el proceso OSPF y aplica a **todas las interfaces del área**. La clave sigue configurándose en cada interfaz.

```bash
router ospf 1
 area 0 authentication message-digest
!
interface GigabitEthernet0/0
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

> 💡 La configuración en la interfaz **tiene prioridad** sobre la del área. Una interfaz puede excluirse de la política del área con `ip ospf authentication null`.

### 6.3 Comparación

| Característica | Por interfaz | Por área |
|---|---|---|
| Alcance | Una interfaz | Todas las interfaces del área |
| Dónde se activa | `interface` | `router ospf` |
| Dónde va la clave | En la interfaz | En cada interfaz |
| Flexibilidad | Alta | Menor |
| Uso recomendado | Control granular por enlace | Política uniforme en toda el área |

```text
Por interfaz                    Por área

Router                                Área 0
 ├── G0/0 → MD5                          │
 ├── G0/1 → Sin autenticación   ┌────────┼────────┐
 └── G0/2 → MD5                G0/0     G0/1     G0/2
                                MD5      MD5      MD5
```

---

## 7. 🖥️ Ejemplo completo: dos routers con MD5

### Topología

```text
   10.0.0.0/24                192.168.1.0/24              172.16.1.0/24
  [LAN R1] ──── R1 G0/1   R1 G0/0 ════════ R2 G0/0   R2 G0/1 ──── [LAN R2]
                          .1     (MD5)       .2
             Router ID: 1.1.1.1              Router ID: 2.2.2.2
```

### R1

```bash
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
 passive-interface GigabitEthernet0/1
!
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

### R2

```bash
router ospf 1
 router-id 2.2.2.2
 network 192.168.1.0 0.0.0.255 area 0
 network 172.16.1.0 0.0.0.255 area 0
 passive-interface GigabitEthernet0/1
!
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

> 💡 `passive-interface` anuncia la red LAN pero **no envía Hellos** hacia ella, evitando que un equipo de usuario intente formar vecindad.

### Parámetros que deben coincidir en el enlace

```text
Tipo:    MD5
Key ID:  1
Clave:   ClaveSecreta
Área:    0
Subred:  192.168.1.0/24
```

### Resultado esperado

```text
R1# show ip ospf neighbor
Neighbor ID   Pri   State      Dead Time   Address       Interface
2.2.2.2         1   FULL/DR    00:00:35    192.168.1.2   GigabitEthernet0/0
```

---

## 8. 🤝 Requisitos de adyacencia

Para formar vecindad, ambos extremos del enlace deben coincidir en:

| Parámetro | Si no coincide… |
|---|---|
| Área | No se forma vecindad |
| Subred y máscara | No se forma vecindad |
| Hello / Dead timers | No se forma vecindad |
| Tipo de autenticación | Los Hellos se descartan |
| Clave y Key ID | Los Hellos se descartan |
| Tipo de red OSPF | Vecindad inestable o rutas incorrectas |
| MTU | Queda atascada en EXSTART / EXCHANGE |
| Router ID | Debe ser **distinto**; si se repite, hay conflicto |

---

## 9. 🔎 Verificación

| Comando | Para qué sirve |
|---|---|
| `show ip ospf neighbor` | Ver vecinos y su estado (se espera **FULL**) |
| `show ip route ospf` | Ver rutas aprendidas por OSPF (marcadas con `O`) |
| `show ip ospf database` | Ver el contenido de la LSDB |
| `show ip protocols` | Ver Router ID, redes configuradas y áreas |
| `show ip ospf interface GigabitEthernet0/0` | Ver área, timers, tipo de red, vecinos y autenticación |

En `show ip ospf interface`, una autenticación MD5 activa se muestra así:

```text
  Message digest authentication enabled
    Youngest key id is 1
```

---

## 10. 🛠️ Diagnóstico de fallas

### Flujo de revisión

```text
¿Aparece el vecino en show ip ospf neighbor?
 │
 ├── NO → ¿La interfaz está up/up?
 │         ¿Hay conectividad IP (ping)?
 │         ¿Coinciden área, subred y timers?
 │         ¿Coincide la autenticación (tipo, Key ID, clave)?
 │         ¿La interfaz está marcada como passive por error?
 │
 └── SÍ → ¿Está en FULL?
           ├── Atascado en EXSTART/EXCHANGE → revisar MTU
           ├── En 2-WAY → normal entre DROTHERs en redes multiacceso
           └── FULL → revisar show ip route ospf
```

### Depuración de autenticación

```bash
debug ip ospf adj
```

Mensajes típicos:

| Mensaje | Causa |
|---|---|
| `Mismatched Authentication type` | Un extremo usa MD5 y el otro no (o usa tipo 1) |
| `Mismatched Authentication Key - Message Digest Key 1` | La clave no coincide |
| `No message digest key 1 on interface` | El Key ID no coincide o no está configurado |

> ⚠️ Desactivar la depuración al terminar con `undebug all`, especialmente en equipos productivos.

---

## 11. 🌐 Área 0 y Router ID

### Área 0 (backbone)

En un diseño multiárea, **todas las áreas deben conectarse al Área 0**. El tráfico entre áreas siempre pasa por el backbone.

```text
        Área 1          Área 2
           │               │
          ABR             ABR
           └──── Área 0 ───┘
                (backbone)
```

Los routers que conectan un área con el backbone se denominan **ABR (Area Border Router)**. Si un área no puede conectarse físicamente al Área 0, se utiliza un **Virtual Link** como solución lógica.

### Router ID

Si no se configura manualmente, IOS lo elige en este orden:

1. Valor configurado con `router-id`.
2. IP más alta de una interfaz **loopback** activa.
3. IP más alta de una interfaz física activa.

> 💡 Tras cambiar el Router ID, el cambio se aplica al reiniciar el proceso con `clear ip ospf process`. Este comando reinicia las vecindades.

---

## 12. 🛡️ Buenas prácticas

* Configurar **Router ID fijos y únicos**.
* Preferir wildcard `0.0.0.0` con la IP exacta, o `ip ospf <proceso> area <área>` en la interfaz, para no activar OSPF por accidente.
* Usar `passive-interface` en interfaces hacia usuarios finales.
* Aplicar autenticación en todos los enlaces entre routers.
* Preferir **HMAC-SHA** si el IOS lo soporta; si no, MD5. Evitar la contraseña simple.
* Usar claves robustas y no reutilizarlas entre dominios.
* Ajustar `auto-cost reference-bandwidth` igual en todos los routers si hay enlaces de 1 Gbps o más.
* Verificar vecindades antes de probar conectividad de extremo a extremo.
* Documentar Router ID, áreas, redes, interfaces y parámetros de autenticación.

---

## 13. 📋 Resumen de comandos

| Función | Comando |
|---|---|
| Iniciar OSPF | `router ospf 1` |
| Router ID | `router-id 1.1.1.1` |
| Activar OSPF en red | `network 10.0.0.0 0.0.0.255 area 0` |
| Activar OSPF en interfaz | `ip ospf 1 area 0` |
| Interfaz pasiva | `passive-interface GigabitEthernet0/1` |
| Ajustar referencia de costo | `auto-cost reference-bandwidth 10000` |
| Autenticación simple | `ip ospf authentication` |
| Contraseña simple | `ip ospf authentication-key MiClavePlana` |
| MD5 en interfaz | `ip ospf authentication message-digest` |
| Clave MD5 | `ip ospf message-digest-key 1 md5 ClaveSecreta` |
| MD5 en área | `area 0 authentication message-digest` |
| Excluir interfaz de autenticación | `ip ospf authentication null` |
| Ver vecinos | `show ip ospf neighbor` |
| Ver rutas OSPF | `show ip route ospf` |
| Ver LSDB | `show ip ospf database` |
| Ver protocolos | `show ip protocols` |
| Ver OSPF en interfaz | `show ip ospf interface GigabitEthernet0/0` |
| Depurar adyacencias | `debug ip ospf adj` |
| Reiniciar proceso | `clear ip ospf process` |

---

## 🎯 Idea clave

Una red OSPF bien configurada no solo **aprende rutas**: también **forma vecindades confiables, mantiene una LSDB coherente y protege el intercambio de información de enrutamiento**. La wildcard mask define dónde participa OSPF; la autenticación define con quién.
