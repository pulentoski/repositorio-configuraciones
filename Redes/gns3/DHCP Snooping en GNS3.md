# Guía de Configuración de DHCP Snooping en GNS3 (Cisco IOS)

Esta guía explica el concepto, la arquitectura y los pasos paso a paso para configurar y verificar **DHCP Snooping** en una topología de red simulada en **GNS3** utilizando Cisco IOS (vIOS-L2 / IOS 15.x).

---

## 1. Introducción

En redes de área local (LAN), la asignación dinámica de direcciones IP se basa en el protocolo **DHCP (Dynamic Host Configuration Protocol)**. Por defecto, las tramas de solicitud DHCP (*DHCP Discover*) se transmiten mediante broadcast en toda la VLAN. 

Si un usuario malintencionado o sin experiencia conecta un servidor DHCP no autorizado (como un router doméstico o una máquina virtual) en un puerto de acceso, este puede empezar a responder solicitudes DHCP más rápido que el servidor legítimo. Esto expone a la red a ataques graves de seguridad.

---

## 2. ¿Qué es DHCP Snooping?

**DHCP Snooping** es una característica de seguridad de Capa 2 (Switching) que actúa como un firewall de inspección entre las interfaces no fiables de los usuarios y el servidor DHCP.

### 2.1 Principales Amenazas que Mitiga

1. **Rogue DHCP Server (Servidor DHCP Falso):**
   Un atacante responde con su propia dirección como Puerta de Enlace Predeterminada (*Default Gateway*) o Servidor DNS, redirigiendo el tráfico de los usuarios para realizar ataques de **Man-in-the-Middle (MitM)** o suplantación de identidades.
   
2. **DHCP Starvation (Agotamiento de Direcciones IP):**
   Un atacante genera miles de peticiones DHCP con direcciones MAC falsas para agotar todo el pool de direcciones IP del servidor legítimo, provocando una Denegación de Servicio (DoS) para nuevos clientes.

### 2.2 Conceptos Clave: Puertos Trusted vs. Untrusted

DHCP Snooping clasifica los puertos del switch en dos categorías estrictas:

* **Puertos de Confianza (*Trusted*):**
  * Puertos donde residen **servidores DHCP legítimos**, routers o enlaces troncales (*trunks*) hacia otros switches.
  * Permiten el paso de **todos** los mensajes DHCP (tanto peticiones de clientes como respuestas del servidor: *OFFER*, *ACK*).

* **Puertos de No Confianza (*Untrusted*):**
  * Puertos de acceso donde se conectan los dispositivos finales (PCs, laptops, teléfonos VoIP, VPCs en GNS3).
  * **Regla de seguridad:** Solo se permiten peticiones del cliente (*DISCOVER*, *REQUEST*). Si por un puerto *untrusted* se detecta un mensaje de respuesta de servidor (*OFFER*, *ACK* o *NAK*), **el switch descarta el paquete inmediatamente** y puede deshabilitar el puerto.

### 2.3 Base de Datos de Enlace (*DHCP Snooping Binding Database*)

Cuando un cliente obtiene una IP legítimamente a través de un puerto *untrusted*, el switch inspecciona los paquetes e introduce una entrada en la **Binding Table**:
* Dirección MAC del cliente.
* Dirección IP asignada por el servidor legítimo.
* Tiempo de concesión (*Lease Time*).
* VLAN asociada.
* Puerto físico de conexión.

> **Nota:** Esta tabla es fundamental, ya que sirve como base para activar otras funciones avanzadas de seguridad L2 como **DAI (Dynamic ARP Inspection)** e **IP Source Guard**.

---

## 3. Consideraciones Especiales en GNS3 y Cisco IOS

Al trabajar con routers Cisco como servidores DHCP o dentro de entornos simulados en GNS3 (vIOS-L2, Dynamips C7200), es común encontrarse con dos comportamientos típicos:

1. **Opción 82 de DHCP (Option 82 / Information Option):**
   Por defecto, el switch adjunta la *Opción 82* a las solicitudes DHCP que pasan por puertos *untrusted*. Los routers Cisco que actúan como servidores DHCP suelen descartar estas peticiones si no están configurados para aceptar la Opción 82, lo que provoca que los clientes/VPCs no reciban IP.
   * **Solución:** Desactivar la inserción de la opción 82 con el comando `no ip dhcp snooping information option` en el switch.
2. **Diferencias de Duplex/Speed:**
   Asegurar que las interfaces entre routers y switches coincidan en velocidad y modo dúplex (`duplex full`, `speed 100`) para evitar mensajes de `%CDP-4-DUPLEX_MISMATCH`.

---

## 4. Comandos de Configuración Paso a Paso

### Topología de Referencia

* **RT-1 (Router / Servidor DHCP):** Conectado en la interfaz `GigabitEthernet0/0` del switch.
* **SW-1 (Switch L2/L3):** Switch donde se aplica DHCP Snooping en la **VLAN 10**.
* **VPC-1 (Cliente):** Conectado a la interfaz `GigabitEthernet0/1` (VLAN 10).

---

### Paso 1: Configurar DHCP Snooping en el Switch (SW-1)

```text
SW-1# configure terminal

! 1. Activar DHCP Snooping de forma global
SW-1(config)# ip dhcp snooping

! 2. Habilitar la función en las VLANs requeridas (ejemplo: VLAN 10 y 20)
SW-1(config)# ip dhcp snooping vlan 10,20

! 3. Desactivar la opción 82 para evitar incompatibilidad con routers Cisco
SW-1(config)# no ip dhcp snooping information option

! 4. Configurar el puerto hacia el Servidor DHCP como de Confianza (Trusted)
SW-1(config)# interface GigabitEthernet0/0
SW-1(config-if)# description === Enlace a Servidor DHCP / Router ===
SW-1(config-if)# ip dhcp snooping trust
SW-1(config-if)# exit

! 5. (Opcional) Limitar la tasa de paquetes DHCP en puertos untrusted para evitar inundaciones (DHCP Starvation)
SW-1(config)# interface GigabitEthernet0/1
SW-1(config-if)# ip dhcp snooping limit rate 15
SW-1(config-if)# exit
```

---

### Paso 2: Solicitud de IP en el Cliente (VPC en GNS3)

En la consola del VPC conectado al puerto `Gi0/1`:

```text
PC-1> ip dhcp
DD Requested IP: 10.10.10.2/24
```

---

## 5. Comandos de Verificación

Para confirmar que DHCP Snooping está funcionando y ver los registros de seguridad generados, utiliza los siguientes comandos en el **Switch (SW-1)**:

### 1. Verificar el Estado Global de DHCP Snooping

Muestra si la función está habilitada, en qué VLANs está activa y qué interfaces son *trusted*.

```text
SW-1# show ip dhcp snooping
```

**Ejemplo de Salida:**
```text
Switch DHCP snooping is enabled
Switch DHCP gleaning is disabled
DHCP snooping is configured on following VLANs:
10,20
DHCP snooping is operational on following VLANs:
10,20
Insertion of option 82 is disabled
DHCP snooping trust/rate is configured on the following Interfaces:

Interface                  Trusted    Allow option    Rate limit (pps)
-----------------------    -------    ------------    ----------------
GigabitEthernet0/0         yes        yes             unlimited
```

---

### 2. Verificar la Base de Datos de Enlace (Binding Table)

Verifica que el switch haya capturado y amarrado correctamente la dirección MAC del cliente con su IP asignada, la VLAN y la interfaz física.

```text
SW-1# show ip dhcp snooping binding
```

**Ejemplo de Salida:**
```text
MacAddress         IpAddress        Lease(sec)  Type           VLAN  Interface
-----------------  ---------------  ----------  -------------  ----  --------------------
00:50:79:66:68:00  10.10.10.2       86223       dhcp-snooping  10    GigabitEthernet0/1
Total number of bindings: 1
```

---

### 3. Verificar Estadísticas de Paquetes y Bloqueos

Muestra cuántos paquetes DHCP fueron procesados, cuántos fueron aceptados y si ha habido paquetes descartados por no cumplir las reglas de seguridad.

```text
SW-1# show ip dhcp snooping statistics
```

---

## 6. Resumen de Diferencia de Comandos Clave

| Equipo | Comando | Propósito |
| :--- | :--- | :--- |
| **Router (DHCP Server)** | `show ip dhcp binding` | Muestra las concesiones de direcciones IP entregadas a los clientes por el servicio DHCP del router. |
| **Switch (Seguridad L2)** | `show ip dhcp snooping binding` | Muestra la tabla de inspección L2 construida por el switch para validar paquetes legítimos y proteger la red. |

---

## 7. Conclusión

Con la implementación de **DHCP Snooping**:
1. Se bloquea cualquier servidor DHCP no autorizado conectado a puertos *untrusted*.
2. Se genera la tabla dinámica **DHCP Snooping Binding**, permitiendo implementar posteriormente soluciones de seguridad complementarias como **Dynamic ARP Inspection (DAI)** e **IP Source Guard**.
