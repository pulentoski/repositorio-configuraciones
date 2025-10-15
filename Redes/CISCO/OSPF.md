# Configuración del Protocolo de Enrutamiento OSPF

## Descripción General
Este documento describe la configuración del protocolo **OSPF (Open Shortest Path First)** en routers Cisco.  
OSPF es un protocolo de enrutamiento dinámico de tipo **link-state**, utilizado para determinar la mejor ruta hacia cada red dentro de un sistema autónomo mediante el cálculo del **costo** basado en el ancho de banda.

## Características Principales
- Tipo de protocolo: Link-State (Estado de Enlace)  
- Algoritmo: Dijkstra (SPF – Shortest Path First)  
- Métrica: Costo (basado en ancho de banda)  
- Soporta áreas jerárquicas (área 0 es el backbone)  
- Permite segmentar redes grandes en múltiples áreas para optimizar el rendimiento y reducir la carga de CPU y memoria.   

## Configuración Básica de OSPF

Habilitar OSPF en el router

    router ospf 1
    router-id 1.1.1.1
    network 10.0.0.0 0.0.0.255 area 0
    network 192.168.1.0 0.0.0.255 area 0

## Explicación de Comandos

### router ospf 1
Inicia el proceso OSPF con el número de identificación **1**.  
Cada proceso OSPF es independiente dentro del router.

### router-id 1.1.1.1
Asigna manualmente un **identificador único** al router dentro del dominio OSPF.  
Si no se configura, el router selecciona la IP más alta de sus interfaces activas.  
Este ID se utiliza para identificar el router en el proceso de formación de adyacencias y en la base de datos de estado de enlace (LSDB).

### network 10.0.0.0 0.0.0.255 area 0
Indica a OSPF que active el proceso en todas las interfaces que pertenezcan a la red **10.0.0.0/24**.  
El parámetro **area 0** especifica que dichas interfaces formarán parte del área backbone.

### network 192.168.1.0 0.0.0.255 area 0
Activa OSPF en la red **192.168.1.0/24** dentro del área 0, permitiendo la formación de vecindades OSPF con otros routers conectados a esta red.


## Configuración de un Segundo Router (Ejemplo)
    router ospf 1
    router-id 2.2.2.2
    network 192.168.1.0 0.0.0.255 area 0
    network 172.16.1.0 0.0.0.255 area 0


## Comandos de Verificación
    show ip route ospf  
    show ip ospf neighbor  
    show ip ospf database  
    show ip protocols  

## Notas 
- El **router-id** es esencial para la identificación en la base de datos OSPF.  
- Todas las interfaces que participan en OSPF deben pertenecer a un área.  
- El **área 0** debe existir en toda topología OSPF jerárquica, ya que actúa como columna vertebral de comunicación.  
- Si hay más de un área, debe existir **conectividad directa o virtual link** hacia el área 0.  

## Buenas Prácticas
- Utilizar **router-id fijos y únicos** para facilitar el diagnóstico.  
- Mantener consistencia en la asignación de áreas.  
- Evitar sobrecargar el área 0 con demasiadas redes; usar áreas adicionales cuando sea necesario.  
- Verificar siempre la **formación de vecindades** y la **propagación de rutas** antes de habilitar redistribución o sumarización.

