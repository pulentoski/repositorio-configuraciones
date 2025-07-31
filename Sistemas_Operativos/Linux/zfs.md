# Guía : ZFS y RAID en Linux

## 1. Introducción a ZFS

ZFS (Zettabyte File System) es un sistema de archivos moderno que combina gestión de volúmenes y
archivos. Proporciona alta integridad de datos, tolerancia a fallos y escalabilidad.

## 2. Lógica de Discos, RAID y RAID-Z
RAID (Redundant Array of Independent Disks) permite combinar discos para redundancia o rendimiento.
RAID-Z es la versión mejorada de ZFS que incluye verificación de datos y tolerancia avanzada a fallos.

# 3. Tipos de Pools en ZFS
## A. Striped Pool (RAID 0)
 - Comando:
   
       zpool create mi_pool /dev/sdb /dev/sdc /dev/sdd
Sin redundancia, mayor rendimiento.

## B. Mirror Pool (RAID 1)
 - Comando:

 
       zpool create mi_pool mirror /dev/sdb /dev/sdc
Redundancia total: un disco puede fallar.

## C. RAID-Z1 (RAID 5)
 - Comando:
   
        zpool create mi_pool raidz /dev/sdb /dev/sdc /dev/sdd
Tolerancia a 1 disco fallido.
   
## D. RAID-Z2 (RAID 6)
 - Comando:

        zpool create mi_pool raidz2 /dev/sdb /dev/sdc /dev/sdd /dev/sde
Tolerancia a 2 discos fallidos.
   
## E. RAID-Z3
 - Comando:
   
       zpool create mi_pool raidz3 /dev/sdb /dev/sdc /dev/sdd /dev/sde /dev/sdf /dev/sdg
Tolerancia a 3 discos fallidos.
   
## Crear el dataset (paso final de configuración)
    zfs create pool-ruz/datos
______________________________________________________________________________

# ZFS vs RAID Tradicional

| Tipo ZFS  | Equivalente RAID       | Discos Mínimos | Capacidad Útil        | Tolerancia a Fallos |
|-----------|------------------------|----------------|-----------------------|---------------------|
| Striped   | RAID 0                 | 1              | 100%                  | 0 discos            |
| Mirror    | RAID 1                 | 2              | 50% (o 1/N si N > 2)  | N-1 discos          |
| RAID-Z1   | RAID 5                 | 3              | N-1 discos            | 1 disco             |
| RAID-Z2   | RAID 6                 | 4              | N-2 discos            | 2 discos            |
| RAID-Z3   | RAID 7 (no estándar)   | 5              | N-3 discos            | 3 discos            |

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

# Administrar Pools ZFS
## 1. Listar y Verificar

    zpool list                # Muestra todos los pools  
    zpool status [pool]       # Estado detallado (discos, errores)  

 
## 2. Eliminar Pool ⚠️ (¡CUIDADO! Borra todo)

    zpool destroy [pool]      # Elimina pool y datos  
    zpool destroy -f [pool]   # Fuerza eliminación si está en uso  

## 3. Exportar/Importar (para mover o recuperar pools)

       zpool export [pool]       # Desmontar seguro  
       zpool import [pool]       # Volver a montar  

## 5. Reemplazar Disco Dañado

       zpool replace [pool] [disco_viejo] [disco_nuevo]  
       Ejemplo: zpool replace mi_pool /dev/sdb /dev/sdz

## 6. Verificar Integridad (corrige errores)

       zpool scrub [pool]  

# 💡 Ejemplo Rápido: Reiniciar Configuración
Borrar pool (si existe):

    zpool destroy testpool  
Crear nuevo pool RAID-Z1:

    zpool create testpool raidz1 sdb sdc sdd  
Verificar:

    zpool status testpool  

🔹 Tips Clave: 

- Backup antes de destruir.

- RAID-Z no permite añadir discos sueltos, solo nuevos grupos (ej: otro RAID-Z1).

- Usa zfs para gestionar datasets (archivos/volúmenes dentro del pool).
