# DHCP Snooping: Configuración y Comandos

**¿Qué es DHCP Snooping?**  
DHCP Snooping es una función de seguridad en switches que protege la red contra ataques de DHCP spoofing. Bloquea servidores DHCP no autorizados y asegura que los clientes obtengan IPs solo de servidores legítimos. Mantiene una tabla confiable de asignaciones IP-MAC-Puerto (bindings).

**Objetivos:**  
- Bloquear servidores DHCP no autorizados (rogue DHCP servers)  
- Prevenir ataques de envenenamiento DHCP  
- Generar tabla confiable de bindings IP-MAC-Puerto  
- Limitar solicitudes DHCP excesivas  

**Comandos de Configuración y Ejemplo Completo:**

! 1. Habilitar globalmente DHCP Snooping
configure terminal

    ip dhcp snooping

! 2. Proteger VLANs

    ip dhcp snooping vlan [num]        ! Ejemplo: ip dhcp snooping vlan 10,20-30
    
Se desactiva para todo el switch, porque afecta cómo el switch inserta la Opción 82 en los paquetes DHCP.

    Switch(config)# no ip dhcp snooping information option

! 3. Configurar puertos de confianza (trusted)

    interface [interfaz]      ! Ejemplo: interface GigabitEthernet0/1
    ip dhcp snooping trust
    exit

! 4. Limitar tasa de mensajes DHCP (opcional)

    interface [interfaz]                ! Ejemplo: interface range FastEthernet0/2-24
    ip dhcp snooping limit rate [num]
    exit

! 5. Verificación

    show ip dhcp snooping
    show ip dhcp snooping binding
    show ip dhcp snooping statistics



**Notas Importantes:**  
- Todos los puertos son UNTRUSTED por defecto.  
- Solo los puertos hacia servidores DHCP legítimos deben ser trusted.  
- Funciona en switches de capa 2, no en routers.  
- Requiere que los clientes obtengan IPs mediante DHCP.  
- Puertos no confiables bloquearán automáticamente respuestas DHCP maliciosas.
