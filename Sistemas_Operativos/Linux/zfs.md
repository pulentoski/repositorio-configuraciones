# Guía de Comandos: ZFS y RAID en Linux (AlmaLinux)

## Introducción a ZFS

ZFS (Zettabyte File System) es un sistema de archivos avanzado que combina la funcionalidad de gestión de volúmenes y sistema de archivos en una sola solución. Está diseñado para ofrecer alta integridad de datos, tolerancia a fallos, escalabilidad masiva y administración simplificada.

### Diferencia entre `zpool` y `zfs`

* **`zpool`**: Comando para administrar pools de almacenamiento físico. Permite crear, destruir, verificar, exportar e importar conjuntos de discos físicos configurados en RAID.
* **`zfs`**: Comando para administrar datasets y volúmenes dentro de un pool ZFS. Permite crear sistemas de archivos, asignar cuotas, activar compresión, compartir por red, entre otros.

---

## 1. Instalación de ZFS en AlmaLinux

```bash
dnf install https://zfsonlinux.org/epel/zfs-release-2-3$(rpm --eval "%{dist}").noarch.rpm
dnf install epel-release
dnf install kernel-devel
dnf install zfs
modprobe zfs
```

---

## 2. Creación de Pools ZFS

### RAID 0 (Striped Pool)

```bash
zpool create mi_pool /dev/sdb /dev/sdc /dev/sdd
```

### RAID 1 (Mirror Pool)

```bash
zpool create mi_pool mirror /dev/sdb /dev/sdc
```

### RAID-Z1

```bash
zpool create mi_pool raidz /dev/sdb /dev/sdc /dev/sdd
```

### RAID-Z2

```bash
zpool create mi_pool raidz2 /dev/sdb /dev/sdc /dev/sdd /dev/sde
```

### RAID-Z3

```bash
zpool create mi_pool raidz3 /dev/sdb /dev/sdc /dev/sdd /dev/sde /dev/sdf /dev/sdg
```

### Crear dataset

```bash
zfs create mi_pool/mis_datos
```

### Asignar cuota

```bash
zfs set quota=10G mi_pool/mis_datos
```

---

## 3. Verificación y Administración de Pools

### Ver estado del pool

```bash
zpool status
zfs list
```

### Listar pools

```bash
zpool list
```

### Scrub (verificar integridad)

```bash
zpool scrub mi_pool
```

### Exportar e importar pools

```bash
zpool export mi_pool
zpool import mi_pool
```

### Reemplazar disco dañado

```bash
zpool replace mi_pool /dev/sdX /dev/sdY
```

### Eliminar un pool (con precaución)

```bash
zpool destroy mi_pool
```

---

## 4. Compartir Volúmenes ZFS por NFS (Servidor)

### Opción A: Compartir automáticamente con ZFS

```bash
zfs set sharenfs=on data
zfs set sharenfs=on softwares
zfs set sharenfs=on usuarios
```

### Opción B: Configuración manual con `/etc/exports`

```bash
echo "/data *(rw,sync,no_subtree_check)" >> /etc/exports
echo "/softwares *(rw,sync,no_subtree_check)" >> /etc/exports
echo "/usuarios *(rw,sync,no_subtree_check)" >> /etc/exports
systemctl restart nfs-server
```

---

## 5. Configuración del Cliente NFS

### Instalar cliente NFS

```bash
dnf install nfs-utils         # AlmaLinux / RHEL
apt install nfs-common        # Debian / Ubuntu
```

### Crear puntos de montaje

```bash
mkdir -p /mnt/data /softwares /home
```

### Montar volúmenes compartidos

```bash
mount -t nfs <IP-del-servidor>:/data /mnt/data
mount -t nfs <IP-del-servidor>:/softwares /softwares
mount -t nfs <IP-del-servidor>:/usuarios /home
```

### Verificar montajes

```bash
df -h | grep nfs
mount | grep nfs
```

### Montaje automático (opcional)

```bash
echo "<IP-del-servidor>:/data /mnt/data nfs defaults 0 0" >> /etc/fstab
echo "<IP-del-servidor>:/softwares /softwares nfs defaults 0 0" >> /etc/fstab
echo "<IP-del-servidor>:/usuarios /home nfs defaults 0 0" >> /etc/fstab
```

---

## 6. Utilidades y Mantenimiento

### Limpiar firmas anteriores de discos

```bash
wipefs -a /dev/sdX
```

### Crear archivo de prueba en dataset

```bash
echo "Hola ZFS" > /data/archivo.txt
```

### Ver exportaciones disponibles (cliente)

```bash
showmount -e <IP-del-servidor>
```

---

## 7. Tabla Comparativa: ZFS vs RAID Tradicional

| Tipo ZFS | Equivalente RAID     | Discos Mínimos | Capacidad Útil       | Tolerancia a Fallos |
| -------- | -------------------- | -------------- | -------------------- | ------------------- |
| Striped  | RAID 0               | 1              | 100%                 | 0 discos            |
| Mirror   | RAID 1               | 2              | 50% (o 1/N si N > 2) | N-1 discos          |
| RAID-Z1  | RAID 5               | 3              | N-1 discos           | 1 disco             |
| RAID-Z2  | RAID 6               | 4              | N-2 discos           | 2 discos            |
| RAID-Z3  | RAID 7 (no estándar) | 5              | N-3 discos           | 3 discos            |
