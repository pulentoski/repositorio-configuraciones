# Configuración del Protocolo de Enrutamiento EIGRP

## Descripción General
Este documento describe la configuración del protocolo **EIGRP (Enhanced Interior Gateway Routing Protocol)** en routers Cisco.  
EIGRP es un protocolo de enrutamiento dinámico **híbrido** (posee características tanto de los protocolos de vector de distancia como de los de estado de enlace) desarrollado por Cisco.  
Permite el intercambio de información de enrutamiento de manera eficiente y rápida, utilizando una métrica compuesta basada en ancho de banda, retardo, confiabilidad, carga y MTU.

## Características Principales
- Tipo de protocolo: Híbrido (Vector de distancia avanzado)  
- Algoritmo: DUAL (Diffusing Update Algorithm)  
- Métrica compuesta: Bandwidth, Delay, Reliability, Load, MTU  
- Soporta **VLSM** y **CIDR**  
- Establece **vecindades** con routers en el mismo número de sistema autónomo (AS)  
- Permite **convergencia rápida** y utiliza actualizaciones parciales cuando cambia una ruta 
- Todos los routers utilizan el mismo número de sistema autónomo (AS).  
- Cada router anuncia las redes directamente conectadas.

## Configuración Básica de EIGRP
      router eigrp 100
      network 192.168.1.0 0.0.0.255
      network 10.0.0.0 0.0.0.255
      no auto-summary

## Explicación de Comandos

### router eigrp 100
Inicia el proceso **EIGRP** con el número de **sistema autónomo (AS)** igual a 100.  
Los routers que compartan el mismo AS podrán intercambiar información de enrutamiento.

### network 192.168.1.0 0.0.0.255
Activa EIGRP en todas las interfaces que pertenezcan a la red **192.168.1.0/24**.  
El router enviará paquetes Hello para establecer vecindades EIGRP en esa red.

### network 10.0.0.0 0.0.0.255
Incluye la red **10.0.0.0/24** dentro del proceso EIGRP.  
Permite formar vecindad con otros routers que tengan interfaces en esa red.

### no auto-summary
Desactiva la **sumarización automática** en los límites de las clases de red.  
Permite anunciar subredes específicas en lugar de redes claseful, lo cual es necesario en redes con subredes discontiguas o con VLSM.

## Configuración de un Segundo Router (Ejemplo)
    router eigrp 100
    network 10.0.0.0 0.0.0.255
    network 172.16.1.0 0.0.0.255
    no auto-summary

## Comandos de Verificación
    show ip route eigrp  
    show ip eigrp neighbors  
    show ip eigrp topology  
    show ip protocols  

## Notas Académicas
- Todos los routers que deseen formar vecindad deben tener el **mismo número de sistema autónomo (AS)**.  
- EIGRP utiliza el **algoritmo DUAL**, que garantiza rutas libres de bucles y rápida convergencia.  
- La métrica EIGRP se calcula considerando los valores de **ancho de banda (bandwidth)** y **retardo (delay)** de la ruta más lenta y más larga respectivamente.  
- **No auto-summary** debe estar habilitado en todas las configuraciones modernas para evitar problemas con subredes discontiguas.  
- Es recomendable definir manualmente el **router-id** si se utilizan múltiples procesos o redes complejas.

## Buenas Prácticas
- Verificar la formación de vecindades antes de redistribuir rutas.  
- Mantener consistencia en el número de AS en todos los routers que intercambian información.  
- Utilizar el comando **show ip eigrp topology** para revisar el estado de las rutas de respaldo (feasible successors).  
- Documentar las redes anunciadas y las interfaces participantes para evitar conflictos de configuración.
