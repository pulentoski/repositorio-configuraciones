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
- Permite **autenticación** entre vecinos para garantizar el intercambio seguro de tablas de enrutamiento.

## Configuración Básica de OSPF

Habilitar OSPF en el router:

    router ospf 1
    router-id 1.1.1.1
    network 10.0.0.0 0.0.0.255 area 0
    network 192.168.1.0 0.0.0.255 area 0

## Configuración de Autenticación OSPF

La autenticación en OSPF valida la identidad de los vecinos antes de establecer una adyacencia. Se puede configurar de dos formas principales (Texto Plano o MD5) y aplicarse a nivel de **interfaz** o a nivel de **área**.

### 1. Autenticación MD5 a nivel de Interfaz (Recomendado)
Aplica la configuración directamente sobre la interfaz participante:

    interface GigabitEthernet0/0
     ip ospf authentication message-digest
     ip ospf message-digest-key 1 md5 ClaveSegura123

### 2. Autenticación MD5 a nivel de Área
Habilita el requerimiento de autenticación para todas las interfaces pertenecientes a esa área (sigue requiriendo definir la clave en la interfaz):

    router ospf 1
     area 0 authentication message-digest

    interface GigabitEthernet0/0
     ip ospf message-digest-key 1 md5 ClaveSegura123

### 3. Autenticación por Texto Plano (No recomendada en producción)
Envía la contraseña sin cifrar a través de la red:

    interface GigabitEthernet0/0
     ip ospf authentication
     ip ospf authentication-key MiClavePlana

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

### ip ospf authentication message-digest
Habilita el método de autenticación cifrada (MD5) en la interfaz seleccionada.

### ip ospf message-digest-key 1 md5 [contraseña]
Define el ID de la clave (`1`) y la contraseña cifrada mediante el algoritmo MD5 para la interfaz.

## Configuración de un Segundo Router (Ejemplo con Autenticación)

    router ospf 1
    router-id 2.2.2.2
    network 192.168.1.0 0.0.0.255 area 0
    network 172.16.1.0 0.0.0.255 area 0

    interface GigabitEthernet0/0
     ip ospf authentication message-digest
     ip ospf message-digest-key 1 md5 ClaveSegura123

## Comandos de Verificación
    show ip route ospf  
    show ip ospf neighbor  
    show ip ospf database  
    show ip protocols  
    show ip ospf interface GigabitEthernet0/0  (Muestra detalles de autenticación de la interfaz)

## Notas 
- El **router-id** es esencial para la identificación en la base de datos OSPF.  
- Todas las interfaces que participan en OSPF deben pertenecer a un área.  
- El **área 0** debe existir en toda topología OSPF jerárquica, ya que actúa como columna vertebral de comunicación.  
- Si hay más de un área, debe existir **conectividad directa o virtual link** hacia el área 0.  
- **Importante sobre autenticación:** Para que se forme la adyacencia entre dos routers vecinos, el tipo de autenticación, el Key ID y la contraseña deben coincidir exactamente en ambos extremos.

## Buenas Prácticas
- Utilizar **router-id fijos y únicos** para facilitar el diagnóstico.  
- Mantener consistencia en la asignación de áreas.  
- Usar siempre **autenticación cifrada (MD5)** en entornos de producción para prevenir inyección de rutas no autorizadas.  
- Evitar sobrecargar el área 0 con demasiadas redes; usar áreas adicionales cuando sea necesario.  
- Verificar siempre la **formación de vecindades** y la **propagación de rutas** antes de habilitar redistribución o sumarización.
