# Guía : ZFS y RAID en Linux

## 1. Introducción a ZFS

ZFS (Zettabyte File System) es un sistema de archivos moderno que combina gestión de volúmenes y
archivos. Proporciona alta integridad de datos, tolerancia a fallos y escalabilidad.

## 2. Lógica de Discos, RAID y RAID-Z
RAID (Redundant Array of Independent Disks) permite combinar discos para redundancia o rendimiento.
RAID-Z es la versión mejorada de ZFS que incluye verificación de datos y tolerancia avanzada a fallos.

## 3. Tipos de Pools en ZFS
A. Striped Pool (RAID 0)
 - Comando: zpool create mi_pool sdb sdc sdd
 - Sin redundancia, mayor rendimiento.

B. Mirror Pool (RAID 1)
 - Comando: zpool create mi_pool mirror sdb sdc
 - Redundancia total: un disco puede fallar.

C. RAID-Z1 (RAID 5)
 - Comando: zpool create mi_pool raidz sdb sdc sdd
 - Tolerancia a 1 disco fallido.
   
D. RAID-Z2 (RAID 6)
 - Comando: zpool create mi_pool raidz2 sdb sdc sdd sde
 - Tolerancia a 2 discos fallidos.
   
E. RAID-Z3
 - Comando: zpool create mi_pool raidz3 sdb sdc sdd sde sdf sdg
 - Tolerancia a 3 discos fallidos.
   


## 4. Capacidad Útil según Configuración
Tipo | Discos mín. | Capacidad útil | Tolerancia a fallos
-----------|-------------|---------------------|----------------------
Striped | 1 | 100% | 0 discos
Mirror | 2 | 50% | N - 1 discos
RAID-Z1 | 3 | N - 1 discos | 1 disco
RAID-Z2 | 4 | N - 2 discos | 2 discos
RAID-Z3 | 5 | N - 3 discos | 3 discos

## 5. Verificación y Uso de Pools
- Ver pool: zpool status
- Montaje automático en /<nombre_del_pool>
- Crear archivo: echo 'Hola ZFS' > /<pool>/archivo.txt

## 6. Problemas comunes
Si los discos tienen firmas anteriores, límpialos con:
wipefs -a /dev/sdX

## 7. Práctica en VirtualBox
- Agrega discos desde la configuración de la VM.
- Verifica con lsblk (ej: sdb, sdc, sdd).
- Crea el pool: zpool create testpool raidz sdb sdc sdd
- Prueba: cd /testpool && touch test.txt
