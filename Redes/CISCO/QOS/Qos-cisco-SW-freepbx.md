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

### 1. Crear una ACL extendida para identificar el tráfico de voz
```bash
Router(config)# access-list 100 permit udp any any eq 5060
Router(config)# access-list 100 permit udp any any range 5061 5062
Router(config)# access-list 100 permit udp any any range 10000 20000
```

#### 🔍 Explicación técnica

* `access-list 100`: Crea una ACL extendida numerada para clasificar tráfico.
* `permit udp any any eq 5060`: Identifica el tráfico de señalización **SIP** (puerto UDP 5060).
* `permit udp any any range 5061 5062`: Identifica tráfico SIP adicional (puertos UDP 5061-5062).
* `permit udp any any range 10000 20000`: Identifica el tráfico de voz **RTP** (puertos UDP 10000-20000).
* **Nota:** Ajusta el rango RTP según la configuración de tu FreePBX (Settings → Asterisk SIP Settings → RTP Port Range).

---

### 2. Crear una *Class-Map* para identificar el tráfico de voz
```bash
Router(config)# class-map match-any VOZ
Router(config-cmap)# match access-group 100
Router(config-cmap)# exit
```

#### 🔍 Explicación técnica

* `class-map match-any VOZ`: Crea una clase de tráfico llamada **VOZ**.
* `match access-group 100`: Clasifica el tráfico que coincida con la ACL 100 (SIP/RTP).
* `match-any`: Clasifica el tráfico que cumpla **cualquiera** de los criterios de la ACL.

---

### 3. Crear una *Policy-Map* para priorizar el tráfico de voz
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
* `priority percent 70`: Reserva el **70% del ancho de banda** para la voz (cola de baja latencia - LLQ).
* `class class-default`: Aplica una política al resto del tráfico no clasificado.
* `fair-queue`: Asigna el ancho de banda restante de forma equitativa entre los flujos restantes.

---

### 4. Aplicar la política en la interfaz de salida

#### Escenario 1: Llamadas hacia Internet (Trunk SIP externo)
```bash
Router(config)# interface GigabitEthernet0/0/0
Router(config-if)# service-policy output QOS-VOZ
```

#### Escenario 2: Llamadas internas entre VLANs
```bash
Router(config)# interface GigabitEthernet0/0/1
Router(config-if)# service-policy output QOS-VOZ
```

#### Escenario 3: Ambos casos (Recomendado)
```bash
Router(config)# interface GigabitEthernet0/0/0
Router(config-if)# service-policy output QOS-VOZ
Router(config-if)# exit

Router(config)# interface GigabitEthernet0/0/1
Router(config-if)# service-policy output QOS-VOZ
```

#### 🔍 Explicación técnica

* `service-policy output QOS-VOZ`: Aplica la política **en la dirección de salida** de la interfaz.
* **Interfaz WAN (G0/0/0):** Prioriza el tráfico de voz hacia Internet (trunk SIP externo).
* **Interfaz LAN (G0/0/1):** Prioriza el tráfico de voz entre VLANs internas.
* **Importante:** Ajusta los nombres de las interfaces según tu modelo de router (algunos usan `G0/0` en lugar de `G0/0/0`).

---

### 5. Verificar la configuración
```bash
Router# show access-list 100
Router# show policy-map interface GigabitEthernet0/0/1
Router# show class-map
```

#### 🔍 Explicación técnica

* `show access-list 100`: Muestra los criterios de la ACL y el número de coincidencias.
* `show policy-map interface`: Muestra las estadísticas de paquetes clasificados por cada clase.
* Permite confirmar si los paquetes SIP y RTP están siendo detectados y priorizados.
* **Durante una llamada activa**, deberías ver el contador de packets aumentar en la clase VOZ.

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
Switch(config-if)# exit
```

#### 🔍 Explicación técnica

* `switchport mode access`: Configura el puerto en modo acceso (NO trunk).
* `switchport access vlan 10`: Asigna la VLAN de datos para el PC u otros dispositivos (tráfico sin etiquetar).
* `switchport voice vlan 20`: Asigna la VLAN de voz para el tráfico de telefonía IP (tráfico etiquetado 802.1Q).
* `mls qos trust cos`: Indica al switch que confíe en el **valor CoS (Class of Service)** marcado por el teléfono IP o el servidor FreePBX.
* `spanning-tree portfast`: Optimiza la convergencia del puerto, evitando retardos al iniciar el enlace (solo usar en puertos finales, nunca en trunks).
* **Nota:** El puerto permite tráfico de DOS VLANs simultáneamente: datos (untagged) y voz (tagged), sin necesidad de configurarlo como trunk.

---

### 4. Mapear valores CoS a DSCP
```bash
Switch(config)# mls qos map cos-dscp 0 8 16 24 32 46 48 56
```

#### 🔍 Explicación técnica

* Este comando relaciona los valores **CoS (Capa 2)** con **DSCP (Capa 3)**.
* **Mapeo estándar:**
  * CoS 0 → DSCP 0 (Best Effort)
  * CoS 1 → DSCP 8
  * CoS 2 → DSCP 16
  * CoS 3 → DSCP 24
  * CoS 4 → DSCP 32
  * CoS 5 → DSCP 46 **(EF - Expedited Forwarding)** ← Tráfico de voz
  * CoS 6 → DSCP 48
  * CoS 7 → DSCP 56
* El valor **46 (EF)** es el estándar RFC 3246 para tráfico de voz y garantiza prioridad absoluta en toda la red.

---

### 5. Verificación de QoS en el switch
```bash
Switch# show mls qos
Switch# show mls qos interface FastEthernet0/10
Switch# show mls qos maps cos-dscp
```

#### 🔍 Explicación técnica

* `show mls qos`: Muestra el estado global de QoS en el switch.
* `show mls qos interface`: Muestra el estado del puerto y las estadísticas de QoS.
* `show mls qos maps cos-dscp`: Verifica las tablas de mapeo entre CoS y DSCP activas.

---

## 🧪 Pruebas y Validación

### En el Router:

1. **Realiza una llamada de prueba** desde FreePBX o un teléfono IP.
2. **Verifica que los contadores aumenten:**
```bash
   Router# show policy-map interface GigabitEthernet0/0/1
```
3. **Deberías ver:**
   * Packets incrementándose en la clase VOZ (SIP/RTP)
   * 0 drops en la clase VOZ (sin pérdida de paquetes)
   * Tráfico normal en class-default

### En el Switch:

1. **Verifica las estadísticas del puerto:**
```bash
   Switch# show mls qos interface FastEthernet0/10 statistics
```
2. **Deberías ver:**
   * Tráfico clasificado con CoS 5 (voz)
   * Tráfico de la VLAN 20 (voz) separado de la VLAN 10 (datos)

---

## 🧾 Conclusión

Con esta configuración se logra lo siguiente:

* **ACLs extendidas** para clasificar tráfico SIP/RTP de forma confiable en cualquier router Cisco.
* **VLAN dedicada a voz (VLAN 20)** para aislar el tráfico VoIP.
* **QoS activo en router y switch**, garantizando prioridad a los paquetes SIP/RTP.
* **Marcado y confianza en CoS/DSCP**, manteniendo coherencia de prioridad en toda la red.
* **Compatibilidad universal** sin depender de NBAR o protocolos específicos del IOS.

El resultado es una red optimizada para **telefonía IP con calidad estable**, evitando cortes y retardos durante las llamadas VoIP.

---

## 📝 Notas Adicionales

### Ajuste de puertos RTP en FreePBX:

Si necesitas cambiar el rango de puertos RTP en FreePBX:
1. Accede a **Settings → Asterisk SIP Settings**
2. Busca **RTP Port Range**
3. Configura el rango (por defecto: 10000-20000)
4. Aplica cambios y reinicia Asterisk
5. **Actualiza la ACL 100 en el router** con el nuevo rango

### Solución de problemas:

* **Los paquetes no aumentan en la clase VOZ:**
  * Verifica que el tráfico esté pasando por la interfaz donde aplicaste el QoS
  * Revisa los puertos RTP en FreePBX y ajusta la ACL
  * Usa `show access-list 100` para ver si hay coincidencias

* **Drops en la clase VOZ:**
  * Aumenta el porcentaje de prioridad (por ejemplo, 80%)
  * Verifica el ancho de banda disponible en la interfaz

* **El switch no marca el tráfico:**
  * Verifica que `mls qos` esté activo globalmente
  * Confirma que el puerto tenga `mls qos trust cos`
  * Revisa que FreePBX o los teléfonos IP estén marcando el tráfico con CoS 5
