# 🔐 Guía de Implementación de TACACS+ en Docker + GNS3

> **Documento técnico-académico para laboratorio de redes Cisco**  
> Objetivo: levantar un servidor Linux con **TACACS+** dentro de un contenedor Docker y utilizarlo desde **GNS3** para administrar la autenticación, autorización y auditoría de routers y switches Cisco.

---

## 🎯 Objetivo del laboratorio

La propuesta consiste en utilizar un servidor Linux dentro de un contenedor Docker para proporcionar el servicio **TACACS+** a una topología de laboratorio en GNS3.

La idea general del escenario es:

```text
                         ┌─────────────────────────┐
                         │   Servidor Linux        │
                         │   Docker + TACACS+      │
                         │   IP: 192.168.1.100     │
                         └────────────┬────────────┘
                                      │
                                      │ TACACS+ / TCP 49
                                      │
                              ┌───────┴───────┐
                              │    Switch     │
                              └───┬───────┬───┘
                                  │       │
                              ┌───┘       └───┐
                              │               │
                         ┌────▼────┐     ┌────▼────┐
                         │ Router 1│     │ Router 2│
                         └─────────┘     └─────────┘
```

En el escenario académico también se contempla:

- 🖥️ Un Linux con entorno gráfico para administrar **Zabbix**.
- 📊 Un servidor Zabbix conectado a la infraestructura.
- 🔐 El mismo servidor Linux puede ejecutar **TACACS+**.
- 🌐 Dos routers y dos switches Cisco administrados mediante AAA/TACACS+.

---

# 1. 🔐 ¿Qué es TACACS+?

**TACACS+** (*Terminal Access Controller Access-Control System Plus*) es un protocolo de red utilizado para centralizar el control de acceso a dispositivos de infraestructura, como routers y switches.

Conceptualmente, funciona como un **guardia de seguridad centralizado** para los equipos de red.

Por ejemplo, si existen muchos equipos Cisco, en lugar de crear los usuarios manualmente en cada router y switch, estos pueden definirse en el servidor TACACS+.

Cuando un usuario intenta ingresar a un dispositivo, el equipo Cisco consulta al servidor TACACS+:

```text
Usuario → Router/Switch → Servidor TACACS+
                         │
                         ├── ¿Existe el usuario?
                         ├── ¿La contraseña es correcta?
                         ├── ¿Qué privilegios tiene?
                         └── ¿Qué comandos puede ejecutar?
```

## 🧩 Modelo AAA

TACACS+ se utiliza junto con el modelo **AAA**:

| AAA | Función |
|---|---|
| 🔑 **Authentication** | Determina quién es el usuario. Comprueba usuario y contraseña. |
| 🛂 **Authorization** | Determina qué puede hacer el usuario. |
| 📝 **Accounting** | Registra las acciones realizadas por el usuario. |

Por ejemplo:

- `diego` → administrador total.
- `seba` → usuario limitado, orientado a consultas.
- `juan` → usuario con permisos de modificación.

El **Accounting** permite mantener registros de las actividades realizadas, lo cual resulta especialmente útil en un entorno académico para identificar las acciones efectuadas por cada alumno.

---

# 2. ⚠️ Análisis de la configuración original

La configuración inicial presenta algunas incoherencias que deben corregirse antes de utilizarla.

## 2.1 🔴 Errores críticos en TACACS+ — Servidor

### Grupo `trollmaster`

La configuración original utiliza:

```text
default services = deny
```

Sin embargo, el comando `enable` solo permite la escalada de privilegios y no otorga por sí mismo autorización para ejecutar comandos de configuración.

Además, el bloque:

```text
cmd = configure
```

está estructurado de forma que puede impedir la autorización de los subcomandos ejecutados dentro del modo global (`configure terminal`).

Sin permisos adecuados para los subcomandos, el usuario `juan` puede quedar bloqueado al intentar realizar cambios.

### ❌ Error sintáctico

La configuración original contiene:

```text
accouting file
```

Debe utilizarse:

```text
accounting file
```

El error puede impedir que `tac_plus` inicie correctamente.

### ⚠️ Incompatibilidad de nombres de grupos

El usuario `diego` está asociado al grupo:

```text
admins
```

Pero los equipos Cisco deben estar configurados correctamente para utilizar AAA y obtener el nivel de privilegio correspondiente desde TACACS+.

---

# 3. 🌐 Inconsistencias en los equipos Cisco

## 3.1 Switch `sw_dsj`

La configuración presenta:

```text
interface Vlan1
 ip address 192.168.1.9 255.255.255.0
```

pero el gateway original era:

```text
ip default-gateway 192.168.100.1
```

Esto pertenece a una red diferente.

Si el switch está en:

```text
192.168.1.0/24
```

y el servidor TACACS+ está en:

```text
192.168.1.100
```

el gateway debe pertenecer a la misma red, por ejemplo:

```text
ip default-gateway 192.168.1.1
```

---

## 3.2 🔧 Sintaxis TACACS+ antigua y moderna

El switch utiliza la sintaxis:

```text
tacacs-server host 192.168.1.100 key 12345
```

Mientras que el router utiliza la sintaxis moderna:

```text
tacacs server TAC
```

y:

```text
aaa group server tacacs+ default
```

Es importante mantener coherencia entre la definición del servidor y la forma en que las listas AAA lo referencian.

---

## 3.3 ⚠️ Método AAA en VTY y consola

Las líneas `line vty` y `line con` utilizan la lista:

```text
jetblack
```

pero la configuración debe acompañarse de autorización EXEC, por ejemplo:

```text
aaa authorization exec default group tacacs+ local
```

De lo contrario, un usuario autenticado puede ingresar con privilegio 1 aunque su perfil TACACS+ tenga asignado un privilegio superior.

---

# 4. 🧱 Configuración base de TACACS+

La siguiente configuración corresponde a una base limpia para el servidor:

```text
accounting file = /var/log/tac_plus.acct
key = 12345

group = admins {
    default service = permit
    service = exec {
        priv-lvl = 15
    }
}

group = limited {
    default service = deny
    service = exec {
        priv-lvl = 1
    }
    cmd = show {
        permit ip
        permit interface
        permit running-config
        deny .*
    }
}

group = trollmaster {
    default service = deny
    service = exec {
        priv-lvl = 15
    }
    cmd = configure {
        permit .*
    }

    # Permitir comandos globales
    cmd = interface { permit .* }
    cmd = router { permit .* }
}

user = diego {
    member = admins
    login = cleartext diego
}

user = seba {
    member = limited
    login = cleartext seba
}

user = juan {
    member = trollmaster
    login = cleartext juan
}

user = $enable$ {
    login = cleartext cisco1
}
```

> 🔐 **Nota académica:** las contraseñas mostradas son de laboratorio. No deben utilizarse como credenciales reales en un entorno de producción.

---

# 5. 🖧 ¿Puede el mismo servidor utilizarse para TACACS+ y Zabbix?

Sí. La propuesta es utilizar un único Linux con entorno gráfico para dos funciones:

### 📊 Zabbix

El navegador web del Linux permite acceder a la interfaz gráfica de Zabbix para realizar tareas de monitoreo.

### 🔐 TACACS+

El servicio `tac_plus` funciona en segundo plano y atiende las solicitudes de autenticación de los routers y switches Cisco.

El servidor puede, por tanto, desempeñar ambas funciones:

```text
┌───────────────────────────────────────────┐
│            Linux con entorno gráfico      │
│                                           │
│   ┌───────────────┐   ┌───────────────┐   │
│   │    Zabbix     │   │    TACACS+    │   │
│   │  Monitoreo    │   │  Autenticación│   │
│   └───────────────┘   └───────┬───────┘   │
│                               │           │
└───────────────────────────────┼───────────┘
                                │ TCP/49
                       ┌────────┴────────┐
                       │ Routers/Switches│
                       └─────────────────┘
```

Esto permite aprovechar mejor los recursos disponibles en GNS3.

---

# 6. 🐳 Arquitectura del contenedor

La recomendación para el laboratorio es **crear el TACACS+ dentro de la imagen Docker**, en lugar de instalarlo manualmente cada vez que se inicia el contenedor.

La estructura será:

```text
tacacs-gns3-lab/
├── Dockerfile
├── tac_plus.conf
└── entrypoint.sh
```

### ¿Por qué?

Docker utiliza un `Dockerfile` como una receta de construcción.

Al ejecutar:

```bash
docker build -t tacacs-server:v1 .
```

se crea una imagen que contiene:

- Ubuntu 22.04.
- TACACS+.
- Herramientas básicas de red.
- Configuración TACACS+.
- Script de inicio.

Esto permite reproducir el servidor de forma consistente.

---

# 7. 💻 Software necesario

## 🪟 Windows 10 / 11

Debe instalarse:

| Software | Función |
|---|---|
| 🐳 **Docker Desktop** | Construcción y ejecución de contenedores |
| 🐧 **WSL2** | Backend Linux utilizado por Docker Desktop |
| 🌐 **GNS3** | Simulación de la infraestructura de red |
| 🖥️ **GNS3 VM** | Entorno recomendado para ejecutar nodos |

---

## 🐧 Linux

En una distribución basada en Ubuntu/Debian:

```bash
sudo apt update
sudo apt install docker.io
```

Se recomienda disponer además de:

- Docker Engine.
- GNS3.
- GNS3 VM cuando corresponda.

---

# 8. 📁 Crear la carpeta del proyecto

## 🐧 Linux

Abrir una terminal:

```bash
mkdir tacacs-gns3-lab
cd tacacs-gns3-lab
```

---

## 🪟 Windows — PowerShell

Abrir PowerShell:

```powershell
mkdir tacacs-gns3-lab
cd tacacs-gns3-lab
```

La estructura inicial será:

```text
tacacs-gns3-lab/
```

---

# 9. 📄 Crear el `Dockerfile`

## 🐧 Linux

Utilizar `nano`:

```bash
nano Dockerfile
```

Pegar el siguiente contenido:

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tacacs+ \
    iproute2 \
    iputils-ping \
    nano \
    && rm -rf /var/lib/apt/lists/*

COPY tac_plus.conf /etc/tacacs+/tac_plus.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 49

ENTRYPOINT ["/entrypoint.sh"]
```

Guardar:

```text
Ctrl + O
Enter
Ctrl + X
```

---

## 🪟 Windows — PowerShell

Ejecutar:

```powershell
notepad Dockerfile
```

Cuando Windows pregunte si desea crear el archivo, seleccionar **Sí**.

Pegar el contenido anterior y guardar.

> ⚠️ En Windows debe verificarse que el archivo se llame exactamente `Dockerfile` y no `Dockerfile.txt`.

---

# 10. 📄 Crear `entrypoint.sh`

Este archivo controla el inicio del contenedor.

## 🐧 Linux

```bash
nano entrypoint.sh
```

Contenido:

```bash
#!/bin/bash
echo "Verificando sintaxis de TACACS+..."
tac_plus -P /etc/tacacs+/tac_plus.conf

if [ $? -eq 0 ]; then
    echo "Sintaxis correcta. Iniciando servicio TACACS+..."
    exec tac_plus -G -c /etc/tacacs+/tac_plus.conf
else
    echo "ERROR en la configuración de TACACS+."
    exit 1
fi
```

Guardar:

```text
Ctrl + O
Enter
Ctrl + X
```

---

## 🪟 Windows — PowerShell

Ejecutar:

```powershell
notepad entrypoint.sh
```

Pegar exactamente el contenido anterior y guardar.

> ⚠️ El archivo debe conservar el nombre `entrypoint.sh`.

---

# 11. 📄 Crear `tac_plus.conf`

Este es el archivo principal de configuración de TACACS+.

## 🐧 Linux

```bash
nano tac_plus.conf
```

Pegar:

```text
accounting file = /var/log/tac_plus.acct
key = 12345

group = admins {
    default service = permit
    service = exec {
        priv-lvl = 15
    }
}

group = limited {
    default service = deny
    service = exec {
        priv-lvl = 1
    }
    cmd = show {
        permit ip
        permit interface
        permit running-config
        deny .*
    }
}

user = diego {
    member = admins
    login = cleartext diego
}

user = seba {
    member = limited
    login = cleartext seba
}
```

---

## 🪟 Windows — PowerShell

Ejecutar:

```powershell
notepad tac_plus.conf
```

Pegar exactamente la configuración anterior y guardar.

> ⚠️ Verificar nuevamente que Windows no agregue `.txt` al nombre.

---

# 12. 🔎 Verificar los archivos

Antes de construir la imagen, la carpeta debe contener:

```text
tacacs-gns3-lab/
├── Dockerfile
├── tac_plus.conf
└── entrypoint.sh
```

### Linux

```bash
ls -l
```

### Windows

```powershell
dir
```

---

# 13. 🏗️ Construir la imagen Docker

Una vez creados los tres archivos, ejecutar el comando desde la carpeta:

```text
tacacs-gns3-lab
```

## 🐧 Linux

```bash
sudo docker build -t tacacs-server:v1 .
```

## 🪟 Windows — PowerShell

```powershell
docker build -t tacacs-server:v1 .
```

El punto `.` al final es importante porque indica que Docker debe utilizar la carpeta actual como contexto de construcción.

---

# 14. 📦 Exportar la imagen

Para transportar la imagen a otro equipo o incorporarla posteriormente en GNS3:

## 🐧 Linux

```bash
sudo docker save -o tacacs-server.tar tacacs-server:v1
```

## 🪟 Windows — PowerShell

```powershell
docker save -o tacacs-server.tar tacacs-server:v1
```

Se generará:

```text
tacacs-server.tar
```

Este archivo contiene la imagen Docker.

---

# 15. 🧪 Probar el contenedor

Antes de llevarlo a GNS3, es recomendable comprobar que la imagen puede ejecutarse.

Ejemplo:

```bash
docker run --name tacacs-test tacacs-server:v1
```

Para consultar los contenedores:

```bash
docker ps
```

Para detenerlo:

```bash
docker stop tacacs-test
```

Para eliminarlo:

```bash
docker rm tacacs-test
```

---

# 16. 🌐 Puerto utilizado por TACACS+

TACACS+ utiliza:

```text
TCP/49
```

Por eso el `Dockerfile` contiene:

```dockerfile
EXPOSE 49
```

La comunicación conceptual será:

```text
Cisco Router/Switch
        │
        │ TCP/49
        ▼
192.168.1.100
TACACS+ Server
```

---

# 17. 🧩 Importar el contenedor en GNS3

En GNS3:

```text
Edit
  └── Preferences
       └── Docker Containers
            └── New
```

Seleccionar:

```text
Import an image file
```

y seleccionar:

```text
tacacs-server.tar
```

Asignar:

```text
Name: TACACS_Server
Interfaces: 1
```

Finalizar la importación.

---

# 18. 🖥️ Incorporar el servidor a la topología

Una vez importado:

1. Arrastrar `TACACS_Server` al proyecto.
2. Conectarlo al switch.
3. Configurar su interfaz de red.
4. Comprobar si el contenedor obtiene automáticamente una dirección IP mediante **DHCP**.

## 🌐 Obtener una IP automáticamente

Un contenedor puede utilizar **DHCP** para obtener su dirección IP desde un servidor DHCP disponible en la red a la que está conectado.

En un laboratorio GNS3, esto resulta especialmente útil cuando la topología ya dispone de un router o servidor DHCP.

Dentro del contenedor se puede solicitar una dirección mediante:

```bash
dhclient eth0
```

Luego comprobar la dirección asignada:

```bash
ip addr show eth0
```

o:

```bash
ip -4 addr show eth0
```

También se puede comprobar la conectividad mediante:

```bash
ip route
```

y:

```bash
ping 192.168.1.1
```

### 🔎 Ejemplo

Si existe un servidor DHCP en la red:

```text
                 DHCP
                  │
                  │
             ┌────▼────┐
             │ Switch   │
             └────┬────┘
                  │
             ┌────▼────────────┐
             │ TACACS_Server   │
             │ DHCP → IP       │
             └─────────────────┘
```

El contenedor podría recibir, por ejemplo:

```text
IP:       192.168.1.100
MASK:     255.255.255.0
GATEWAY:  192.168.1.1
```

> ⚠️ **Importante:** DHCP no significa que el contenedor vaya a recibir necesariamente `192.168.1.100`. La dirección dependerá del servidor DHCP y de su configuración.

## 🧪 Verificar si DHCP está disponible

Ejecutar:

```bash
ip addr
```

Si `eth0` ya tiene una dirección IPv4, comprobar:

```bash
ip route
```

Si no tiene dirección, se puede intentar:

```bash
dhclient eth0
```

Si `dhclient` no está instalado en la imagen, será necesario agregar el paquete correspondiente al `Dockerfile` o utilizar el mecanismo DHCP disponible en la distribución.

### 📌 DHCP versus IP fija

Para el laboratorio existen dos alternativas:

| Método | Ventaja | Desventaja |
|---|---|---|
| 🌐 **DHCP** | Configuración automática y sencilla | La IP puede cambiar |
| 🔒 **IP fija** | La dirección del servidor TACACS+ siempre es conocida | Requiere configuración manual |

Para **TACACS+**, una IP fija suele ser más conveniente, porque los routers y switches Cisco deben saber a qué dirección enviar las solicitudes de autenticación.

Por ejemplo:

```text
TACACS+ Server
IP: 192.168.1.100
TCP: 49
```

Por esta razón, **DHCP es excelente para pruebas iniciales**, pero para el escenario de evaluación se recomienda reservar una dirección mediante DHCP o utilizar una IP fija.

## 🔒 Alternativa recomendada: reserva DHCP

Una solución intermedia consiste en configurar el servidor DHCP para que siempre entregue la misma dirección al contenedor.

Conceptualmente:

```text
MAC del contenedor
       │
       ▼
Servidor DHCP
       │
       └── Siempre entrega → 192.168.1.100
```

De esta manera se mantiene la comodidad de DHCP, pero el servidor TACACS+ conserva una dirección conocida.

---

## 🛠️ Configuración con IP fija

Si no existe DHCP en la topología, se puede utilizar una dirección fija.

La configuración de red propuesta es:

```text
IP:
192.168.1.100

Máscara:
255.255.255.0

Gateway:
192.168.1.1
```

> ⚠️ La dirección `192.168.1.100` debe estar disponible y pertenecer a la misma red utilizada por los equipos que necesitan comunicarse con TACACS+.

---

# 19. 🔧 Configuración del Switch

El switch puede utilizar:

```cisco
interface Vlan1
 ip address 192.168.1.9 255.255.255.0
!
ip default-gateway 192.168.1.1
```

El objetivo es que el switch pueda alcanzar:

```text
192.168.1.100
```

---

# 20. 🔐 Configuración AAA en Cisco

La configuración base propuesta es:

```cisco
aaa new-model
aaa authentication login jetblack group tacacs+ local
aaa authentication enable default group tacacs+ enable
aaa authorization exec default group tacacs+ local
aaa authorization commands 15 default group tacacs+ local
aaa accounting exec default start-stop group tacacs+
aaa accounting commands 15 default start-stop group tacacs+
```

Estas líneas permiten implementar:

- 🔑 Autenticación.
- 🛂 Autorización EXEC.
- 🛠️ Autorización de comandos de privilegio 15.
- 📝 Accounting de sesiones EXEC.
- 📝 Accounting de comandos.

---

# 21. 🧠 ¿Cómo encaja todo?

La arquitectura final queda conceptualmente así:

```text
                         GNS3
                          │
             ┌────────────┴────────────┐
             │                         │
       ┌─────▼─────┐             ┌─────▼─────┐
       │  Switch 1 │             │  Switch 2 │
       │            │             │            │
       │   Zabbix  │             │ Linux GUI  │
       └─────┬──────┘             │ TACACS+    │
             │                    └─────┬──────┘
             │                          │
             └──────────┬───────────────┘
                        │
                 ┌──────▼──────┐
                 │   Router 1  │
                 └─────────────┘

                 ┌─────────────┐
                 │   Router 2  │
                 └─────────────┘
```

El servidor Linux puede concentrar servicios para el laboratorio:

```text
Linux
├── 🖥️ Entorno gráfico
├── 📊 Zabbix
└── 🔐 TACACS+
```

---

# 22. ♻️ ¿Sirve el servidor para cualquier laboratorio?

Sí, la idea es utilizarlo como una **plantilla reutilizable**.

El servidor puede mantenerse como imagen base y posteriormente adaptarse a diferentes topologías.

Para una nueva práctica normalmente será necesario modificar:

- 🌐 Dirección IP del servidor.
- 👤 Usuarios.
- 👥 Grupos.
- 🔐 Clave compartida.
- 🛂 Permisos.
- 🖧 Configuración AAA de los nuevos routers y switches.

Los routers y switches nuevos deben configurarse para conocer:

```text
IP del servidor TACACS+
Clave compartida
Métodos AAA
Listas de autenticación
Listas de autorización
Accounting
```

---

# 23. 🎓 Aplicación en una evaluación

Una posible evaluación puede utilizar:

```text
                ┌─────────────────┐
                │ Linux + Zabbix  │
                │     TACACS+     │
                └────────┬────────┘
                         │
                    ┌────▼────┐
                    │ Switch 1│
                    └────┬────┘
                         │
                 ┌───────┴───────┐
                 │               │
             ┌───▼───┐       ┌───▼───┐
             │Router1│       │Router2│
             └───────┘       └───────┘
                         │
                    ┌────▼────┐
                    │ Switch 2│
                    └─────────┘
```

Los alumnos podrían trabajar sobre:

1. 🌐 Configuración IP.
2. 🔗 Conectividad.
3. 🔐 Configuración AAA.
4. 🖥️ Integración con TACACS+.
5. 🛂 Autenticación.
6. 👥 Roles y privilegios.
7. 📝 Accounting.
8. 📊 Monitoreo mediante Zabbix.
9. 🧪 Pruebas de acceso y autorización.

---

# 24. 🧪 Comprobaciones fundamentales

Antes de configurar los equipos Cisco con TACACS+, comprobar:

### Desde el servidor

```bash
ping 192.168.1.9
```

### Desde el Cisco

```cisco
ping 192.168.1.100
```

La conectividad IP debe funcionar antes de intentar solucionar problemas de AAA.

La secuencia recomendada es:

```text
1. 🟢 Docker funciona
       ↓
2. 🟢 TACACS+ inicia
       ↓
3. 🟢 Interfaz tiene IP
       ↓
4. 🟢 Cisco alcanza al servidor
       ↓
5. 🟢 TCP/49 disponible
       ↓
6. 🟢 AAA configurado
       ↓
7. 🟢 Usuario autenticado
       ↓
8. 🟢 Autorización aplicada
       ↓
9. 🟢 Accounting registrado
```

---

# 25. 📌 Resumen de archivos

| Archivo | Función |
|---|---|
| `Dockerfile` | 🐳 Define cómo se construye la imagen |
| `entrypoint.sh` | ▶️ Verifica la configuración e inicia TACACS+ |
| `tac_plus.conf` | 🔐 Define usuarios, grupos, permisos y clave |
| `tacacs-server.tar` | 📦 Imagen exportada para transportar/importar |

---

# 26. 🧭 Flujo completo

```text
                    DESARROLLO
                         │
                         ▼
              Crear archivos del proyecto
                         │
                         ▼
                    Dockerfile
                 tac_plus.conf
                 entrypoint.sh
                         │
                         ▼
                 docker build
                         │
                         ▼
                Imagen Docker
                         │
                         ▼
                  docker save
                         │
                         ▼
               tacacs-server.tar
                         │
                         ▼
                       GNS3
                         │
                         ▼
                Importar imagen
                         │
                         ▼
                 TACACS_Server
                         │
                         ▼
                Configurar IP
                         │
                         ▼
              Conectar a Switch
                         │
                         ▼
             Configurar AAA en Cisco
                         │
                         ▼
               Probar autenticación
                         │
                         ▼
             🟢 Laboratorio operativo
```

---

# ⚠️ Consideraciones técnicas

- El servidor TACACS+ debe tener conectividad IP con los equipos Cisco.
- La IP puede obtenerse mediante DHCP para pruebas, aunque para TACACS+ se recomienda una dirección conocida y estable.
- La clave compartida configurada en TACACS+ debe coincidir con la configurada en los equipos Cisco.
- El puerto de TACACS+ es **TCP/49**.
- La configuración AAA debe ser coherente entre routers, switches y servidor.
- La configuración mostrada utiliza credenciales simples porque corresponde a un laboratorio académico.
- Para producción deben utilizarse credenciales y políticas de seguridad adecuadas.
- Antes de aplicar AAA en equipos remotos, se recomienda mantener un método local de respaldo para evitar perder el acceso administrativo.

---

# 📚 Resultado esperado

Al finalizar esta primera etapa se debe disponer de una imagen Docker reutilizable:

```text
tacacs-server:v1
```

y, opcionalmente, de su archivo transportable:

```text
tacacs-server.tar
```

El siguiente paso del laboratorio corresponde a la **configuración de los routers y switches Cisco para utilizar TACACS+ mediante AAA**, seguida de las pruebas de autenticación, autorización y accounting.

---

> 🧑‍🏫 **Enfoque académico:** esta guía está planteada para que el servidor TACACS+ pueda ser construido una vez y posteriormente reutilizado en diferentes prácticas y evaluaciones dentro de GNS3.
