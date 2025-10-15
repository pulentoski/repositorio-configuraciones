# Configuración de Redistribución entre EIGRP y OSPF

Este documento explica cómo configurar la redistribución entre los protocolos de enrutamiento dinámico EIGRP y OSPF para lograr convergencia entre ambos.  
El escenario considera tres routers donde el router central actúa como punto de redistribución entre ambos protocolos.

## Topología de Referencia
[ R1 - EIGRP ] —— [ R2 - EIGRP + OSPF ] —— [ R3 - OSPF ]

- R1 utiliza EIGRP.  
- R2 utiliza EIGRP y OSPF (redistribuye rutas).  
- R3 utiliza OSPF.

## Configuración del Router Intermedio (R2)
Configuración EIGRP
  
    router eigrp 100
    network 192.168.1.0 0.0.0.255
    network 172.16.1.0 0.0.0.255
    no auto-summary

Configuración OSPF

    router ospf 1
    network 172.16.1.0 0.0.0.255 area 0
    network 10.0.0.0 0.0.0.255 area 0

Redistribución entre protocolos

    router eigrp 100
    redistribute ospf 1 metric 10000 100 255 1 1500

    router ospf 1
    redistribute eigrp 100 subnets


## Explicación de Comandos

### no auto-summary
Desactiva la sumarización automática en EIGRP.  
Permite que se anuncien las subredes específicas (por ejemplo, 172.16.1.0/24) en lugar de la red completa por clase (172.16.0.0/16).  
Esto evita errores de enrutamiento en redes discontiguas o con VLSM.

## Redistribución entre Protocolos

El comando de redistribución permite que un protocolo de enrutamiento comparta las rutas aprendidas con otro.  
En este caso, EIGRP importará rutas desde OSPF y OSPF importará rutas desde EIGRP.

### redistribuir OSPF hacia EIGRP
router eigrp 100
redistribute ospf 1 metric 10000 100 255 1 1500

### Significado de cada parámetro:
- **redistribute ospf 1:** Indica que se redistribuirán las rutas aprendidas desde el proceso OSPF número 1 hacia EIGRP.
- **metric:** Define manualmente los valores que EIGRP necesita para calcular su métrica compuesta.

| Parámetro | Significado | Descripción |
|------------|--------------|-------------|
| 10000 | Bandwidth | Ancho de banda expresado en Kbps inverso. |
| 100 | Delay | Retardo total de la ruta en décimas de microsegundo. |
| 255 | Reliability | Confiabilidad del enlace (0–255, donde 255 es el máximo). |
| 1 | Load | Carga actual del enlace (1–255, donde 1 indica baja carga). |
| 1500 | MTU | Tamaño máximo de unidad de transmisión en bytes. |

### redistribuir EIGRP hacia OSPF
router ospf 1
redistribute eigrp 100 subnets

El parámetro **subnets** indica que deben redistribuirse todas las subredes aprendidas por EIGRP, no solo las redes claseful.

## Comandos de Verificación
show ip route  
show ip protocols  
show ip eigrp topology  
show ip ospf database
