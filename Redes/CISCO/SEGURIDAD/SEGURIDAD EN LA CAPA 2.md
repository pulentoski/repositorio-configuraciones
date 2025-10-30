# RESUMEN TÉCNICO: SEGURIDAD EN LA CAPA 2
La Capa 2 (Enlace de Datos) es fundamental para la red. 
Si se ve comprometida, se afectan todas las capas superiores.
## A continuación se detallan los ataques más comunes y las configuraciones de mitigación.

# 1. PORT SECURITY
# Protege los puertos del switch limitando las direcciones MAC permitidas.
# Evita ataques de inundación de tabla MAC (MAC Flooding) y suplantación (Spoofing).

    Switch(config-if)# switchport mode access                        # Configura el puerto como de acceso
    Switch(config-if)# switchport port-security                      # Habilita la seguridad de puerto
    Switch(config-if)# switchport port-security maximum <1-8192>      # Limita el número de MACs por puerto
    Switch(config-if)# switchport port-security mac-address <mac>     # Asigna una MAC específica al puerto
    Switch(config-if)# switchport port-security mac-address sticky    # Aprende y guarda MACs automáticamente
    Switch(config-if)# switchport port-security violation {shutdown | restrict | protect}  # Define acción ante violación
    Switch(config-if)# shutdown
    Switch(config-if)# no shutdown                                   # Restablece puerto tras violación

# 2. SEGURIDAD DE VLANs
# Evita ataques de VLAN hopping y doble etiquetado.
# Garantiza que los puertos se mantengan en VLANs seguras y no participen en trunks no autorizados.

    Switch(config-if)# switchport mode access                        # Fija el puerto como acceso
    Switch(config-if)# switchport access vlan <vlan-id>              # Asigna VLAN al puerto
    Switch(config-if)# switchport mode trunk                         # Configura trunk manualmente
    Switch(config-if)# switchport trunk native vlan <vlan-id>        # Cambia la VLAN nativa (evita VLAN 1)
    Switch(config-if)# switchport nonegotiate                        # Desactiva DTP (negociación automática)
    Switch(config-if)# shutdown                                      # Deshabilita puertos no usados
    Switch(config-if)# switchport access vlan 1000                   # Mueve puertos inactivos a VLAN no usada
    Switch(config-if)# switchport protected                          # Aísla puertos (PVLAN Edge)

# 3. DHCP SNOOPING
# Evita ataques DHCP Starvation y servidores falsos (DHCP Spoofing).
# Permite solo respuestas de servidores DHCP legítimos.

    Switch(config)# ip dhcp snooping                                 # Habilita DHCP Snooping globalmente
    Switch(config)# ip dhcp snooping vlan <vlan-id|vlan-range>        # Activa DHCP Snooping en VLANs específicas
    Switch(config-if)# ip dhcp snooping trust                        # Marca puerto como confiable (hacia servidor)
    Switch(config-if)# ip dhcp snooping limit rate <rate>             # Limita solicitudes DHCP por segundo
    Switch(config)# ip dhcp snooping verify no-relay-address          # Verifica campos DHCP
    Switch(config)# ip dhcp snooping information option               # Controla inserción de opción 82

# 4. DYNAMIC ARP INSPECTION (DAI)
# Previene ataques de ARP Spoofing/Poisoning verificando IP-MAC en tramas ARP.
# Solo permite ARP válidos según la base de datos de DHCP Snooping.

    Switch(config)# ip arp inspection vlan <vlan-id|vlan-range>       # Activa inspección ARP en VLAN
    Switch(config-if)# ip arp inspection trust                        # Marca puerto como confiable
    Switch(config)# ip arp inspection validate {src-mac | dst-mac | ip}  # Valida campos en tramas ARP
    Switch(config-if)# ip arp inspection limit rate <pps>             # Limita tasa de tramas ARP
    Switch(config)# ip arp inspection log-buffer entries <number>     # Define buffer de logs ARP
    Switch(config)# ip arp inspection log-buffer logs <interval>      # Intervalo de registro de eventos

# 5. IP SOURCE GUARD (IPSG)
# Bloquea tráfico IP/MAC no autorizado según registros DHCP Snooping.
# Previene suplantación de IPs y MACs (Spoofing).

    Switch(config-if)# ip verify source                               # Activa validación IP de origen
    Switch(config-if)# ip verify source port-security                 # Verifica IP + MAC simultáneamente
    Switch(config)# ip dhcp snooping                                  # Requiere DHCP Snooping habilitado
    Switch(config)# ip dhcp snooping vlan <vlan-id>                   # Asocia VLAN protegidas

# 6. SEGURIDAD STP
# Protege el Spanning Tree Protocol contra ataques que manipulan roles de root bridge o generan bucles.

    Switch(config-if)# spanning-tree portfast                         # Habilita PortFast en puertos de acceso
    Switch(config)# spanning-tree portfast default                    # Aplica PortFast globalmente
    Switch(config-if)# spanning-tree bpduguard enable                 # Desactiva puertos que reciben BPDUs
    Switch(config)# spanning-tree portfast bpduguard default          # Activa BPDU Guard global
    Switch(config-if)# spanning-tree guard root                       # Evita que puertos no raíz sean root
    Switch(config-if)# spanning-tree guard loop                       # Evita bucles por pérdida de BPDUs
    Switch(config)# spanning-tree loopguard default                   # Activa Loop Guard global
    Switch(config-if)# spanning-tree bpdufilter enable                # Filtra BPDUs en puertos específicos

# 7. COMANDOS DE VERIFICACIÓN
# Verifica el estado y configuración de las funciones de seguridad en Capa 2.

    Switch# show port-security                                        # Muestra estado general de Port Security
    Switch# show port-security interface <interface>                  # Detalla estado de interfaz específica
    Switch# show port-security address                                # Muestra direcciones MAC seguras
    Switch# show ip dhcp snooping                                     # Estado de DHCP Snooping
    Switch# show ip dhcp snooping binding                             # Muestra tabla de bindings válidos
    Switch# show ip arp inspection                                    # Estado de ARP Inspection
    Switch# show ip arp inspection statistics                         # Muestra estadísticas de DAI
    Switch# show ip arp inspection interface <interface>               # Estado por interfaz
    Switch# show ip verify source                                     # Estado de IP Source Guard
    Switch# show spanning-tree summary                                # Resumen de STP y roles
    Switch# show spanning-tree interface <interface> detail            # Detalle de STP en interfaz
    Switch# show spanning-tree inconsistentports                      # Puertos bloqueados por inconsistencias STP
    Switch# show interfaces status                                    # Estado general de puertos
    Switch# show interfaces switchport                                # Detalles de modo y VLAN en cada puerto
    Switch# show vlan brief                                           # Muestra VLANs activas

# 8. CONFIGURACIÓN GLOBAL DE SEGURIDAD
# Mejora la seguridad general del switch deshabilitando servicios innecesarios y controlando acceso administrativo.

    Switch(config)# no cdp run                                        # Desactiva Cisco Discovery Protocol
    Switch(config)# no lldp run                                       # Desactiva LLDP
    Switch(config)# banner motd $Unauthorized Access Prohibited$      # Agrega mensaje legal de acceso
    Switch(config)# line console 0
    Switch(config-line)# exec-timeout 5 0                             # Cierra sesiones inactivas
    Switch(config)# logging console                                   # Habilita logging por consola
    Switch(config)# logging buffered 16384                            # Configura buffer de logs interno
    Switch(config)# access-list 10 permit 192.168.1.0 0.0.0.255       # ACL para administración
    Switch(config)# line vty 0 15
    Switch(config-line)# access-class 10 in                           # Aplica ACL a sesiones remotas
