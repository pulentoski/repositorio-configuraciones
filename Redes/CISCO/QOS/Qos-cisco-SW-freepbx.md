# Guía Configuración QoS en Cisco Router y Switch

## 🧠 Introducción

**QoS (Quality of Service)** es un conjunto de técnicas utilizadas en redes para **priorizar ciertos tipos de tráfico** y **garantizar la calidad en la transmisión de datos sensibles al retardo**, como la voz y el video.
En redes donde se utiliza **FreePBX** u otro sistema de telefonía IP, QoS es esencial para evitar **retardos, jitter y pérdida de paquetes** durante las llamadas.

Cisco implementa QoS a través de cuatro procesos principales:

* **Clasificación:** Identificación del tráfico por protocolo o puerto.
* **Marcado:** Etiquetado del tráfico con un valor de prioridad.
* **Priorización:** Asignación de recursos o colas específicas.
* **Control:** Aplicación de políticas que aseguran el uso eficiente del ancho de banda.

En este procedimiento se configura **QoS** y **una VLAN exclusiva de voz**, garantizando que los paquetes SIP/RTP del servidor **FreePBX** sean tratados con la máxima prioridad.

---

## ⚙️ Configuración en el Router Cisco

### 1. Crear una *Class-Map* para identificar el tráfico de voz

```bash
Router(config)# class-map match-any VOZ
Router(config-cmap)# match protocol sip
Router(config-cmap)# match protocol rtp
Router(config-cmap)# exit
```

#### 🔍 Explicación técnica

* `class-map match-any VOZ`: Crea una clase de tráfico llamada **VOZ**.
* `match protocol sip`: Identifica el tráfico de señalización SIP.
* `match protocol rtp`: Identifica el tráfico de voz RTP.
* `match-any`: Clasifica el tráfico que cumpla **cualquiera** de los criterios anteriores.

---

### 2. Crear una *Policy-Map* para priorizar el tráfico de voz

```bash
Router(config)# policy-map QOS-VOZ
Router(config-pmap)# class VOZ
Router(config-pmap-c)# priority percent 70
Router(config-pmap-c)# exit
Router(config-pmap)# class class-default
Router(config-pmap-c)# fair-queue
Router(config-pmap-c)# exit
Router(config-pmap)# exit
```

#### 🔍 Explicación técnica

* `policy-map QOS-VOZ`: Define una política global para manejar el tráfico.
* `class VOZ`: Llama a la clase creada anteriormente.
* `priority percent 70`: Reserva el **70% del ancho de banda** para la voz (cola de baja latencia).
* `class-default`: Aplica una política al resto del tráfico no clasificado.
* `fair-queue`: Asigna el ancho de banda restante de forma equitativa entre los flujos restantes.

---

### 3. Aplicar la política en la interfaz de salida

```bash
Router(config)# interface GigabitEthernet0/0
Router(config-if)# service-policy output QOS-VOZ
```

#### 🔍 Explicación técnica

* `service-policy output QOS-VOZ`: Aplica la política **en la dirección de salida** de la interfaz WAN, asegurando que el tráfico de voz salga con prioridad.

---

### 4. Verificar la configuración

```bash
Router# show policy-map interface
```

#### 🔍 Explicación técnica

* Muestra las estadísticas de paquetes clasificados por cada clase.
* Permite confirmar si los paquetes SIP y RTP están siendo detectados y priorizados.

---

## ⚙️ Configuración en el Switch Cisco

### 1. Crear la VLAN de voz

```bash
Switch(config)# vlan 20
Switch(config-vlan)# name VOZ
Switch(config-vlan)# exit
```

#### 🔍 Explicación técnica

* `vlan 20`: Crea una VLAN identificada con el número 20, reservada para voz.
* `name VOZ`: Asigna un nombre descriptivo.
* Esta VLAN separa el tráfico de voz del resto, mejorando el rendimiento y el control de QoS.

---

### 2. Activar QoS globalmente

```bash
Switch(config)# mls qos
```

#### 🔍 Explicación técnica

* `mls qos`: Activa el motor de QoS en el plano de conmutación del switch.
  A partir de este punto, el switch puede clasificar y priorizar el tráfico según los valores CoS/DSCP.

---

### 3. Configurar el puerto donde se conecta FreePBX o los teléfonos IP

```bash
Switch(config)# interface FastEthernet0/10
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config-if)# switchport voice vlan 20
Switch(config-if)# mls qos trust cos
Switch(config-if)# spanning-tree portfast
```

#### 🔍 Explicación técnica

* `switchport access vlan 10`: Asigna la VLAN de datos para el PC u otros dispositivos.
* `switchport voice vlan 20`: Asigna la VLAN de voz para el tráfico de telefonía IP.
* `mls qos trust cos`: Indica al switch que confíe en el **valor CoS (Class of Service)** marcado por el teléfono IP o el servidor.
* `spanning-tree portfast`: Optimiza la convergencia del puerto, evitando retardos al iniciar el enlace.

---

### 4. Mapear valores CoS a DSCP

```bash
Switch(config)# mls qos map cos-dscp 0 8 16 24 32 46 48 56
```

#### 🔍 Explicación técnica

* Este comando relaciona los valores **CoS (nivel 2)** con **DSCP (nivel 3)**.
* El valor **46 (EF - Expedited Forwarding)** es el estándar para tráfico de voz y garantiza prioridad absoluta en toda la red.

---

### 5. Verificación de QoS en el switch

```bash
Switch# show mls qos interface FastEthernet0/10
Switch# show mls qos maps
```

#### 🔍 Explicación técnica

* `show mls qos interface`: Muestra el estado del puerto y las estadísticas de QoS.
* `show mls qos maps`: Verifica las tablas de mapeo entre CoS y DSCP activas.

---

## 🧾 Conclusión

Con esta configuración se logra lo siguiente:

* **VLAN dedicada a voz (VLAN 20)** para aislar el tráfico VoIP.
* **QoS activo en router y switch**, garantizando prioridad a los paquetes SIP/RTP.
* **Marcado y confianza en CoS/DSCP**, manteniendo coherencia de prioridad en toda la red.

El resultado es una red optimizada para **telefonía IP con calidad estable**, evitando cortes y retardos durante las llamadas VoIP.
