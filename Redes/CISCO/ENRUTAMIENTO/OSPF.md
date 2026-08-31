# 📘 Configuración y Autenticación del Protocolo de Enrutamiento OSPF

## 📖 1. Descripción General

Este documento describe la configuración del protocolo **OSPF (Open Shortest Path First)** en routers Cisco.

OSPF es un protocolo de enrutamiento dinámico de tipo **Link-State (Estado de Enlace)**, utilizado para determinar la mejor ruta hacia cada red dentro de un sistema autónomo mediante el cálculo del **costo** asociado a los enlaces.

El cálculo de las rutas se realiza mediante el algoritmo **Dijkstra**, también denominado **SPF (Shortest Path First)**.

Además de proporcionar enrutamiento dinámico, OSPF incorpora mecanismos de **autenticación entre routers vecinos**, permitiendo proteger el intercambio de información de enrutamiento frente a dispositivos no autorizados.

---

## ⚙️ 2. Características Principales

* 🔗 **Tipo de protocolo:** Link-State (Estado de Enlace).
* 🧮 **Algoritmo:** Dijkstra (SPF – Shortest Path First).
* 📊 **Métrica:** Costo, basado por defecto en el ancho de banda del enlace.
* 🏗️ **Arquitectura jerárquica:** OSPF permite dividir el dominio de enrutamiento en diferentes áreas.
* 🌐 **Área 0:** Corresponde al **backbone** o área principal de OSPF.
* 📈 **Escalabilidad:** La utilización de múltiples áreas permite segmentar redes extensas y reducir la carga de procesamiento y memoria de los routers.
* 🤝 **Formación de vecindades:** Los routers OSPF establecen relaciones de vecindad para intercambiar información de estado de enlace.
* 🗄️ **Base de datos LSDB:** Cada router mantiene una **Link-State Database (LSDB)** con información sobre la topología conocida.
* 🔐 **Autenticación:** OSPF permite autenticar los mensajes intercambiados entre routers vecinos mediante diferentes mecanismos.
* 🔄 **Convergencia:** OSPF puede adaptar las rutas cuando se producen cambios en la topología de la red.

---

## ⚙️ 3. Configuración Básica de OSPF

### 🖥️ 3.1 Habilitar OSPF en el Router

Una configuración básica de OSPF en un router Cisco puede realizarse mediante los siguientes comandos:

```bash
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
```

### 🔎 3.2 Explicación de los Comandos

#### `router ospf 1`

Inicia el proceso OSPF en el router.

El número `1` corresponde al **Process ID**, utilizado para identificar el proceso OSPF localmente dentro del router.

> 💡 **Importante:** El Process ID no tiene que coincidir necesariamente entre routers para que puedan establecer una vecindad OSPF.

---

#### `router-id 1.1.1.1`

Asigna manualmente un identificador al router dentro del dominio OSPF.

El `router-id` utiliza el formato de una dirección IPv4, pero su función principal es **identificar al router dentro del proceso OSPF**, no proporcionar conectividad IP.

Configurar el `router-id` manualmente facilita la administración, el monitoreo y el diagnóstico de la red.

---

#### `network 10.0.0.0 0.0.0.255 area 0`

Indica a OSPF que debe activarse en las interfaces cuyas direcciones IP coincidan con el rango definido por:

* Red: `10.0.0.0`
* Wildcard Mask: `0.0.0.255`
* Área: `0`

La wildcard mask permite identificar las interfaces que pertenecen a la red `10.0.0.0/24`.

---

#### `network 192.168.1.0 0.0.0.255 area 0`

Activa OSPF en las interfaces que pertenecen a la red `192.168.1.0/24` y las incorpora al **Área 0**.

Si dicha interfaz está conectada a otro router OSPF configurado correctamente, podrá utilizarse para establecer una relación de vecindad.

---

## 🔐 4. Autenticación en OSPF

La autenticación OSPF permite verificar que los mensajes OSPF recibidos provienen de un vecino que posee la configuración de autenticación correspondiente.

Su objetivo es proteger el intercambio de información de enrutamiento frente a dispositivos que intenten participar de forma no autorizada en el dominio OSPF.

La autenticación puede configurarse de manera **granular por interfaz** o mediante una política de autenticación asociada a un **área OSPF**.

---

## 🔐 4.1 Tipos de Autenticación OSPF

En OSPFv2 se encuentran los siguientes tipos de autenticación:

### 0️⃣ Tipo 0 — Null Authentication

No utiliza autenticación.

Es el comportamiento predeterminado cuando no se configura ningún mecanismo de autenticación.

---

### 1️⃣ Tipo 1 — Simple Password

Utiliza una contraseña simple para autenticar los mensajes OSPF.

La contraseña se incorpora al paquete OSPF sin proporcionar la protección criptográfica de mecanismos como MD5.

Por esta razón, **no se recomienda para entornos donde se requiera un nivel adecuado de seguridad**.

Configuración:

```bash
interface GigabitEthernet0/0
 ip ospf authentication
 ip ospf authentication-key MiClavePlana
```

#### 🔎 Explicación

* `ip ospf authentication`: habilita la autenticación en la interfaz.
* `ip ospf authentication-key MiClavePlana`: establece la contraseña utilizada para la autenticación.

---

### 2️⃣ Tipo 2 — MD5 Authentication

La autenticación MD5 utiliza una **clave secreta compartida** para generar un resumen criptográfico asociado al mensaje OSPF.

El objetivo es permitir que el receptor compruebe que el mensaje fue generado utilizando la clave correspondiente y que su contenido no fue alterado.

> ⚠️ **Importante:** MD5 en OSPF **no cifra el paquete OSPF ni la contraseña**. Se utiliza como mecanismo de autenticación e integridad mediante un resumen criptográfico.

En configuraciones Cisco IOS tradicionales, MD5 se habilita mediante:

```bash
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

---

# 🔐 5. Autenticación MD5 a Nivel de Interfaz

La autenticación MD5 puede configurarse directamente sobre una interfaz determinada.

Este método proporciona un control **granular**, ya que permite decidir individualmente qué interfaces utilizarán autenticación y qué claves serán utilizadas en cada enlace.

### ⚙️ Configuración

```bash
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

### 🔎 Explicación de los comandos

#### `ip ospf authentication message-digest`

Activa la autenticación mediante **Message Digest**, utilizando MD5 en la interfaz seleccionada.

```bash
ip ospf authentication message-digest
```

---

#### `ip ospf message-digest-key 1 md5 ClaveSecreta`

Define la clave que será utilizada para la autenticación.

```bash
ip ospf message-digest-key 1 md5 ClaveSecreta
```

Los elementos del comando son:

| Elemento       | Descripción                            |
| -------------- | -------------------------------------- |
| `1`            | Identificador de la clave o **Key ID** |
| `md5`          | Algoritmo utilizado                    |
| `ClaveSecreta` | Clave compartida entre los routers     |

### 💡 Ventajas de la autenticación por interfaz

* 🎯 Permite controlar individualmente cada enlace.
* 🔑 Permite utilizar diferentes claves en diferentes interfaces.
* 🛡️ Facilita la aplicación selectiva de políticas de seguridad.
* ⚙️ Es apropiada cuando no todas las interfaces del router requieren la misma política de autenticación.

---

# 🔐 6. Autenticación MD5 a Nivel de Área

OSPF también permite establecer el requerimiento de autenticación mediante la configuración del área.

Este mecanismo permite definir que las interfaces pertenecientes a determinada área deben utilizar autenticación MD5.

### ⚙️ Paso 1 — Habilitar autenticación MD5 para el área

```bash
router ospf 1
 area 0 authentication message-digest
```

El comando:

```bash
area 0 authentication message-digest
```

establece el requerimiento de autenticación MD5 para el **Área 0** dentro del proceso OSPF correspondiente.

---

### 🔑 Paso 2 — Configurar la clave en la interfaz

La clave continúa siendo configurada en el contexto de cada interfaz:

```bash
interface GigabitEthernet0/0
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

Por lo tanto, aunque el requerimiento de autenticación se establezca a nivel del área, la **clave concreta se configura en cada interfaz participante**.

### 📌 Características

* 🌐 Permite establecer una política de autenticación para un área.
* ⚙️ Facilita la administración cuando existen múltiples interfaces dentro de una misma área.
* 🔑 La clave continúa asociándose a cada interfaz.
* 🤝 Todos los routers que deban establecer vecindad deben utilizar una configuración compatible.

---

# 📊 7. Diferencia entre Autenticación por Interfaz y por Área

| Característica             | Nivel de Interfaz                   | Nivel de Área                         |
| -------------------------- | ----------------------------------- | ------------------------------------- |
| 🎯 Alcance                 | Una interfaz específica             | Interfaces pertenecientes al área     |
| ⚙️ Configuración principal | `interface`                         | `router ospf`                         |
| 🔧 Flexibilidad            | Alta                                | Menor                                 |
| 📋 Administración          | Interfaz por interfaz               | Política asociada al área             |
| 🔑 Clave                   | Se configura en la interfaz         | Se configura en cada interfaz         |
| 🏢 Uso recomendado         | Cuando se requiere control granular | Cuando se desea una política uniforme |

### 🧠 Resumen conceptual

**Autenticación por interfaz:**

```text
Router
 ├── G0/0 → MD5
 ├── G0/1 → Sin autenticación
 └── G0/2 → MD5
```

**Autenticación por área:**

```text
             Área 0
                │
       ┌────────┼────────┐
       │        │        │
     G0/0     G0/1     G0/2
       │        │        │
      MD5      MD5      MD5
```

La diferencia fundamental está en **dónde se establece el requerimiento de autenticación**.

---

# 🖥️ 8. Configuración Completa de Dos Routers con Autenticación MD5

A continuación se presenta un ejemplo de configuración entre dos routers Cisco.

La red `192.168.1.0/24` será utilizada como segmento de conexión entre ambos routers.

## 🖥️ 8.1 Router 1 — R1

```bash
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0

interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

R1 utiliza:

* `1.1.1.1` como Router ID.
* `10.0.0.0/24` como red interna.
* `192.168.1.0/24` como red de interconexión.
* Área `0`.
* MD5 con `Key ID 1`.
* Clave compartida `ClaveSecreta`.

---

## 🖥️ 8.2 Router 2 — R2

```bash
router ospf 1
 router-id 2.2.2.2
 network 192.168.1.0 0.0.0.255 area 0
 network 172.16.1.0 0.0.0.255 area 0

interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

R2 utiliza:

* `2.2.2.2` como Router ID.
* `192.168.1.0/24` como red de interconexión.
* `172.16.1.0/24` como red interna.
* Área `0`.
* MD5 con `Key ID 1`.
* La misma clave compartida `ClaveSecreta`.

---

# 🤝 9. Requisitos para Establecer una Adyacencia OSPF

Para que dos routers OSPF establezcan correctamente una relación de vecindad, deben existir parámetros compatibles entre ambos extremos del enlace.

Entre los principales parámetros se encuentran:

* 🌐 **Área OSPF:** debe ser compatible en el enlace.
* 🔐 **Tipo de autenticación:** debe coincidir.
* 🔑 **Clave de autenticación:** debe coincidir.
* 🆔 **Key ID:** debe corresponder cuando se utiliza autenticación MD5.
* 📡 **Máscara de red:** debe ser compatible.
* ⏱️ **Temporizador Hello:** debe coincidir.
* ⏱️ **Temporizador Dead:** debe coincidir.
* 🔗 **Tipo de red OSPF:** debe ser compatible.
* 🟢 **Interfaces activas:** las interfaces deben encontrarse operativas y participar en OSPF.

### 🔑 Ejemplo de configuración compatible

Router 1:

```bash
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

Router 2:

```bash
interface GigabitEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSecreta
```

Los parámetros fundamentales de autenticación son equivalentes:

```text
Tipo:       MD5
Key ID:     1
Clave:      ClaveSecreta
```

> ⚠️ **Si alguno de estos parámetros no coincide, la autenticación fallará y la vecindad OSPF no podrá establecerse correctamente.**

---

# 🔎 10. Comandos de Verificación y Diagnóstico

Una vez configurado OSPF, es necesario verificar tanto el funcionamiento del protocolo como la formación de las vecindades.

## `show ip route ospf`

Muestra las rutas aprendidas mediante OSPF que fueron incorporadas a la tabla de enrutamiento.

```bash
show ip route ospf
```

Permite comprobar si las redes remotas están siendo aprendidas correctamente.

---

## `show ip ospf neighbor`

Muestra los routers vecinos detectados mediante OSPF.

```bash
show ip ospf neighbor
```

Una vecindad correctamente establecida normalmente debe alcanzar el estado:

```text
FULL
```

---

## `show ip ospf database`

Muestra información de la **Link-State Database (LSDB)**.

```bash
show ip ospf database
```

Permite analizar la información de estado de enlace utilizada por OSPF para construir la representación de la topología.

---

## `show ip protocols`

Muestra información general de los protocolos de enrutamiento configurados.

```bash
show ip protocols
```

Permite revisar, entre otros elementos:

* Router ID.
* Redes anunciadas.
* Áreas.
* Procesos de enrutamiento.
* Parámetros generales de OSPF.

---

## `show ip ospf interface GigabitEthernet0/0`

Permite consultar información detallada de OSPF en una interfaz específica.

```bash
show ip ospf interface GigabitEthernet0/0
```

Puede utilizarse para revisar información relacionada con:

* Área OSPF.
* Estado de la interfaz.
* Temporizadores.
* Vecinos.
* Tipo de red.
* Autenticación.

---

# 🛠️ 11. Diagnóstico de Problemas de Autenticación

Cuando dos routers OSPF no establecen una vecindad, la configuración de autenticación debe revisarse cuidadosamente.

### 🔐 Comprobar el tipo de autenticación

Ambos extremos deben utilizar el mismo método.

Por ejemplo:

```bash
ip ospf authentication message-digest
```

debe corresponder con una configuración MD5 en el router vecino.

---

### 🔑 Comprobar el Key ID

Ejemplo:

```bash
ip ospf message-digest-key 1 md5 ClaveSecreta
```

El `Key ID` utilizado debe ser compatible entre ambos extremos.

---

### 🔐 Comprobar la clave

La clave debe ser exactamente la misma:

```text
Router 1 → ClaveSecreta
Router 2 → ClaveSecreta
```

Una diferencia en la clave impedirá la autenticación.

---

### 🌐 Comprobar el área

Por ejemplo:

```bash
network 192.168.1.0 0.0.0.255 area 0
```

El enlace utilizado para establecer la vecindad debe pertenecer al área correspondiente.

---

### ⏱️ Comprobar los temporizadores

Los temporizadores Hello y Dead deben ser compatibles entre los routers vecinos.

Estos parámetros pueden revisarse mediante:

```bash
show ip ospf interface GigabitEthernet0/0
```

---

# 🌐 12. Consideraciones sobre el Área 0

El **Área 0** corresponde al backbone de OSPF.

En una arquitectura OSPF de múltiples áreas, las comunicaciones entre diferentes áreas deben utilizar el backbone como elemento central de interconexión.

Una representación simplificada sería:

```text
                 Área 1
                   │
                   │
              ┌────┴────┐
              │  Área 0 │
              │ Backbone│
              └────┬────┘
                   │
                   │
                 Área 2
```

El diseño jerárquico mediante áreas permite mejorar la escalabilidad y limitar el alcance de determinada información de estado de enlace.

Cuando un área no puede conectarse físicamente al Área 0, OSPF contempla mecanismos como el **Virtual Link** para proporcionar conectividad lógica con el backbone.

---

# 🆔 13. Importancia del Router ID

El `router-id` identifica de manera lógica al router dentro del dominio OSPF.

Una configuración explícita facilita:

* 🔎 La identificación de routers.
* 🛠️ El diagnóstico de problemas.
* 🗄️ El análisis de la LSDB.
* 🤝 La interpretación de las vecindades.
* 📊 La administración de redes de mayor tamaño.

Ejemplo:

```bash
router ospf 1
 router-id 1.1.1.1
```

Otro router podría utilizar:

```bash
router ospf 1
 router-id 2.2.2.2
```

Cada router debe poseer un identificador único dentro del dominio OSPF.

---

# 🛡️ 14. Buenas Prácticas

* 🆔 Utilizar **Router ID fijos y únicos**.
* 🌐 Mantener una planificación clara de las áreas OSPF.
* 🏗️ Utilizar el **Área 0** como backbone de la arquitectura OSPF.
* 🔐 Aplicar autenticación en los enlaces donde sea necesario proteger el intercambio de información de enrutamiento.
* 🛡️ Preferir mecanismos de autenticación más robustos disponibles en la plataforma y versión de IOS utilizada.
* ⚠️ Evitar utilizar autenticación mediante contraseña simple en entornos donde la seguridad sea un requisito.
* 🔑 Utilizar claves seguras y evitar reutilizarlas innecesariamente en diferentes dominios o enlaces.
* 🤝 Verificar la formación de las vecindades antes de realizar pruebas de conectividad de extremo a extremo.
* 📋 Comprobar la tabla de enrutamiento después de establecer las adyacencias.
* 🔎 Utilizar comandos de diagnóstico como `show ip ospf neighbor`, `show ip ospf database` y `show ip ospf interface`.
* 📝 Documentar los `Router ID`, áreas, redes, interfaces y parámetros de autenticación utilizados.

---

# 📋 15. Resumen de Comandos

| Función                         | Comando                                         |
| ------------------------------- | ----------------------------------------------- |
| ⚙️ Iniciar OSPF                 | `router ospf 1`                                 |
| 🆔 Configurar Router ID         | `router-id 1.1.1.1`                             |
| 🌐 Incorporar red a OSPF        | `network 10.0.0.0 0.0.0.255 area 0`             |
| 🔐 Activar MD5 en interfaz      | `ip ospf authentication message-digest`         |
| 🔑 Configurar clave MD5         | `ip ospf message-digest-key 1 md5 ClaveSecreta` |
| 🌐 Activar MD5 para un área     | `area 0 authentication message-digest`          |
| 🔓 Activar autenticación simple | `ip ospf authentication`                        |
| 🔑 Configurar contraseña simple | `ip ospf authentication-key MiClavePlana`       |
| 🛣️ Ver rutas OSPF              | `show ip route ospf`                            |
| 🤝 Ver vecinos OSPF             | `show ip ospf neighbor`                         |
| 🗄️ Ver LSDB                    | `show ip ospf database`                         |
| 📊 Ver protocolos               | `show ip protocols`                             |
| 🔎 Ver OSPF en interfaz         | `show ip ospf interface GigabitEthernet0/0`     |

---

# 🧠 16. Conceptos Fundamentales

Para comprender correctamente la configuración de OSPF y su autenticación, es importante diferenciar los siguientes conceptos:

| Concepto             | Función                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| ⚙️ **Process ID**    | Identifica localmente el proceso OSPF                                                            |
| 🆔 **Router ID**     | Identifica al router dentro del dominio OSPF                                                     |
| 🌐 **Area ID**       | Determina el área OSPF a la que pertenece una interfaz                                           |
| 🎯 **Wildcard Mask** | Determina las interfaces donde se activará OSPF mediante el comando `network`                    |
| 🗄️ **LSDB**         | Base de datos que contiene información del estado de los enlaces                                 |
| 🧮 **SPF**           | Algoritmo utilizado para calcular las mejores rutas                                              |
| 📊 **Costo**         | Métrica utilizada por OSPF para seleccionar rutas                                                |
| 🤝 **Neighbor**      | Router OSPF con el cual se establece una relación de vecindad                                    |
| 🔑 **Key ID**        | Identificador de una clave utilizada en autenticación MD5                                        |
| 🔐 **MD5**           | Mecanismo criptográfico utilizado para autenticar mensajes OSPF en configuraciones tradicionales |
| 🌐 **Área 0**        | Backbone de una arquitectura OSPF de múltiples áreas                                             |

---

# 🎓 17. Conclusión

OSPF es un protocolo de enrutamiento dinámico basado en estado de enlace que permite construir una representación de la topología de red y calcular las rutas óptimas mediante el algoritmo SPF.

Su arquitectura basada en áreas proporciona escalabilidad, mientras que mecanismos como la autenticación permiten proteger el intercambio de información entre routers vecinos.

La autenticación MD5 puede implementarse directamente sobre una interfaz o mediante una política asociada a un área OSPF. En ambos casos, es fundamental mantener una configuración compatible entre los routers que necesitan establecer una vecindad.

Una configuración OSPF correctamente implementada debe considerar no solamente la declaración de redes y áreas, sino también parámetros como **Router ID, autenticación, Key ID, claves, temporizadores, interfaces y mecanismos de verificación**.

> 🎓 **Idea clave:** Una red OSPF correctamente configurada no solo debe ser capaz de **aprender rutas**, sino también de **establecer vecindades confiables, mantener una base de datos coherente y proteger el intercambio de información de enrutamiento**.
