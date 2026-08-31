# 🛡️ Manual Técnico de Instalación de pfSense CE en VirtualBox

> **Documento técnico y académico para implementación de un firewall/router virtualizado mediante Oracle VM VirtualBox.**

---

## 📋 1. Introducción

Este manual describe el procedimiento para instalar **pfSense Community Edition (CE)** en una máquina virtual utilizando **Oracle VM VirtualBox**.

La implementación considera una arquitectura de red con dos interfaces:

- **WAN:** interfaz utilizada para la comunicación con la red externa.
- **LAN:** interfaz utilizada para proporcionar conectividad a la red interna.

Durante el procedimiento se configurarán los recursos de la máquina virtual, los adaptadores de red, las interfaces WAN/LAN de pfSense y el almacenamiento virtual necesario para completar la instalación.

---

## 🎯 2. Objetivos

### Objetivo general

Implementar pfSense Community Edition como firewall y router virtualizado sobre Oracle VM VirtualBox.

### Objetivos específicos

- Crear una máquina virtual compatible con pfSense.
- Asignar recursos de procesamiento, memoria y almacenamiento.
- Configurar dos interfaces de red virtuales.
- Asignar las interfaces WAN y LAN dentro de pfSense.
- Configurar el direccionamiento de la red LAN.
- Instalar pfSense sobre el disco virtual.
- Verificar los parámetros básicos de la instalación.

---

## 🧰 3. Requisitos

### 3.1 Hardware

Para un laboratorio académico se recomienda disponer de:

| Recurso | Configuración recomendada |
|---|---:|
| CPU | 2 vCPU |
| Memoria RAM | 4 GB |
| Disco virtual | 20 GB o superior |
| Arquitectura | 64 bits |
| Interfaces de red | 2 |

> 💡 **Nota:** La cantidad de recursos puede adaptarse a las capacidades del equipo anfitrión y al propósito del laboratorio.

### 3.2 Software

- Oracle VM VirtualBox.
- Imagen ISO de **pfSense Community Edition**.
- Equipo anfitrión con arquitectura de 64 bits.

---

## 🏗️ 4. Arquitectura del laboratorio

La implementación utiliza una topología de doble interfaz. La primera interfaz proporciona conectividad WAN y la segunda constituye la red LAN administrada por pfSense.

```text
                         RED EXTERNA / INTERNET
                                  │
                                  │
                           ┌──────▼──────┐
                           │  VirtualBox │
                           │     NAT     │
                           └──────┬──────┘
                                  │
                                  │ WAN
                                  │ em0
                       ┌──────────▼──────────┐
                       │       pfSense       │
                       │   Firewall / Router │
                       │        VM           │
                       └──────────┬──────────┘
                                  │
                                  │ LAN
                                  │ em1
                                  │
                           192.168.1.1/24
                                  │
                       ┌──────────▼──────────┐
                       │      RED LAN        │
                       │  192.168.1.0/24     │
                       └─────────────────────┘
```

### 📡 Distribución de interfaces

| Interfaz | Identificador | Función | Configuración |
|---|---|---|---|
| WAN | `em0` | Red externa | DHCP |
| LAN | `em1` | Red interna | `192.168.1.1/24` |

---

# 💻 5. Fase I — Creación de la máquina virtual

## 5.1 Crear la máquina virtual

En Oracle VM VirtualBox, cree una nueva máquina virtual.

Utilice los siguientes parámetros:

| Parámetro | Valor |
|---|---|
| Nombre | `pfSense-CE` |
| Tipo | BSD |
| Versión | FreeBSD (64-bit) |
| Memoria | 4096 MB |
| CPU | 2 vCPU |
| Disco | 20 GB o superior |

---

## 5.2 Configuración de memoria

Acceda a:

```text
Configuración → Sistema → Placa base
```

Asigne:

```text
Memoria base: 4096 MB
```

La memoria puede ajustarse de acuerdo con los recursos disponibles en el equipo anfitrión.

---

## 5.3 Configuración del procesador

Acceda a:

```text
Configuración → Sistema → Procesador
```

Configure:

```text
Procesadores: 2
Límite de ejecución: 100 %
```

---

## 5.4 Configuración del almacenamiento

Cree un disco virtual para la máquina.

Como referencia para el laboratorio:

```text
Tipo: VDI
Tamaño: 20 GB o superior
Asignación: Dinámica
```

El disco será utilizado posteriormente por el instalador de pfSense.

---

# 🔌 6. Fase II — Configuración de las interfaces de red

pfSense debe disponer de dos interfaces de red independientes:

```text
Adaptador 1 → WAN
Adaptador 2 → LAN
```

---

## 6.1 Adaptador 1 — WAN

Acceda a:

```text
Configuración → Red → Adaptador 1
```

Active:

```text
Habilitar adaptador de red
```

Configure:

```text
Conectar a: NAT
```

La interfaz será utilizada como conexión WAN de pfSense.

Posteriormente, dentro de pfSense, esta interfaz será identificada como:

```text
em0
```

y funcionará como cliente DHCP.

---

## 6.2 Adaptador 2 — LAN

Acceda a:

```text
Configuración → Red → Adaptador 2
```

Active:

```text
Habilitar adaptador de red
```

Para un laboratorio aislado se recomienda utilizar:

```text
Conectar a: Red Interna
Nombre: intnet
```

Esta interfaz será utilizada como red LAN.

Dentro de pfSense será identificada como:

```text
em1
```

> ⚠️ **Importante:** La interfaz LAN debe pertenecer a una red distinta de la interfaz WAN. Esto permite que pfSense funcione como dispositivo de enrutamiento y filtrado entre ambas redes.

---

# 💿 7. Fase III — Montaje de la imagen ISO

Antes de iniciar la máquina virtual, monte la imagen ISO de pfSense.

En VirtualBox:

```text
Configuración → Almacenamiento
```

Seleccione la unidad óptica virtual y asigne la imagen ISO de pfSense.

Posteriormente, inicie la máquina virtual.

---

# 🚀 8. Fase IV — Inicio del instalador de pfSense

Una vez iniciado el sistema desde la ISO, pfSense cargará el entorno de instalación.

## 8.1 Aviso de distribución

El instalador mostrará:

```text
Copyright and Distribution Notice
```

Seleccione:

```text
[ Accept ]
```

y presione:

```text
Enter
```

---

## 8.2 Inicio de la instalación

En la pantalla:

```text
Welcome to pfSense!
```

seleccione:

```text
Install
```

y confirme mediante:

```text
[ OK ]
```

---

## 8.3 Inicialización de red

El instalador puede mostrar:

```text
Network Installation
```

Confirme:

```text
[ OK ]
```

para continuar.

---

# 🌐 9. Fase V — Configuración de interfaces de red

Durante la instalación se asignarán las interfaces virtuales de VirtualBox a las funciones WAN y LAN de pfSense.

---

## 9.1 Asignación de la interfaz WAN

En:

```text
WAN Interface Assignment
```

seleccione:

```text
em0
```

Esta interfaz corresponde al **Adaptador 1** de VirtualBox.

Posteriormente aparecerá:

```text
WAN (em0) Network Mode Setup
```

Configure:

```text
Interface Mode: DHCP (client)
VLAN: Disabled
```

Continúe con:

```text
>> Continue
```

---

## 9.2 Asignación de la interfaz LAN

En:

```text
LAN Interface Assignment
```

seleccione:

```text
em1
```

Esta interfaz corresponde al **Adaptador 2** de VirtualBox.

---

## 9.3 Configuración de la LAN

En:

```text
LAN (em1) Network Mode Setup
```

configure la red LAN:

```text
Modo: STATIC
Dirección IP: 192.168.1.1
Máscara: /24
```

El servidor DHCP de la LAN utilizará el siguiente rango:

```text
192.168.1.100 - 192.168.1.150
```

Por tanto:

```text
Red:             192.168.1.0/24
Gateway LAN:     192.168.1.1
DHCP inicial:    192.168.1.100
DHCP final:      192.168.1.150
```

---

## 9.4 Validación de interfaces

Antes de continuar, verifique que el mapeo sea:

```text
LAN → em1
WAN → em0
```

La correspondencia lógica debe quedar:

```text
VirtualBox Adaptador 1 → em0 → WAN
VirtualBox Adaptador 2 → em1 → LAN
```

---

# 💾 10. Fase VI — Selección de pfSense Community Edition

En la pantalla:

```text
Active Subscription Validation
```

seleccione:

```text
[ Install CE ]
```

Esto permite continuar con la instalación de **pfSense Community Edition**.

---

# 🗄️ 11. Fase VII — Configuración del almacenamiento

## 11.1 Opciones de instalación

En:

```text
Installation Options
```

seleccione:

```text
ZFS
GPT
```

y continúe con:

```text
>> Continue
```

---

## 11.2 Configuración de ZFS

En:

```text
ZFS Configuration
```

seleccione:

```text
stripe - Stripe - No Redundancy
```

Esta configuración es apropiada para un laboratorio que utiliza un único disco virtual.

> ⚠️ **Advertencia:** Un pool ZFS en modo `stripe` no proporciona redundancia. La pérdida del disco implica la pérdida del sistema instalado.

---

## 11.3 Selección del disco

En:

```text
Disk Selection
```

seleccione el disco virtual destinado a pfSense.

Por ejemplo:

```text
[*] ada0 20G <VBOX HARDDISK>
```

Utilice:

```text
Space
```

para marcar el disco.

Después seleccione:

```text
[ OK ]
```

y presione:

```text
Enter
```

---

# ⚠️ 12. Fase VIII — Confirmación de escritura

El instalador mostrará una advertencia indicando que el contenido del disco seleccionado será destruido.

Ejemplo:

```text
Last Chance! Are you sure you want to destroy
the current contents of the following disks:

ada0
```

Seleccione:

```text
[ Yes ]
```

> ⚠️ **Advertencia crítica:** Esta operación elimina la información existente en el disco seleccionado. Verifique que `ada0` corresponda al disco virtual destinado exclusivamente a pfSense.

---

# 📦 13. Fase IX — Instalación del sistema

## 13.1 Selección de versión

En:

```text
Software Version to Install
```

seleccione la versión de **pfSense Community Edition** disponible que corresponda al entorno de laboratorio.

Confirme mediante:

```text
[ OK ]
```

---

## 13.2 Descarga de paquetes

El instalador procederá a preparar el sistema y descargar los componentes necesarios.

Durante este proceso pueden aparecer operaciones relacionadas con:

```text
Repository
Package Catalog
pkg
Extraction
Installation
```

Espere hasta que finalice el proceso.

> 💡 **Recomendación:** No apague ni reinicie la máquina virtual durante esta etapa.

---

# 🔄 14. Fase X — Finalización de la instalación

Una vez completada la instalación:

1. Espere a que el instalador confirme la finalización.
2. Reinicie la máquina virtual cuando el instalador lo indique.
3. Retire o desmonte la ISO de instalación para evitar iniciar nuevamente el instalador.
4. Inicie pfSense desde el disco virtual instalado.

La secuencia de arranque deberá pasar desde:

```text
ISO de instalación
       ↓
Instalador pfSense
       ↓
Disco virtual
       ↓
pfSense instalado
```

---

# 🖥️ 15. Fase XI — Primer arranque

Después del reinicio, pfSense iniciará desde el disco virtual.

La consola permitirá verificar las interfaces detectadas y su asignación.

La configuración esperada es:

```text
WAN → em0
LAN → em1
```

La LAN deberá utilizar:

```text
192.168.1.1/24
```

y el servidor DHCP deberá encontrarse habilitado para el rango:

```text
192.168.1.100 - 192.168.1.150
```

---

# 🌐 16. Fase XII — Parámetros finales de red

La configuración lógica del laboratorio queda establecida de la siguiente manera:

```text
                    WAN
                 DHCP Client
                    em0
                     │
                     │
              ┌──────▼──────┐
              │   pfSense   │
              │ Firewall /  │
              │   Router    │
              └──────┬──────┘
                     │
                    em1
                     │
               192.168.1.1/24
                     │
          ┌──────────▼──────────┐
          │         LAN         │
          │   192.168.1.0/24   │
          └──────────┬──────────┘
                     │
              DHCP 100–150
```

---

# 📊 17. Matriz de configuración

| Parámetro | Configuración |
|---|---|
| Plataforma | Oracle VM VirtualBox |
| Sistema | pfSense Community Edition |
| Arquitectura | FreeBSD 64-bit |
| vCPU | 2 |
| RAM | 4096 MB |
| Disco virtual | 20 GB o superior |
| Particionado | GPT |
| Sistema de archivos | ZFS |
| ZFS Pool | Stripe |
| Adaptador 1 | WAN |
| WAN | `em0` |
| WAN Mode | DHCP Client |
| WAN VirtualBox | NAT |
| Adaptador 2 | LAN |
| LAN | `em1` |
| LAN Mode | Static |
| LAN Network | `192.168.1.0/24` |
| LAN Gateway | `192.168.1.1` |
| DHCP | Habilitado |
| DHCP Range | `192.168.1.100 - 192.168.1.150` |

---

# 🔍 18. Verificación de la instalación

Una instalación correctamente implementada debe cumplir, como mínimo, las siguientes condiciones:

### Sistema

- [ ] La máquina virtual inicia correctamente.
- [ ] pfSense inicia desde el disco virtual.
- [ ] No vuelve a iniciar el instalador ISO.

### Interfaces

- [ ] `em0` corresponde a WAN.
- [ ] `em1` corresponde a LAN.
- [ ] WAN utiliza DHCP.
- [ ] LAN utiliza `192.168.1.1/24`.

### DHCP

- [ ] El servidor DHCP está habilitado.
- [ ] El rango corresponde a `192.168.1.100–192.168.1.150`.

### Almacenamiento

- [ ] El disco virtual fue detectado.
- [ ] La instalación utiliza GPT.
- [ ] ZFS se encuentra configurado.
- [ ] El pool corresponde al modo `stripe`.

---

# ⚠️ 19. Consideraciones técnicas

## 19.1 Separación WAN/LAN

WAN y LAN deben utilizar interfaces de red independientes. La separación permite que pfSense desempeñe las funciones de:

- Enrutamiento.
- Firewall.
- Control de tráfico.
- Servidor DHCP.
- Gateway de la red LAN.

## 19.2 Uso de NAT en VirtualBox

Cuando el Adaptador 1 utiliza `NAT`, VirtualBox proporciona conectividad de salida para la interfaz WAN.

La arquitectura resultante es:

```text
Internet
   ↓
VirtualBox NAT
   ↓
pfSense WAN
   ↓
pfSense LAN
   ↓
Red interna
```

## 19.3 Red Interna para laboratorio

La utilización de `Red Interna` en el segundo adaptador permite construir una red de laboratorio aislada.

Esto resulta especialmente útil para incorporar posteriormente:

```text
PC cliente
Servidor
Windows
Linux
Servidor web
DNS
DHCP
Máquinas vulnerables
Herramientas de monitoreo
```

sin conectar directamente estos equipos a la red física.

---

# 🧪 20. Escenario de laboratorio recomendado

Una vez instalado pfSense, la topología puede ampliarse:

```text
                         INTERNET
                             │
                             │
                        VirtualBox
                           NAT
                             │
                         ┌───▼───┐
                         │ WAN   │
                         │ em0   │
                    ┌────┴───────┴────┐
                    │     pfSense     │
                    │ Firewall/Router │
                    └────┬────────────┘
                         │
                         │ em1
                         │
                  192.168.1.0/24
                         │
             ┌───────────┼───────────┐
             │           │           │
          Cliente      Servidor    Equipo
          Linux       Windows      Linux
```

Este diseño permite utilizar pfSense como componente central para prácticas de:

- 🌐 Redes.
- 🔥 Firewall.
- 🔐 Seguridad de redes.
- 📡 Enrutamiento.
- 🧩 NAT.
- 📋 ACL y reglas de filtrado.
- 🖥️ Servicios de red.
- 📊 Monitoreo.
- 🧪 Pruebas de seguridad controladas.

---

# 🎓 21. Resultado esperado

Al finalizar el procedimiento se dispondrá de una máquina virtual con **pfSense Community Edition** instalado y configurado con dos interfaces de red.

La configuración final será:

```text
                    ┌─────────────────────┐
                    │       INTERNET      │
                    └──────────┬──────────┘
                               │
                              NAT
                               │
                         ┌─────▼─────┐
                         │   em0     │
                         │    WAN    │
                         │   DHCP    │
                         ├───────────┤
                         │  pfSense  │
                         │ Firewall  │
                         │  Router   │
                         ├───────────┤
                         │    LAN    │
                         │   em1     │
                         │192.168.1.1│
                         └─────┬─────┘
                               │
                         Red Interna
                               │
                     192.168.1.0/24
                               │
                  ┌────────────┼────────────┐
                  │            │            │
               Cliente      Servidor      Cliente
```

---

# 📚 22. Conclusión

La instalación de pfSense CE sobre VirtualBox permite implementar un entorno de firewall y enrutamiento completamente virtualizado.

La configuración de dos interfaces proporciona una separación lógica entre la red externa y la red interna, mientras que el direccionamiento `192.168.1.0/24` permite establecer una LAN controlada por pfSense.

Esta infraestructura constituye una base adecuada para continuar con configuraciones posteriores de seguridad, enrutamiento, NAT, servicios de red, reglas de firewall y prácticas de administración de infraestructura.

---

## 📄 Información del documento

| Campo | Valor |
|---|---|
| Documento | Manual Técnico de Instalación de pfSense CE |
| Plataforma | Oracle VM VirtualBox |
| Sistema | pfSense Community Edition |
| Tipo | Manual de laboratorio |
| Formato | Markdown |
| Destino | Repositorio Git |
| Nivel | Técnico / Académico |

---

> 🛡️ **Manual técnico orientado a la implementación de infraestructura de red y seguridad en entornos virtualizados.**
