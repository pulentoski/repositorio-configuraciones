
Conversación con Gemini
mira: show ru

*Aug 17 01:28:52.881: %SYS-5-CONFIG_I: Configured from console by console

*Aug 17 01:28:53.914: %PLATFORM-5-SIGNATURE_VERIFIED: Image 'flash0:/vios_l2-adventerprisek9-m' passed code signing verificationn

Switch#show running-config 

Building configuration...



Current configuration : 2980 bytes

!

! Last configuration change at 01:28:52 UTC Mon Aug 17 2026

!

version 15.2

service timestamps debug datetime msec

service timestamps log datetime msec

no service password-encryption

service compress-config

!

hostname Switch

!

boot-start-marker

boot-end-marker

!

!

!

no aaa new-model

!

!

!

!

!         

!         

!         

!         

ip cef    

no ipv6 cef

!         

!         

!         

spanning-tree mode rapid-pvst

spanning-tree extend system-id

!         

vlan internal allocation policy ascending

!         

!         

!         

!         

!         

!         

!         

!         

!         

!         

!         

!         

!         

!         

interface GigabitEthernet0/0

 media-type rj45

 negotiation auto

!         

interface GigabitEthernet0/1

 media-type rj45

 negotiation auto

!         

interface GigabitEthernet0/2

 media-type rj45

 negotiation auto

!         

interface GigabitEthernet0/3

 media-type rj45

 negotiation auto

!         

interface GigabitEthernet1/0

 media-type rj45

 negotiation auto

!         

interface GigabitEthernet1/1

 media-type rj45

 negotiation auto

!         

interface GigabitEthernet1/2

 media-type rj45

 negotiation auto

!         

interface GigabitEthernet1/3

 media-type rj45

 negotiation auto

!         

ip forward-protocol nd

!         

no ip http server

no ip http secure-server

!         

!         

!         

!         

!         

!         

control-plane

!         

banner exec ^C

**************************************************************************

* IOSv is strictly limited to use for evaluation, demonstration and IOS  *

* education. IOSv is provided as-is and is not supported by Cisco's      *

* Technical Advisory Center. Any use or disclosure, in whole or in part, *

* of the IOSv Software or Documentation to any third party for any       *

* purposes is expressly prohibited except as otherwise authorized by     *

* Cisco in writing.                                                      *

**************************************************************************^C

banner incoming ^C

**************************************************************************

* IOSv is strictly limited to use for evaluation, demonstration and IOS  *

* education. IOSv is provided as-is and is not supported by Cisco's      *

* Technical Advisory Center. Any use or disclosure, in whole or in part, *

* of the IOSv Software or Documentation to any third party for any       *

* purposes is expressly prohibited except as otherwise authorized by     *

* Cisco in writing.                                                      *

**************************************************************************^C

banner login ^C

**************************************************************************

* IOSv is strictly limited to use for evaluation, demonstration and IOS  *

* education. IOSv is provided as-is and is not supported by Cisco's      *

* Technical Advisory Center. Any use or disclosure, in whole or in part, *

* of the IOSv Software or Documentation to any third party for any       *

* purposes is expressly prohibited except as otherwise authorized by     *

* Cisco in writing.                                                      *

**************************************************************************^C

!         

line con 0

line aux 0

line vty 0 4

!         

!         

end       

          

Switch#

Switch#

Switch#

Switch#

Switch#

Switch#

Switch#

Switch#

¡Excelente! Tu switch vIOS-L2 con IOS 15.2 está iniciado y listo.

Para confirmar que esta imagen resuelve tus requerimientos de Seguridad L2 que no podías hacer en los routers anteriores, aquí tienes los comandos exactos para probarla en tu topología:

1. Configuración de Port Security y Voice VLAN

Plaintext
configure terminal
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown
 switchport port-security aging time 2
exit
2. Configuración de DHCP Snooping y Trunk Security

Plaintext
ip dhcp snooping
ip dhcp snooping vlan 10,20
no ip dhcp snooping information option

interface GigabitEthernet0/0
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,999
 ip dhcp snooping trust
exit
3. Configuración de VACL (VLAN Access List)

Plaintext
ip access-list extended BLOQUEO_IP
 permit ip host 192.168.10.50 any

vlan access-map FILTRO_VLAN 10
 match ip address BLOQUEO_IP
 action drop
vlan access-map FILTRO_VLAN 20
 action forward
exit

vlan filter FILTRO_VLAN vlan-list 10
4. Activar Routing Inter-VLAN (Switch Multicapa)

Plaintext
ip routing
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
Todos estos comandos son 100% nativos y funcionales en tu nuevo nodo vIOS-L2.

despues vamos por loscomandos, ahora dime con un 7200 y la iso de sw capa 3 estoy listo para configurar ?

Sí, estás 100% listo.

Con esa combinación tienes cubierto todo tu temario sin limitaciones:

Switch vIOS-L2: Te da el 100% de la Seguridad L2 (Port Security, DHCP Snooping, VACLs, Voice VLAN) y funcionalidad de Switch Multicapa.

Router C7200 (IOS 15.2): Te da todo el Routing Avanzado (OSPFv2/v3, BGP, Redistribución de rutas y Router-on-a-Stick).

Lo único que no corre dentro de IOS Cisco son los servidores finales de aplicación (Web HTTPS real, Email SMTP/POP/IMAP, DNS completo). Para probar esos Servicios L7, solo agregas dentro del lienzo de GNS3 nodos de tipo VPCS, Docker o VMs ligeras (Ubuntu/Alpine) conectadas a los switches.

se simple, se me olvido configurar la troncal: #switchport mo

Switch(config-if)#switchport mode tr

Switch(config-if)#switchport mode trunk 

Command rejected: An interface whose trunk encapsulation is "Auto" can not be configured to "trunk" mode.

Switch(config-if)#

Switch(config-if)#enc

Switch(config-if)#enca

Switch(config-if)#sw  

Switch(config-if)#switchport en

Switch(config-if)#             

Ejecuta la encapsulación primero y luego el modo troncal:

Plaintext
Switch(config-if)# switchport trunk encapsulation dot1q
Switch(config-if)# switchport mode trunk
Por qué pasa: Como la interfaz admite tanto ISL como 802.1Q, el switch exige definir cuál usar (dot1q) antes de forzar el puerto a modo trunk.

con que comando obtengo ip en el vpc

Para solicitar una IP por DHCP:

Plaintext
ip dhcp
Para verificar la IP obtenida:

Plaintext
show ip
(Si necesitas asignarla de forma estática: ip <direccion_ip> <mascara> <gateway>, por ejemplo: ip 192.168.10.10 255.255.255.0 192.168.10.1)

por que me sale este mensaje? es por que tengo una giga un fast? *Aug 17 01:34:39.899: %SYS-5-CONFIG_I: Configured from console by console

RT-1#

*Aug 17 01:34:42.887: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:35:13.951: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/0, changed state to down

RT-1#

*Aug 17 01:35:21.955: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/0, changed state to up

RT-1#

*Aug 17 01:35:22.815: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

*Aug 17 01:35:23.811: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:35:24.811: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:35:25.811: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

*Aug 17 01:35:26.811: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:35:27.811: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

*Aug 17 01:35:28.807: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:35:29.807: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:35:30.843: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:36:25.723: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:37:16.923: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:38:08.599: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

*Aug 17 01:39:04.167: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/0 (not half duplex), with Switch GigabitEthernet0/0 (half duplex).

RT-1#

No, no es por conectar Gigabit con FastEthernet. La velocidad se ajusta automáticamente al extremo más lento (100 Mbps).

El error es por una diferencia en el modo de transmisión: tu router está operando en Full Duplex y el switch en Half Duplex.

Solución
Para corregirlo, fuerza el modo Full Duplex en ambos extremos:

En el Router (RT-1):

Plaintext
configure terminal
interface FastEthernet0/0
 duplex full
En el Switch:

Plaintext
configure terminal
interface GigabitEthernet0/0
 duplex full
(Si ambos equipos soportan auto-negociación, también puedes aplicar duplex auto en ambas interfaces).

que es hal y full duplex

Duplex define la capacidad y dirección en la que dos dispositivos se envían datos a través de un canal de red.

Característica	Half Duplex	Full Duplex
Flujo de datos	Bidireccional, pero uno a la vez	Bidireccional simultáneo (envía y recibe al mismo tiempo)
Analogía	Walkie-talkie: Si hablas no escuchas; debes esperar a que la otra persona termine.	Llamada telefónica: Ambos pueden hablar y escuchar simultáneamente.
Carretera	Puente de un solo carril con semáforo (pasan en una dirección u otra).	Autopista de dos carriles independientes (cada uno va en su sentido).
Colisiones	Posibles. Si ambos transmiten a la vez, se pierde el paquete.	Imposibles. Utiliza rutas o hilos de cable independientes para Tx (transmitir) y Rx (recibir).
Rendimiento	Utiliza la mitad del ancho de banda teórico.	Duplica la capacidad de la red (ej. 100 Mbps de subida + 100 Mbps de bajada).
Uso actual	Hubs antiguos, redes Wi-Fi (a nivel de medio aéreo).	Switches Ethernet modernos, enlaces de fibra y conexiones cableadas actuales.
mira: Switch(config-if)#dupl

Switch(config-if)#duplex fu

Switch(config-if)#duplex full 

Autoneg enabled. Duplex cannot be set



Switch(config-if)#

Switch(config-if)#

Switch(config-if)#

*Aug 17 01:49:34.953: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on GigabitEthernet0/0 (not full duplex), with RT-2 FastEthernet1/0 (full duplex).

Switch(config-if)#

Switch(config-if)#

Switch(config-if)#

Switch(config-if)#

Switch(config-if)#dupl

Switch(config-if)#duplex fu

Switch(config-if)#duplex full 

Autoneg enabled. Duplex cannot be set



Switch(config-if)#

Switch(config-if)#

Switch(config-if)#exit

Switch(config)#

Switch(config)#

El switch no te deja cambiar el duplex porque la auto-negociación está activada por defecto en la interfaz Gigabit.

Desactívala primero y luego asigna el duplex:

Plaintext
configure terminal
interface GigabitEthernet0/0
 no negotiation auto
 duplex full
(Si el comando no negotiation auto no funciona en esa versión, asigna la velocidad manualmente con speed 100 antes de ejecutar duplex full).

Switch(config-if)#

Switch(config-if)#exit

Switch(config)#

Switch(config)#interface g0/0                       

Switch(config-if)#no neg

Switch(config-if)#no negotiation au

Switch(config-if)#no negotiation auto 

Switch(config-if)#

Switch(config-if)#du

Switch(config-if)#duplex fu

Switch(config-if)#duplex full 

Switch(config-if)#

Switch(config-if)#

Switch(config-if)#

*Aug 17 01:50:24.364: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on GigabitEthernet0/0 (not full duplex), with RT-2 FastEthernet1/0 (full duplex).

Switch(config-if)#exit

Switch(config)#

Switch(config)#

Switch(config)#

Switch(config)#

El mensaje volvió a salir porque la interfaz GigabitEthernet del switch sigue intentando operar a 1000 Mbps, mientras que la del router es FastEthernet (100 Mbps).

Para solucionarlo, debes fijar la velocidad a 100 Mbps en el switch para que coincida con el router:

En el Switch:

Plaintext
configure terminal
interface GigabitEthernet0/0
 speed 100
 duplex full
En el Router (RT-2):

Plaintext
configure terminal
interface FastEthernet1/0
 speed 100
 duplex full
(Nota: CDP envía alertas cada 60 segundos. Si ejecutas shutdown y luego no shutdown en las interfaces, el mensaje desaparecerá de inmediato).

como veo la ip asignada en la vpc

Ejecuta el comando:

Plaintext
show ip
(También funciona simplemente escribiendo show).

Verás un resumen como este con tu dirección, máscara, gateway y servidor DHCP:

Plaintext
NAME        : PC1[1]
IP/MASK     : 192.168.10.10/24
GATEWAY     : 192.168.10.1
DNS         : 
MAC         : 00:50:79:66:68:00
DHCP Server : 192.168.10.1
explicame que es DHCP Snooping

DHCP Snooping es una función de seguridad de Capa 2 que actúa como un "firewall" dentro del switch para filtrar el tráfico DHCP y evitar ataques en la red local.

1. El problema que resuelve

Servidores DHCP Falsos (Rogue DHCP): Evita que un usuario o atacante conecte un router/servidor DHCP no autorizado para repartir IPs falsas, puertas de enlace incorrectas o robar tráfico mediante un ataque de tipo Man-in-the-Middle.

Agotamiento de IPs (DHCP Starvation): Ayuda a mitigar ataques donde un usuario solicita miles de direcciones IP con MACs falsas para agotar el pool del servidor.

2. Cómo funciona

El switch clasifica sus puertos en dos tipos:

Puertos de Confianza (Trusted):

Se asignan únicamente a los puertos conectados a servidores DHCP legítimos, routers o enlaces troncales.

Permiten el paso de cualquier tráfico DHCP (tanto peticiones de clientes como respuestas del servidor: OFFER, ACK).

Puertos de No Confianza (Untrusted):

Son los puertos donde se conectan los usuarios finales (PCs, teléfonos, laptops).

Regla estricta: Solo se permiten peticiones de clientes (DISCOVER, REQUEST). Si el switch detecta que por un puerto untrusted ingresa una respuesta de servidor (OFFER o ACK), descarta el paquete de inmediato y puede desactivar el puerto.

3. Base de Datos de Enlace (DHCP Snooping Binding Table)

Al estar activo, el switch inspecciona los paquetes legítimos y crea automáticamente una tabla en memoria con la siguiente información:

Dirección MAC del cliente.

Dirección IP asignada por el servidor legítimo.

Puerto físico donde está conectado.

VLAN y tiempo de concesión (lease time).

(Esta tabla es indispensable porque la utilizan más adelante otras funciones de seguridad como DAI - Dynamic ARP Inspection e IP Source Guard).

4. Comandos básicos en Cisco IOS:

Plaintext
! 1. Activar DHCP Snooping globalmente
ip dhcp snooping

! 2. Indicar en qué VLANs se aplicará
ip dhcp snooping vlan 10,20

! 3. Configurar el puerto que va hacia el Servidor DHCP como Trusted
interface GigabitEthernet0/0
 ip dhcp snooping trust
eso son los comandos ? como verifico qeue sta bien ?

Sí, esos son los comandos principales. Agrega siempre el comando no ip dhcp snooping information option para evitar que el switch bloquee las peticiones en laboratorios.

Configuración completa:

Plaintext
configure terminal
ip dhcp snooping
ip dhcp snooping vlan 10,20
no ip dhcp snooping information option

interface GigabitEthernet0/0
 ip dhcp snooping trust
exit
Comandos de verificación:

show ip dhcp snooping
Verifica si la función está habilitada globalmente, en qué VLANs está activa y qué interfaces están configuradas como de confianza (trusted).

show ip dhcp snooping binding
Muestra la tabla dinámica de clientes que han obtenido IP por DHCP (muestra la dirección IP, MAC, VLAN, puerto y tiempo de concesión).

show ip dhcp snooping statistics
Muestra el contador de paquetes DHCP procesados, aceptados o descartados (útil si alguna PC no está recibiendo IP).

Prueba práctica en tu laboratorio:

Ejecuta ip dhcp en la VPC (conectada a un puerto untrusted).

Si obtiene IP correctamente, ejecuta en el switch:

Plaintext
Switch# show ip dhcp snooping binding
Debes ver una entrada con la dirección MAC y la IP asignada a la VPC.

SW-1#show ip dhcp snooping 

Switch DHCP snooping is enabled

Switch DHCP gleaning is disabled

DHCP snooping is configured on following VLANs:

10,20

DHCP snooping is operational on following VLANs:

10,20

DHCP snooping is configured on the following L3 Interfaces:



Insertion of option 82 is enabled

   circuit-id default format: vlan-mod-port

   remote-id: 0c19.3819.0000 (MAC)

Option 82 on untrusted port is not allowed

Verification of hwaddr field is enabled

Verification of giaddr field is enabled

DHCP snooping trust/rate is configured on the following Interfaces:



Interface                  Trusted    Allow option    Rate limit (pps)

-----------------------    -------    ------------    ----------------   

GigabitEthernet0/0         yes        yes             unlimited

  Custom circuit-ids:

SW-1#

La configuración básica está bien aplicada, pero tienes habilitada la Opción 82 (Insertion of option 82 is enabled), lo cual provocará que las VPCs no reciban IP si tu servidor DHCP es un router Cisco.

Análisis de tu resultado:

VLANs 10 y 20: Funcionando correctamente con DHCP Snooping.

GigabitEthernet0/0: Configurado correctamente como puerto de confianza (Trusted: yes).

Problema con Opción 82: Por defecto, el switch le añade etiquetas adicionales a los paquetes DHCP. Si el servidor DHCP es un router, este las rechazará y la VPC se quedará sin IP.

Solución rápida:

Desactiva la inserción de la Opción 82 en el switch ejecutando:

Plaintext
configure terminal
no ip dhcp snooping information option
Prueba final:

Ve a tu VPC y solicita dirección IP:

Plaintext
ip dhcp
Si la VPC obtiene IP, verifica la tabla de registros en el switch:

Plaintext
SW-1# show ip dhcp snooping binding
Si todo está en orden, ahí verás la dirección MAC, IP y VLAN asociadas a tu VPC.

me dio ip: SW-1#show ip dhcp snooping 

Switch DHCP snooping is enabled

Switch DHCP gleaning is disabled

DHCP snooping is configured on following VLANs:

10,20

DHCP snooping is operational on following VLANs:

10,20

DHCP snooping is configured on the following L3 Interfaces:



Insertion of option 82 is disabled

   circuit-id default format: vlan-mod-port

   remote-id: 0c19.3819.0000 (MAC)

Option 82 on untrusted port is not allowed

Verification of hwaddr field is enabled

Verification of giaddr field is enabled

DHCP snooping trust/rate is configured on the following Interfaces:



Interface                  Trusted    Allow option    Rate limit (pps)

-----------------------    -------    ------------    ----------------   

GigabitEthernet0/0         yes        yes             unlimited

  Custom circuit-ids:

SW-1#

¡Excelente! Al desactivar la Opción 82 el flujo de DHCP funcionó a la perfección.

Para ver la base de datos dinámica que el switch acaba de construir con la IP asignada a tu VPC, ejecuta este comando:

Plaintext
SW-1# show ip dhcp snooping binding
Deberías ver una salida similar a esta:

Plaintext
MacAddress         IpAddress        Lease(sec)  Type           VLAN  Interface
-----------------  ---------------  ----------  -------------  ----  --------------------
00:50:79:66:68:00  192.168.10.10    86400       dhcp-snooping  10    GigabitEthernet0/1
Esta tabla es la prueba definitiva de que DHCP Snooping está operando al 100% y servirá de protección para la red.

¿Cuál es la siguiente característica de seguridad L2 que quieres configurar (Port Security o VACLs)?

por q en sw si el dhp esta en el rt

Porque el router distribuye las direcciones IP, pero el switch controla los puertos físicos (Capa 2) por donde viaja ese tráfico.

Un router no puede protegerte de un ataque DHCP dentro de la red local por las siguientes razones:

El router no ve el tráfico interno del switch: Si un usuario conecta un router casero (DHCP falso) a un puerto del switch, el tráfico de broadcast (DHCP Discover) se queda dentro de la VLAN. El switch respondería a las PCs con la IP falsa antes de que la petición siquiera llegue al router legítimo.

Inspección en el punto de acceso: El switch es el único equipo capaz de analizar paquete por paquete en cada puerto físico. Al activar DHCP Snooping en el switch, este bloquea de inmediato cualquier respuesta DHCP (DHCP Offer/ACK) que venga de un puerto de usuario (untrusted), sin importar si el servidor legítimo está en un router o en un servidor dedicado.

Control de acceso: El router solo ve direcciones IP/MAC cuando los paquetes intentan salir de la subred; el switch las ve en el instante en que el cable se conecta a la pared.

SW-1#

SW-1#show ip dhcp binding 

Bindings from all pools not associated with VRF:

IP address      Client-ID/ Lease expiration Type       State      Interface

Hardware address/

User name

SW-1#

show ip dhcp binding 

Bindings from all pools not associated with VRF:

IP address      Client-ID/ Lease expiration Type       State      Interface

Hardware address/

User name

10.10.10.2      0100.5079.6668.00       Aug 18 2026 02:06 AM    Automatic  Active     FastEthernet0/0.10

RT-1#

Estás ejecutando comandos distintos para funciones distintas en cada equipo:

En el Router (RT-1): show ip dhcp binding muestra las IPs asignadas por su Servidor DHCP interno (por eso ahí sí aparece 10.10.10.2).

En el Switch (SW-1): El comando show ip dhcp binding busca un servidor DHCP configurado dentro del switch (que no existe). Para consultar la tabla de seguridad generada por el filtro L2, debes agregar la palabra snooping:

Plaintext
SW-1# show ip dhcp snooping binding
Diferencia clave:

Router: show ip dhcp binding → "¿A quién le entregué una IP como servidor?"

Switch: show ip dhcp snooping binding → "¿Qué relación MAC/IP/Puerto registré para proteger la red?"

Connected to localhost.

Escape character is '^]'.



SW-1#

SW-1#

SW-1#SW-1# show ip dhcp snooping binding

      ^

% Invalid input detected at '^' marker.



SW-1#show ip dhcp snooping binding      

MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface

------------------  ---------------  ----------  -------------  ----  --------------------

00:50:79:66:68:00   10.10.10.2       86223       dhcp-snooping   10    GigabitEthernet0/1

Total number of bindings: 1



SW-1#

¡Perfecto! Ahí tienes la confirmación total.

La tabla de DHCP Snooping registró exitosamente el tráfico:

MAC 00:50:79:66:68:00 obtuvo la IP 10.10.10.2 en la VLAN 10 a través del puerto GigabitEthernet0/1.

Ahora el switch tiene esa relación amarrada en memoria. Si alguien intentara cambiar manualmente su IP a otra o usar esa MAC en otro puerto, la red lo bloquearía.

¿Pasamos a Port Security o quieres probar Dynamic ARP Inspection (DAI) usando esta misma tabla?

quiero un readme.md en formato markdown sobre como configurar dhcp snopping en gns3. debe tener una intro, explciar que es, los comandos de configuracion y de verificacion.

Paso 2: Solicitud de IP en el Cliente (VPC en GNS3)
En la consola del VPC conectado al puerto Gi0/1:

Plaintext
PC-1> ip dhcp
DD Requested IP: 10.10.10.2/24
5. Comandos de Verificación
Para confirmar que DHCP Snooping está funcionando y ver los registros de seguridad generados, utiliza los siguientes comandos en el Switch (SW-1):

1. Verificar el Estado Global de DHCP Snooping
Muestra si la función está habilitada, en qué VLANs está activa y qué interfaces son trusted.

Plaintext
SW-1# show ip dhcp snooping
Ejemplo de Salida:

Plaintext
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
2. Verificar la Base de Datos de Enlace (Binding Table)
Verifica que el switch haya capturado y amarrado correctamente la dirección MAC del cliente con su IP asignada, la VLAN y la interfaz física.

Plaintext
SW-1# show ip dhcp snooping binding
Ejemplo de Salida:

Plaintext
MacAddress         IpAddress        Lease(sec)  Type           VLAN  Interface
-----------------  ---------------  ----------  -------------  ----  --------------------
00:50:79:66:68:00  10.10.10.2       86223       dhcp-snooping  10    GigabitEthernet0/1
Total number of bindings: 1
3. Verificar Estadísticas de Paquetes y Bloqueos
Muestra cuántos paquetes DHCP fueron procesados, cuántos fueron aceptados y si ha habido paquetes descartados por no cumplir las reglas de seguridad.

Plaintext
SW-1# show ip dhcp snooping statistics
6. Resumen de Diferencia de Comandos Clave
Equipo	Comando	Propósito
Router (DHCP Server)	show ip dhcp binding	Muestra las concesiones de direcciones IP entregadas a los clientes por el servicio DHCP del router.
Switch (Seguridad L2)	show ip dhcp snooping binding	Muestra la tabla de inspección L2 construida por el switch para validar paquetes legítimos y proteger la red.
7. Conclusión
Con la implementación de DHCP Snooping:

Se bloquea cualquier servidor DHCP no autorizado conectado a puertos untrusted.

Se genera la tabla dinámica DHCP Snooping Binding, permitiendo implementar posteriormente soluciones de seguridad complementarias como Dynamic ARP Inspection (DAI) e IP Source Guard.
"""

file_path = "README.md"
with open(file_path, "w", encoding="utf-8") as f:
f.write(readme_content)

print(f"File saved successfully as {file_path}")


```text?code_stdout&code_event_index=1
File saved successfully as README.md

Your Markdown file is ready

Icono de MD
README
 MD 
Abierto
He generado el archivo README.md con la estructura completa en formato Markdown sobre cómo configurar DHCP Snooping en GNS3.

Contenido resumido del documento:
Introducción: Explicación del flujo DHCP y los riesgos en capa 2.

¿Qué es DHCP Snooping?: Amenazas que mitiga (Rogue DHCP, DHCP Starvation), concepto de puertos Trusted vs. Untrusted y la Binding Table.

Consideraciones para GNS3 / Cisco IOS: Explicación detallada del porqué se debe desactivar la Opción 82 (no ip dhcp snooping information option).

Comandos de Configuración: Paso a paso para el Switch y solicitudes en VPC.

Comandos de Verificación: show ip dhcp snooping, show ip dhcp snooping binding y estadísticas.

Tabla Comparativa: Diferencia entre show ip dhcp binding (Router) vs. show ip dhcp snooping binding (Switch).

ahora quiero u readme pero de como instalar un sw capa 3 en gns: este link use para descragar la iso https://upw.io/75g/vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E

Debes verificar que muestre la versión 15.2 y la plataforma vIOS-L2.

2. Verificar Interfaces Disponibles
Plaintext
Switch# show ip interface brief
Confirmará las interfaces GigabitEthernet activas (Gi0/0, Gi0/1, etc.).

3. Verificar Capacidad Multicapa (Habilitar Enrutamiento IP)
Por defecto, el switch actúa en modo Capa 2 pura. Para habilitar las capacidades de Switch Capa 3 (Routing Inter-VLAN / SVIs):

Plaintext
Switch# configure terminal
Switch(config)# ip routing
4. Probar Creación de VLANs e Interfaz SVI
Plaintext
Switch(config)# vlan 10
Switch(config-vlan)# name VENTAS
Switch(config-vlan)# exit

Switch(config)# interface vlan 10
Switch(config-if)# ip address 192.168.10.1 255.255.255.0
Switch(config-if)# no shutdown
5. Verificar la Tabla de Enrutamiento
Plaintext
Switch# show ip route
Confirmará que el switch está operando como dispositivo Capa 3 al mostrar las redes directamente conectadas.

4. Solución de Problemas Comunes
Problema	Causa Probable	Solución
El switch no arranca o entra en bucle de reinicio	RAM insuficiente asignada al nodo QEMU.	Aumentar la memoria RAM a 1024 MB en las propiedades de la VM QEMU en GNS3.
No reconoce el comando ip routing	La imagen cargada no es un vIOS-L2 o se está usando un modelo L2 básico.	Confirmar mediante show version que la imagen corresponda al archivo vios_l2-adventerprisek9-m.vmdk....
Nombres de interfaz extraños (e0/0 en lugar de Gi0/0)	Formato de adaptador no configurado en la plantilla.	En Preferencias de GNS3 → QEMU VMs → Edit → Network, configurar Custom adapter name format a Gi0/{port}.
"""		
file_path = "README_INSTALL_SW_L3.md"
with open(file_path, "w", encoding="utf-8") as f:
f.write(readme_content)

print(f"File saved successfully as {file_path}")


```text?code_stdout&code_event_index=1
File saved successfully as README_INSTALL_SW_L3.md

Your Markdown file is ready

Icono de MD
README_INSTALL_SW_L3
 MD 
Abierto
He generado el archivo README_INSTALL_SW_L3.md estructurado en formato Markdown que detalla el procedimiento de instalación y verificación de la imagen de Switch Capa 3 (vIOS-L2) en GNS3.

Contenido del documento:
Introducción y Requisitos: Datos del archivo descargado (vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E), versión de IOS y enlace de referencia.

Métodos de Instalación:

Método A (Automático): Uso del archivo de plantilla .gns3a en la GNS3 VM.

Método B (Manual): Paso a paso para agregar la VM QEMU (RAM recomendada, asignación de 8-16 interfaces, nombre de adaptadores Gi0/{port} e icono de Switch Multicapa).

Primer Inicio y Verificación:

Comandos de consola IOS (show version, show ip interface brief).

Activación del enrutamiento IP (ip routing).

Pruebas de interfaces SVI y consulta de la tabla de rutas (show ip route).

Solución de Problemas Comunes: Tabla con fallas típicas (bucle de reinicio por RAM, problemas de sintaxis o nombres de puerto) y sus respectivas soluciones.




Gemini es una IA y puede cometer errores.

Analizando
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
README.md
Mostrando README.md.
