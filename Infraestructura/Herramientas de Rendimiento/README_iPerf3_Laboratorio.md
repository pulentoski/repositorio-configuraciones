# 🚀 Guía Práctica de iPerf3

## Medición de rendimiento, diagnóstico de redes y evaluación experimental de enlaces

> **Laboratorio académico de Redes de Datos / Telecomunicaciones**\
> Nivel: técnico--intermedio\
> Modalidad: práctica guiada + análisis de resultados

------------------------------------------------------------------------

## 📚 1. Presentación

**iPerf3** es una herramienta de medición activa de rendimiento de redes
IP. Funciona mediante un modelo **cliente--servidor**: un equipo genera
tráfico y el otro lo recibe, permitiendo observar cuánto tráfico puede
transportar el camino de red bajo determinadas condiciones.

Es especialmente útil para:

-   📶 medir **throughput** o rendimiento efectivo;
-   🔄 comparar tráfico en diferentes direcciones;
-   🚦 estudiar **TCP, UDP y SCTP**;
-   📦 observar pérdida de datagramas y jitter en UDP;
-   🧵 evaluar el efecto de múltiples flujos paralelos;
-   🖥️ detectar limitaciones de CPU, buffers, NIC o sistema operativo;
-   🌐 comparar IPv4 e IPv6;
-   🧪 realizar pruebas controladas sobre enlaces Ethernet, Wi-Fi, VLAN,
    VPN y otros caminos IP;
-   📊 generar resultados en JSON para análisis automatizado.

La documentación oficial de iPerf3 indica que la herramienta está
diseñada para realizar mediciones de throughput y que puede trabajar con
TCP, UDP y SCTP. El proyecto también señala que las opciones disponibles
deben verificarse con la versión instalada, ya que algunas capacidades
dependen de la plataforma y de cómo fue compilado iPerf3.

------------------------------------------------------------------------

## 🎯 2. Objetivos de aprendizaje

Al finalizar este laboratorio, el estudiante será capaz de:

1.  Explicar el modelo cliente--servidor utilizado por iPerf3.
2.  Diferenciar **throughput**, capacidad nominal del enlace, pérdida de
    paquetes y jitter.
3.  Instalar y verificar iPerf3.
4.  Ejecutar pruebas TCP y UDP.
5.  Utilizar pruebas normales, inversas y bidireccionales.
6.  Analizar el efecto de múltiples streams.
7.  Interpretar retransmisiones TCP.
8.  Analizar pérdida de datagramas y jitter en UDP.
9.  Identificar posibles cuellos de botella.
10. Diseñar una prueba experimental sobre un cable Ethernet.
11. Documentar resultados de forma técnica y reproducible.

------------------------------------------------------------------------

# 🔎 3. ¿Qué es iPerf3?

iPerf3 es una aplicación de línea de comandos que genera tráfico de red
de forma controlada para medir el rendimiento de una comunicación IP.

Su arquitectura básica es:

``` text
             RED / ENLACE BAJO PRUEBA
      ┌─────────────────────────────────────┐
      │                                     │
┌─────▼─────┐                         ┌─────▼─────┐
│  CLIENTE  │ ─────── tráfico ──────► │ SERVIDOR  │
│  iPerf3   │                         │  iPerf3   │
└───────────┘                         └───────────┘
```

El servidor se ejecuta normalmente con:

``` bash
iperf3 -s
```

El cliente se conecta indicando la dirección del servidor:

``` bash
iperf3 -c 192.168.1.50
```

Por defecto, el cliente transmite hacia el servidor. Con `-R` se
invierte la dirección.

### ⚠️ Concepto fundamental

**iPerf3 no mide directamente "la capacidad del cable" como lo haría un
certificador de cableado.**

iPerf3 mide el rendimiento de un **camino de comunicación IP completo**.

Por ejemplo:

``` text
Cable
  ↓
Conectores
  ↓
NIC
  ↓
Controlador
  ↓
Sistema operativo
  ↓
TCP/UDP
  ↓
iPerf3
```

Por esta razón, una prueba con iPerf3 puede revelar que un enlace no
alcanza el rendimiento esperado, pero **no puede por sí sola certificar
que un cable cumple Cat 5e, Cat 6 o una norma específica de cableado
estructurado**.

Para certificar físicamente el cableado se utilizan instrumentos
especializados.

------------------------------------------------------------------------

# 🧠 4. Conceptos que debes dominar

  -----------------------------------------------------------------------
  Concepto                            Significado
  ----------------------------------- -----------------------------------
  **Bandwidth / capacidad nominal**   Capacidad teórica o contratada de
                                      un enlace.

  **Throughput**                      Tasa efectiva de datos observada
                                      durante una prueba.

  **Goodput**                         Datos útiles entregados,
                                      descontando determinados
                                      overheads/retransmisiones.

  **Latencia**                        Tiempo necesario para que un
                                      paquete atraviese un camino.

  **Jitter**                          Variación temporal observada entre
                                      paquetes, especialmente relevante
                                      en UDP.

  **Packet Loss**                     Datagramas enviados que no llegan
                                      correctamente al receptor.

  **Retransmissions**                 Segmentos TCP retransmitidos debido
                                      a pérdidas u otras condiciones.

  **RTT**                             Round Trip Time: tiempo de ida y
                                      vuelta.

  **MTU**                             Maximum Transmission Unit.

  **MSS**                             Maximum Segment Size utilizado por
                                      TCP/SCTP.

  **Stream**                          Flujo independiente de tráfico
                                      generado por iPerf3.

  **Full-Duplex**                     Transmisión simultánea en ambas
                                      direcciones.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 🛠️ 5. Instalación

## Debian / Ubuntu / Kali Linux

``` bash
sudo apt update
sudo apt install iperf3
```

Verificar:

``` bash
iperf3 --version
```

Consultar ayuda:

``` bash
iperf3 --help
```

> 💡 **Regla de laboratorio:** antes de comenzar, registra la versión
> instalada. Dos equipos con versiones diferentes pueden disponer de
> capacidades distintas.

------------------------------------------------------------------------

# 🔌 6. Preparación de un laboratorio básico

Se recomienda utilizar dos equipos:

``` text
Equipo A                         Equipo B
192.168.100.1/24                 192.168.100.2/24
     │                                  │
     └──────── Cable / Switch ──────────┘
```

Para una prueba de cable aislada:

-   utilizar NIC Gigabit Ethernet o superior;
-   desactivar Wi-Fi cuando sea posible;
-   evitar tráfico adicional;
-   utilizar IPs estáticas;
-   verificar conectividad;
-   comprobar la velocidad negociada de la interfaz.

Ejemplo en Linux:

``` bash
ip addr
ip link
```

Para revisar la negociación Ethernet:

``` bash
sudo ethtool eth0
```

Buscar especialmente:

``` text
Speed:
Duplex:
Link detected:
```

### ⚠️ Importante

Si la NIC negocia a **100 Mb/s**, no tiene sentido esperar
aproximadamente 940 Mb/s aunque el cable sea Cat 6.

El rendimiento final está condicionado por el elemento más restrictivo
del camino.

------------------------------------------------------------------------

# 🖥️ 7. Modelo de operación

## 7.1 Iniciar servidor

En el Equipo A:

``` bash
iperf3 -s
```

Servidor en un puerto diferente:

``` bash
iperf3 -s -p 5002
```

## 7.2 Ejecutar cliente

En el Equipo B:

``` bash
iperf3 -c 192.168.100.1
```

Con puerto personalizado:

``` bash
iperf3 -c 192.168.100.1 -p 5002
```

------------------------------------------------------------------------

# 🧪 8. Pruebas técnicas con iPerf3

## 8.1 Prueba TCP básica

``` bash
iperf3 -c 192.168.100.1
```

### ¿Qué estudia?

-   throughput TCP;
-   comportamiento de una conexión;
-   retransmisiones;
-   rendimiento promedio.

Duración personalizada:

``` bash
iperf3 -c 192.168.100.1 -t 30
```

Intervalos de reporte cada 2 segundos:

``` bash
iperf3 -c 192.168.100.1 -t 30 -i 2
```

------------------------------------------------------------------------

## 8.2 Prueba TCP con múltiples streams

``` bash
iperf3 -c 192.168.100.1 -P 4 -t 30
```

Crea cuatro flujos TCP paralelos.

### ¿Por qué utilizar varios streams?

Un único flujo puede no saturar completamente un enlace debido a:

-   ventana TCP;
-   algoritmo de congestión;
-   latencia;
-   CPU;
-   implementación del sistema operativo;
-   características de la ruta.

Por ello, comparar:

``` bash
iperf3 -c 192.168.100.1 -t 30
```

contra:

``` bash
iperf3 -c 192.168.100.1 -P 4 -t 30
```

puede ayudar a identificar limitaciones.

------------------------------------------------------------------------

## 8.3 Prueba TCP inversa

``` bash
iperf3 -c 192.168.100.1 -R -t 30
```

La dirección cambia:

``` text
Normal:
Cliente ─────────► Servidor

Reverse:
Cliente ◄───────── Servidor
```

Es útil para comparar rendimiento de subida y bajada.

------------------------------------------------------------------------

## 8.4 Prueba bidireccional

``` bash
iperf3 -c 192.168.100.1 --bidir -t 30
```

Ambos extremos transmiten simultáneamente.

Permite estudiar:

-   comportamiento full-duplex;
-   saturación;
-   asimetrías;
-   limitaciones de CPU;
-   comportamiento bajo tráfico simultáneo.

------------------------------------------------------------------------

## 8.5 Prueba UDP

``` bash
iperf3 -c 192.168.100.1 -u -b 100M -t 20
```

Aquí se fija una tasa objetivo de 100 Mbit/s.

UDP permite estudiar especialmente:

-   jitter;
-   datagramas enviados;
-   datagramas recibidos;
-   pérdida;
-   tasa efectiva.

### ⚠️ Atención

UDP no funciona como TCP.

TCP adapta su comportamiento según congestión y condiciones de red. UDP
permite generar una tasa configurada por el usuario y, si el camino no
puede sostenerla, pueden aparecer pérdidas.

------------------------------------------------------------------------

## 8.6 Prueba UDP a 500 Mbit/s

``` bash
iperf3 -c 192.168.100.1 -u -b 500M -t 20
```

------------------------------------------------------------------------

## 8.7 Prueba UDP de alta carga

``` bash
iperf3 -c 192.168.100.1 -u -b 900M -t 20 -i 1
```

Esto permite observar qué sucede cuando el tráfico generado se aproxima
a la capacidad de un enlace Gigabit.

> ⚠️ No asumas que "900M" significa que necesariamente circularán 900
> Mbit/s útiles. La tasa configurada es un objetivo de generación; el
> resultado real depende del camino y de los extremos.

------------------------------------------------------------------------

## 8.8 Modificar el tamaño de buffer

``` bash
iperf3 -c 192.168.100.1 -l 64K
```

El parámetro `-l` modifica la longitud del buffer utilizado por iPerf3.

Es una excelente variable para experimentar con:

-   tamaño de transferencia;
-   overhead;
-   comportamiento de UDP;
-   MTU;
-   rendimiento del sistema.

------------------------------------------------------------------------

## 8.9 Modificar la ventana/socket buffer

``` bash
iperf3 -c 192.168.100.1 -w 1M
```

Permite estudiar el efecto de buffers y ventanas TCP.

------------------------------------------------------------------------

## 8.10 Desactivar Nagle

``` bash
iperf3 -c 192.168.100.1 -N
```

`-N` activa TCP_NODELAY y deshabilita el algoritmo de Nagle.

Útil para estudiar el comportamiento de tráfico TCP con paquetes
pequeños.

------------------------------------------------------------------------

## 8.11 Utilizar IPv4

``` bash
iperf3 -c 192.168.100.1 -4
```

## 8.12 Utilizar IPv6

``` bash
iperf3 -c 2001:db8::1 -6
```

------------------------------------------------------------------------

## 8.13 Generar resultados JSON

``` bash
iperf3 -c 192.168.100.1 -t 20 -J
```

Esto resulta útil para:

-   automatización;
-   scripts;
-   dashboards;
-   análisis con Python;
-   integración con sistemas de monitoreo.

JSON en flujo:

``` bash
iperf3 -c 192.168.100.1 -J --json-stream
```

------------------------------------------------------------------------

## 8.14 Guardar resultados en archivo

``` bash
iperf3 -c 192.168.100.1 -t 30 --logfile resultado.txt
```

------------------------------------------------------------------------

## 8.15 Omitir el inicio de la prueba

``` bash
iperf3 -c 192.168.100.1 -t 30 -O 5
```

Los primeros 5 segundos se utilizan como período inicial y sus
estadísticas se excluyen del resultado.

Esto puede ser útil en TCP para evitar que el período inicial de **slow
start** distorsione el análisis del régimen estable.

------------------------------------------------------------------------

## 8.16 Utilizar múltiples streams y omitir slow start

``` bash
iperf3 -c 192.168.100.1 -P 4 -t 30 -O 5 -i 2
```

------------------------------------------------------------------------

## 8.17 Prueba con un número de bytes

``` bash
iperf3 -c 192.168.100.1 -n 1G
```

La prueba termina al transferir la cantidad especificada.

------------------------------------------------------------------------

## 8.18 Prueba por cantidad de bloques

``` bash
iperf3 -c 192.168.100.1 -k 100000
```

`-k` y `-n` son alternativas al tiempo de prueba.

------------------------------------------------------------------------

## 8.19 Prueba con CPU affinity

``` bash
iperf3 -c 192.168.100.1 -A 2
```

Permite asociar el proceso a una CPU concreta cuando la plataforma lo
admite.

Es especialmente útil cuando se quiere investigar si la CPU es un factor
limitante.

------------------------------------------------------------------------

## 8.20 Seleccionar interfaz

``` bash
iperf3 -c 192.168.100.1 -B 192.168.100.2
```

En sistemas compatibles también se puede utilizar:

``` bash
iperf3 -c 192.168.100.1 --bind-dev eth0
```

------------------------------------------------------------------------

## 8.21 Cambiar el algoritmo de congestión TCP

En Linux y FreeBSD:

``` bash
iperf3 -c 192.168.100.1 -C cubic
```

También puede utilizarse, por ejemplo:

``` bash
iperf3 -c 192.168.100.1 -C reno
```

El objetivo de laboratorio es comparar cómo el algoritmo de control de
congestión puede afectar el throughput.

------------------------------------------------------------------------

## 8.22 Prueba MPTCP

Cuando el sistema y la versión de iPerf3 lo soportan:

``` bash
iperf3 -c 192.168.100.1 --mptcp
```

Permite investigar Multipath TCP.

------------------------------------------------------------------------

## 8.23 Zero-copy

``` bash
iperf3 -c 192.168.100.1 -Z
```

Puede reducir determinadas operaciones de copia durante el envío.

> 🧠 No debe utilizarse automáticamente para todas las mediciones. Si el
> objetivo es estudiar el rendimiento "normal" de una aplicación,
> conviene establecer primero una línea base sin optimizaciones
> especiales.

------------------------------------------------------------------------

## 8.24 Medición utilizando archivo

``` bash
iperf3 -c 192.168.100.1 -F archivo.bin
```

Esta modalidad permite investigar si el almacenamiento puede convertirse
en un cuello de botella.

No convierte a iPerf3 en una herramienta general de transferencia de
archivos.

No está disponible para pruebas UDP.

------------------------------------------------------------------------

# 📋 9. Tabla completa de parámetros de iPerf3

> **Nota de compatibilidad:** esta tabla toma como referencia la
> documentación oficial de iPerf3 3.21. La disponibilidad de ciertas
> opciones puede depender del sistema operativo, librerías y
> características con las que fue compilado el programa. Ejecuta siempre
> `iperf3 --help` y `iperf3 --version` en tu equipo antes de diseñar una
> práctica.

## 9.1 Opciones generales

  --------------------------------------------------------------------------------------
  Parámetro         Equivalente largo             Función              Ámbito
  ----------------- ----------------------------- -------------------- -----------------
  `-p n`            `--port n`                    Define el puerto TCP General
                                                  de control/escucha.  
                                                  Predeterminado:      
                                                  5201.                

  `-f fmt`          `--format fmt`                Define unidades:     General
                                                  Kbits, Mbits, Gbits  
                                                  o Tbits.             

  `-i n`            `--interval n`                Intervalo de         General
                                                  reportes en          
                                                  segundos. `0`        
                                                  desactiva reportes   
                                                  periódicos.          

  `-I file`         `--pidfile file`              Escribe el PID del   General
                                                  proceso en un        
                                                  archivo.             

  `-F file`         `--file file`                 Usa un archivo como  General
                                                  fuente o destino de  
                                                  datos. No disponible 
                                                  con UDP.             

  `-A n`            `--affinity n`                Fija afinidad de     General
                                                  CPU. En cliente      
                                                  puede utilizar       
                                                  `n,m`.               

  `-B host`         `--bind host`                 Vincula iPerf3 a una General
                                                  dirección/interfaz   
                                                  específica.          

  ---               `--bind-dev dev`              Vincula el proceso a General
                                                  una interfaz         
                                                  concreta.            

  `-V`              `--verbose`                   Muestra información  General
                                                  más detallada.       

  `-J`              `--json`                      Produce salida JSON. General

  ---               `--json-stream`               Produce JSON         General
                                                  delimitado por       
                                                  líneas.              

  ---               `--json-stream-full-output`   JSON completo junto  General
                                                  con JSON streaming.  

  ---               `--logfile file`              Envía la salida a un General
                                                  archivo.             

  ---               `--forceflush`                Fuerza el vaciado de General
                                                  salida en cada       
                                                  intervalo.           

  ---               `--timestamps[=format]`       Agrega timestamps a  General
                                                  cada línea.          

  ---               `--rcv-timeout ms`            Timeout de recepción General
                                                  durante una prueba.  

  ---               `--snd-timeout ms`            Timeout de datos TCP General
                                                  no reconocidos.      

  ---               `--use-pkcs1-padding`         Compatibilidad con   General
                                                  el método de padding 
                                                  antiguo de           
                                                  autenticación.       

  `-m`              `--mptcp`                     Utiliza MPTCP cuando General
                                                  aplica a TCP.        

  `-d`              `--debug`                     Activa salida de     General
                                                  depuración.          

  `-v`              `--version`                   Muestra versión.     General

  `-h`              `--help`                      Muestra ayuda.       General
  --------------------------------------------------------------------------------------

## 9.2 Opciones del servidor

  --------------------------------------------------------------------------------------
  Parámetro                              Función                 Ámbito
  -------------------------------------- ----------------------- -----------------------
  `-s` / `--server`                      Ejecuta iPerf3 en modo  Servidor
                                         servidor.               

  `-D` / `--daemon`                      Ejecuta el servidor     Servidor
                                         como daemon.            

  `-1` / `--one-off`                     Atiende como máximo una Servidor
                                         conexión y termina.     

  `--idle-timeout n`                     Reinicia/termina el     Servidor
                                         servidor según el       
                                         tiempo de inactividad   
                                         configurado.            

  `--server-max-duration n`              Limita la duración      Servidor
                                         máxima de una prueba    
                                         contra el servidor.     

  `--server-bitrate-limit n[KMGT][/n]`   Limita la tasa          Servidor
                                         permitida por el        
                                         servidor.               

  `--rsa-private-key-path file`          Ruta de la clave        Servidor
                                         privada RSA para        
                                         autenticación.          

  `--authorized-users-path file`         Archivo con usuarios    Servidor
                                         autorizados y hashes de 
                                         contraseña.             

  `--time-skew-threshold seconds`        Define tolerancia de    Servidor
                                         diferencia temporal     
                                         para autenticación.     
  --------------------------------------------------------------------------------------

## 9.3 Opciones del cliente

  ------------------------------------------------------------------------------
  Parámetro                      Función                 Ámbito
  ------------------------------ ----------------------- -----------------------
  `-c host` / `--client host`    Ejecuta modo cliente y  Cliente
                                 conecta al servidor.    

  `--sctp`                       Utiliza SCTP en lugar   Cliente
                                 de TCP.                 

  `-u` / `--udp`                 Utiliza UDP.            Cliente

  `--connect-timeout n`          Timeout de conexión     Cliente
                                 inicial en              
                                 milisegundos.           

  `-b rate` / `--bitrate rate`   Define tasa objetivo.   Cliente
                                 UDP predeterminado: 1   
                                 Mbit/s; TCP/SCTP: sin   
                                 límite.                 

  `--pacing-timer n`             Configura intervalo del Cliente
                                 temporizador de pacing  
                                 interno.                

  `--fq-rate rate`               Utiliza pacing basado   Cliente
                                 en fair queueing.       

  `--no-fq-socket-pacing`        Desactiva/establece en  Cliente
                                 cero el socket pacing   
                                 FQ. Está deprecado.     

  `-t n` / `--time n`            Duración de la prueba.  Cliente
                                 Predeterminado: 10 s.   

  `-n n` / `--bytes n`           Cantidad de bytes a     Cliente
                                 transmitir.             

  `-k n` / `--blockcount n`      Número de               Cliente
                                 bloques/paquetes a      
                                 transmitir.             

  `-l n` / `--length n`          Tamaño del buffer de    Cliente
                                 lectura/escritura.      

  `--cport port`                 Puerto de origen de los Cliente
                                 streams de datos.       

  `-P n` / `--parallel n`        Número de streams       Cliente
                                 paralelos.              

  `-R` / `--reverse`             El servidor transmite   Cliente
                                 hacia el cliente.       

  `--bidir`                      Transmisión simultánea  Cliente
                                 en ambas direcciones.   

  `-w n` / `--window n`          Tamaño de socket        Cliente
                                 buffer/ventana.         

  `-M n` / `--set-mss n`         Define MSS TCP/SCTP.    Cliente

  `-N` / `--no-delay`            Deshabilita Nagle       Cliente
                                 mediante TCP_NODELAY.   

  `-4` / `--version4`            Fuerza IPv4.            Cliente

  `-6` / `--version6`            Fuerza IPv6.            Cliente

  `-S n` / `--tos n`             Define bits IP ToS.     Cliente

  `--dscp value`                 Define DSCP numérico o  Cliente
                                 simbólico.              

  `-L n` / `--flowlabel n`       Define IPv6 Flow Label. Cliente

  `-X name` / `--xbind name`     Vincula asociaciones    Cliente/SCTP
                                 SCTP a enlaces          
                                 específicos.            

  `--nstreams n`                 Define número de        Cliente/SCTP
                                 streams SCTP.           

  `-Z` / `--zerocopy`            Utiliza método de envío Cliente
                                 zero-copy.              

  `--skip-rx-copy`               Evita copiar datos      Cliente
                                 recibidos al espacio de 
                                 usuario mediante        
                                 MSG_TRUNC.              

  `-O n` / `--omit n`            Omite estadísticas de   Cliente
                                 los primeros n          
                                 segundos.               

  `-T str` / `--title str`       Agrega un prefijo a     Cliente
                                 cada línea de salida.   

  `--extra-data str`             Agrega información      Cliente
                                 adicional al JSON.      

  `-C algo` /                    Selecciona algoritmo de Cliente
  `--congestion algo`            congestión TCP.         

  `--get-server-output`          Recupera la salida      Cliente
                                 generada por el         
                                 servidor.               

  `--udp-counters-64bit`         Utiliza contadores UDP  Cliente/UDP
                                 de 64 bits.             

  `--repeating-payload`          Usa un patrón           Cliente
                                 repetitivo en lugar de  
                                 payload aleatorio.      

  `--dont-fragment`              Activa IPv4 Don't       Cliente/UDP
                                 Fragment para UDP sobre 
                                 IPv4.                   

  `--username username`          Usuario para            Cliente
                                 autenticación del       
                                 servidor.               

  `--rsa-public-key-path file`   Ruta de la clave        Cliente
                                 pública RSA utilizada   
                                 para autenticación.     
  ------------------------------------------------------------------------------

------------------------------------------------------------------------

# 📊 10. Parámetros que debes dominar primero

Aunque iPerf3 tiene muchas opciones, para un laboratorio de redes no es
necesario memorizar todas.

  Prioridad   Parámetros       ¿Para qué?
  ----------- ---------------- -------------------
  ⭐⭐⭐      `-s`             Servidor
  ⭐⭐⭐      `-c`             Cliente
  ⭐⭐⭐      `-t`             Duración
  ⭐⭐⭐      `-i`             Intervalo
  ⭐⭐⭐      `-P`             Streams paralelos
  ⭐⭐⭐      `-u`             UDP
  ⭐⭐⭐      `-b`             Tasa objetivo UDP
  ⭐⭐⭐      `-R`             Dirección inversa
  ⭐⭐⭐      `--bidir`        Ambas direcciones
  ⭐⭐        `-J`             JSON
  ⭐⭐        `-4`, `-6`       IPv4 / IPv6
  ⭐⭐        `-w`             Ventana/buffer
  ⭐⭐        `-l`             Tamaño de buffer
  ⭐⭐        `-O`             Omitir inicio
  ⭐⭐        `-C`             Congestión TCP
  ⭐          `-A`             Afinidad CPU
  ⭐          `-Z`             Zero-copy
  ⭐          `-M`             MSS
  ⭐          `-S`, `--dscp`   QoS/DSCP
  ⭐          `--mptcp`        Multipath TCP
  ⭐          `--sctp`         SCTP

------------------------------------------------------------------------

# 🧪 11. ACTIVIDAD 1 --- Evaluación experimental de un cable Ethernet

## 🎯 Objetivo

Seleccionar un cable Ethernet disponible en el laboratorio,
independientemente de que sea **Cat 5, Cat 5e o Cat 6**, construir un
escenario controlado y determinar el rendimiento IP observado mediante
iPerf3.

### ⚠️ Corrección conceptual importante

El objetivo **no** será afirmar:

> "iPerf3 certificó que este cable es Cat 6".

Eso sería técnicamente incorrecto.

El objetivo será:

> **Medir el rendimiento observado al utilizar el cable dentro de un
> enlace Ethernet y analizar si existen evidencias de limitación de
> rendimiento.**

La categoría del cable debe registrarse mediante su rotulado,
documentación o identificación física, no deducirse exclusivamente del
resultado de iPerf3.

------------------------------------------------------------------------

## 🧰 Materiales

-   [ ] 2 computadores con Ethernet.
-   [ ] 1 cable Ethernet seleccionado por el grupo.
-   [ ] iPerf3 instalado en ambos equipos.
-   [ ] 2 cables de alimentación.
-   [ ] Acceso a terminal.
-   [ ] Opcional: switch administrable.
-   [ ] Opcional: `ethtool`.

------------------------------------------------------------------------

## 🔬 Escenario A --- Conexión directa

``` text
Equipo A                              Equipo B
192.168.100.1/24                     192.168.100.2/24
       │                                      │
       └──────────── CABLE UTP ──────────────┘
                    BAJO PRUEBA
```

### Paso 1 --- Registrar características

Cada grupo debe registrar:

  Dato                     Resultado
  ------------------------ -----------
  Categoría declarada      
  Longitud aproximada      
  Tipo de conector         
  Tipo de terminación      
  Velocidad NIC Equipo A   
  Velocidad NIC Equipo B   
  Duplex                   
  Sistema operativo        
  Versión iPerf3           

------------------------------------------------------------------------

## Paso 2 --- Verificar la negociación

Linux:

``` bash
sudo ethtool eth0
```

Registrar:

``` text
Speed:
Duplex:
Link detected:
```

------------------------------------------------------------------------

## Paso 3 --- Configurar IP

Equipo A:

``` text
IP: 192.168.100.1
Máscara: 255.255.255.0
```

Equipo B:

``` text
IP: 192.168.100.2
Máscara: 255.255.255.0
```

Probar:

``` bash
ping 192.168.100.2
```

------------------------------------------------------------------------

## Paso 4 --- Iniciar servidor

Equipo A:

``` bash
iperf3 -s
```

------------------------------------------------------------------------

## Paso 5 --- Prueba TCP base

Equipo B:

``` bash
iperf3 -c 192.168.100.1 -t 30 -i 2
```

Registrar:

-   throughput promedio;
-   throughput máximo observado;
-   retransmisiones;
-   intervalo de prueba;
-   velocidad negociada.

------------------------------------------------------------------------

## Paso 6 --- Prueba TCP con paralelismo

``` bash
iperf3 -c 192.168.100.1 -t 30 -P 4 -i 2
```

Comparar con la prueba anterior.

------------------------------------------------------------------------

## Paso 7 --- Prueba inversa

``` bash
iperf3 -c 192.168.100.1 -R -t 30 -i 2
```

------------------------------------------------------------------------

## Paso 8 --- Prueba bidireccional

``` bash
iperf3 -c 192.168.100.1 --bidir -t 30 -i 2
```

------------------------------------------------------------------------

## Paso 9 --- Repetibilidad

Cada prueba debe ejecutarse al menos **3 veces**.

Tabla sugerida:

  Prueba            Repetición 1   Repetición 2   Repetición 3   Promedio
  --------------- -------------- -------------- -------------- ----------
  TCP                                                          
  TCP `-P 4`                                                   
  Reverse                                                      
  Bidireccional                                                

### Preguntas de análisis

1.  ¿La velocidad negociada coincide con la esperada?
2.  ¿El throughput se aproxima al máximo práctico del enlace?
3.  ¿Aumentar `-P` modificó significativamente el resultado?
4.  ¿La prueba reverse obtuvo un resultado diferente?
5.  ¿Qué ocurrió durante `--bidir`?
6.  ¿Se observaron retransmisiones?
7.  ¿Qué otros componentes podrían explicar un resultado inferior?
8.  ¿El resultado permite certificar la categoría del cable? ¿Por qué?

------------------------------------------------------------------------

# 🧪 12. ACTIVIDAD 2 --- Análisis de estabilidad mediante UDP

## 🎯 Objetivo

Analizar el comportamiento de un enlace bajo una tasa de tráfico UDP
controlada, observando:

-   throughput;
-   jitter;
-   datagramas enviados;
-   datagramas recibidos;
-   pérdida de paquetes.

------------------------------------------------------------------------

## Paso 1 --- Servidor

Equipo A:

``` bash
iperf3 -s
```

------------------------------------------------------------------------

## Paso 2 --- Prueba UDP

Equipo B:

``` bash
iperf3 -c 192.168.100.1 -u -b 100M -t 20 -i 1
```

------------------------------------------------------------------------

## Paso 3 --- Incrementar progresivamente la carga

Ejecutar:

``` bash
iperf3 -c 192.168.100.1 -u -b 100M -t 20
```

``` bash
iperf3 -c 192.168.100.1 -u -b 500M -t 20
```

``` bash
iperf3 -c 192.168.100.1 -u -b 800M -t 20
```

``` bash
iperf3 -c 192.168.100.1 -u -b 900M -t 20
```

Si el hardware y la red lo permiten, el docente puede proponer cargas
superiores.

------------------------------------------------------------------------

## 📊 Tabla de registro

  --------------------------------------------------------------------------------
          Tasa   Throughput       Jitter      Pérdida   Datagramas Observaciones
      objetivo                                                     
  ------------ ------------ ------------ ------------ ------------ ---------------
    100 Mbit/s                                                     

    500 Mbit/s                                                     

    800 Mbit/s                                                     

    900 Mbit/s                                                     
  --------------------------------------------------------------------------------

### Preguntas

1.  ¿En qué tasa comienza a aumentar significativamente el jitter?
2.  ¿En qué punto aparece pérdida?
3.  ¿La pérdida aumenta de forma lineal?
4.  ¿Qué relación existe entre tasa objetivo y capacidad disponible?
5.  ¿Qué componentes pueden provocar pérdida antes de saturar
    físicamente el cable?
6.  ¿Qué diferencia conceptual existe entre una pérdida UDP y una
    retransmisión TCP?

### ⚠️ Sobre el "0,1 %"

No debe utilizarse una regla universal como:

> "un enlace saludable siempre debe tener menos de 0,1 % de pérdida".

La interpretación depende del escenario, medio, tasa, dispositivo,
congestión, buffers y objetivo de la prueba.

En este laboratorio los estudiantes deben **medir, comparar y
justificar**, no aplicar un umbral arbitrario sin contexto.

------------------------------------------------------------------------

# 🔬 13. ACTIVIDAD 3 --- Diseño experimental libre

> ⭐ **Desafío para estudiantes avanzados**

Diseña una prueba que permita investigar una de estas hipótesis:

### Opción A --- ¿Más streams = mayor throughput?

Comparar:

``` bash
-P 1
-P 2
-P 4
-P 8
```

Mantener constantes:

-   equipos;
-   cable;
-   duración;
-   dirección;
-   protocolo.

------------------------------------------------------------------------

### Opción B --- ¿El tamaño de buffer afecta el rendimiento?

Comparar:

``` bash
-l 1K
-l 8K
-l 64K
-l 128K
-l 1M
```

------------------------------------------------------------------------

### Opción C --- ¿TCP y UDP se comportan igual?

Comparar:

``` bash
iperf3 -c 192.168.100.1 -t 30
```

contra:

``` bash
iperf3 -c 192.168.100.1 -u -b 500M -t 30
```

------------------------------------------------------------------------

### Opción D --- ¿IPv4 e IPv6 presentan diferencias?

Comparar:

``` bash
iperf3 -c servidor -4 -t 30
```

contra:

``` bash
iperf3 -c servidor -6 -t 30
```

------------------------------------------------------------------------

# 📈 14. Interpretación técnica de resultados

## 14.1 Throughput

El throughput representa la tasa efectiva observada durante la prueba.

Ejemplo:

``` text
[SUM]  0.00-30.00 sec  3.27 GBytes  936 Mbits/sec
```

La conclusión correcta sería:

> "Durante esta prueba se observó un throughput promedio de
> aproximadamente 936 Mbit/s."

No:

> "El cable tiene una capacidad de 936 Mbit/s."

------------------------------------------------------------------------

## 14.2 Retransmisiones TCP

Las retransmisiones pueden indicar:

-   pérdida;
-   congestión;
-   problemas del camino;
-   limitaciones del receptor;
-   condiciones anómalas.

Sin embargo:

> **Una retransmisión no demuestra por sí sola que el cable esté
> defectuoso.**

Debe analizarse junto con el resto de variables.

------------------------------------------------------------------------

## 14.3 Jitter

En UDP, iPerf3 muestra jitter como variación temporal entre la recepción
de datagramas.

Un jitter elevado puede ser relevante para:

-   VoIP;
-   videoconferencia;
-   streaming;
-   aplicaciones interactivas;
-   sistemas de tiempo real.

------------------------------------------------------------------------

## 14.4 Packet Loss

UDP no garantiza entrega.

Por ello, cuando el tráfico generado supera la capacidad efectiva de un
camino, pueden aparecer datagramas perdidos.

Esto permite utilizar UDP como herramienta experimental para observar el
comportamiento de un enlace bajo diferentes cargas.

------------------------------------------------------------------------

# 🧩 15. Metodología correcta para una prueba profesional

Una medición técnicamente válida debe controlar variables.

## Mantener constantes

-   mismo hardware;
-   mismo cable;
-   misma longitud;
-   misma NIC;
-   misma versión de iPerf3;
-   misma configuración IP;
-   misma duración;
-   misma dirección;
-   mismo protocolo;
-   ausencia de tráfico externo significativo.

## Cambiar una variable por vez

Ejemplo:

``` text
Prueba 1 → P = 1
Prueba 2 → P = 2
Prueba 3 → P = 4
Prueba 4 → P = 8
```

No cambiar simultáneamente:

``` text
-P
-t
-l
-w
-C
-u
```

porque posteriormente será difícil determinar qué produjo el cambio.

------------------------------------------------------------------------

# 🧮 16. Ejemplo de análisis

Supongamos:

  Prueba                   Resultado
  --------------- ------------------
  TCP P=1                 915 Mbit/s
  TCP P=4                 942 Mbit/s
  Reverse                 939 Mbit/s
  Bidirectional     930 + 928 Mbit/s

Una interpretación razonable sería:

> El enlace presenta un rendimiento cercano a la capacidad práctica de
> Gigabit Ethernet en las pruebas unidireccionales. El uso de cuatro
> streams incrementó el throughput observado, lo que puede indicar que
> una sola conexión no saturaba completamente el camino. La prueba
> bidireccional mostró capacidad simultánea en ambos sentidos. Estos
> resultados no constituyen una certificación física del cable.

------------------------------------------------------------------------

# 🧪 17. Variables que pueden convertirse en cuello de botella

Cuando el resultado sea inferior al esperado, investigar:

``` text
                    ┌──────────────┐
                    │    Cable     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Conectores    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │     NIC      │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │    Driver    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │     CPU      │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ OS / buffers │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ TCP / UDP    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   iPerf3     │
                    └──────────────┘
```

------------------------------------------------------------------------

# 🧠 18. Errores frecuentes

### ❌ Error 1

"Si el cable es Cat 6, iPerf3 debe mostrar 10 Gbit/s."

**Incorrecto.**

La categoría del cable no determina por sí sola la velocidad negociada
del enlace.

------------------------------------------------------------------------

### ❌ Error 2

"iPerf3 certifica el cable."

**Incorrecto.**

iPerf3 mide rendimiento IP. La certificación del cableado requiere
pruebas físicas específicas.

------------------------------------------------------------------------

### ❌ Error 3

"Si UDP tiene pérdida, el cable está malo."

**Incorrecto.**

Puede existir saturación, buffers insuficientes, CPU limitada, errores
de configuración u otros factores.

------------------------------------------------------------------------

### ❌ Error 4

"El número configurado con `-b` es el throughput obtenido."

**Incorrecto.**

`-b` define una tasa objetivo de generación. El resultado debe
analizarse en la salida de iPerf3.

------------------------------------------------------------------------

### ❌ Error 5

"Una sola prueba es suficiente."

**Incorrecto.**

Una medición aislada no permite evaluar correctamente la repetibilidad.

------------------------------------------------------------------------

# 📝 19. Formato de informe

Cada grupo deberá entregar un informe con:

## 1. Identificación

-   integrantes;
-   fecha;
-   laboratorio;
-   equipos utilizados;
-   sistemas operativos;
-   versiones de iPerf3.

## 2. Topología

Incluir diagrama:

``` text
Equipo A ───── Cable bajo prueba ───── Equipo B
```

## 3. Características del cable

-   categoría declarada;
-   longitud;
-   tipo;
-   conectores;
-   observaciones.

## 4. Configuración

-   IP;
-   máscara;
-   velocidad negociada;
-   duplex;
-   NIC.

## 5. Pruebas

Incluir los comandos utilizados.

## 6. Resultados

Incluir tablas y, opcionalmente, gráficos.

## 7. Análisis

Responder:

-   ¿Cuál fue el throughput?
-   ¿Hubo diferencias entre TCP y UDP?
-   ¿Qué ocurrió al aumentar `-P`?
-   ¿Qué ocurrió en reverse?
-   ¿Qué ocurrió en bidireccional?
-   ¿Hubo pérdida?
-   ¿Hubo retransmisiones?
-   ¿Hubo jitter significativo?
-   ¿Qué variable parece limitar el rendimiento?

## 8. Conclusión

La conclusión debe basarse en evidencia experimental.

------------------------------------------------------------------------

# 🎓 20. Rúbrica sugerida

  Criterio                                        Puntaje
  --------------------------------------------- ---------
  Preparación y configuración del laboratorio          15
  Uso correcto de iPerf3                               20
  Ejecución de pruebas                                 20
  Registro de resultados                               15
  Análisis técnico                                     20
  Conclusiones                                         10
  **Total**                                       **100**

------------------------------------------------------------------------

# 🚀 21. Mini-cheat sheet

### Servidor

``` bash
iperf3 -s
```

### Cliente

``` bash
iperf3 -c 192.168.1.50
```

### 30 segundos

``` bash
iperf3 -c 192.168.1.50 -t 30
```

### Reporte cada 2 segundos

``` bash
iperf3 -c 192.168.1.50 -t 30 -i 2
```

### 4 streams

``` bash
iperf3 -c 192.168.1.50 -P 4
```

### Reverse

``` bash
iperf3 -c 192.168.1.50 -R
```

### Bidireccional

``` bash
iperf3 -c 192.168.1.50 --bidir
```

### UDP

``` bash
iperf3 -c 192.168.1.50 -u -b 100M
```

### JSON

``` bash
iperf3 -c 192.168.1.50 -J
```

### IPv4

``` bash
iperf3 -c 192.168.1.50 -4
```

### IPv6

``` bash
iperf3 -c 2001:db8::1 -6
```

### Omitir primeros 5 segundos

``` bash
iperf3 -c 192.168.1.50 -O 5
```

### Algoritmo TCP

``` bash
iperf3 -c 192.168.1.50 -C cubic
```

### Seleccionar interfaz

``` bash
iperf3 -c 192.168.1.50 -B 192.168.1.20
```

------------------------------------------------------------------------

# 🔐 22. Buenas prácticas de laboratorio

-   Ejecutar pruebas únicamente en redes autorizadas.
-   No generar tráfico de alta intensidad sobre redes productivas sin
    autorización.
-   Definir previamente duración y tasa máxima.
-   Evitar pruebas UDP excesivas sobre infraestructura compartida.
-   Documentar versión de iPerf3.
-   Repetir mediciones.
-   Mantener constantes las variables.
-   No confundir rendimiento IP con certificación física.
-   Interpretar los resultados dentro del contexto de la topología.

------------------------------------------------------------------------

# 📚 23. Referencias técnicas

-   **ESnet / iPerf3 --- documentación oficial:**\
    https://software.es.net/iperf/

-   **ESnet / iPerf3 --- guía de invocación y parámetros:**\
    https://software.es.net/iperf/invoking.html

-   **Repositorio oficial de iPerf:**\
    https://github.com/esnet/iperf

-   **Manual de iPerf3 incluido en el proyecto:**\
    https://github.com/esnet/iperf/blob/master/src/iperf3.1

> 📌 La referencia oficial debe prevalecer sobre apuntes, blogs o
> capturas de pantalla cuando exista una diferencia entre versiones.

------------------------------------------------------------------------

# 🏁 24. Desafío final

## "El detective de redes" 🕵️‍♂️

El docente entrega a cada grupo un escenario donde el rendimiento
observado es inferior al esperado.

Ejemplo:

``` text
Enlace negociado: 1 Gbit/s
Resultado TCP:    420 Mbit/s
Resultado P=4:    790 Mbit/s
Resultado UDP:    850 Mbit/s
Pérdida UDP:      0,8 %
```

### Misión

Determinar qué hipótesis es más probable:

-   [ ] Problema físico.
-   [ ] Limitación de CPU.
-   [ ] Problema de buffers.
-   [ ] TCP no alcanza el máximo con un único flujo.
-   [ ] Saturación.
-   [ ] Problema de configuración.
-   [ ] Limitación de NIC.
-   [ ] Otra hipótesis.

### Regla

**No basta con decir qué creen que ocurre.**

Deben demostrarlo mediante nuevas pruebas.

------------------------------------------------------------------------

# 💡 Idea clave para recordar

> **Medir no es simplemente ejecutar un comando. Medir técnicamente
> significa controlar variables, obtener evidencia, repetir el
> experimento y construir una conclusión que pueda defenderse.**

🚀 **iPerf3 convierte la red en un laboratorio medible.**
