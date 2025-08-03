# 🌐 Guía de Administración ZFS y RAID en Linux (AlmaLinux)

## 📘 Introducción

**ZFS (Zettabyte File System)** es un sistema de archivos avanzado que combina la gestión de volúmenes y archivos en una única solución. Fue diseñado para:

- 💾 Alta **integridad de datos**
- 🛡️ **Tolerancia a fallos**
- 📈 **Escalabilidad masiva**
- 🔧 Administración simple y eficiente

ZFS permite crear configuraciones tipo RAID llamadas **RAID-Z**, además de soportar funcionalidades como compresión, snapshots, cuotas, y más.

---

## 🔍 Diferencias entre `zpool` y `zfs`

| 🛠️ Comando | 📌 Función                                                                 |
|------------|----------------------------------------------------------------------------|
| `zpool`    | Administra pools de almacenamiento físico (RAID-Z, Mirror, etc.)          |
| `zfs`      | Administra datasets, cuotas, compresión, snapshots, y compartición de datos |

---

## 🚀 1. Instalación de ZFS en AlmaLinux

```bash
dnf install https://zfsonlinux.org/epel/zfs-release-2-3$(rpm --eval "%{dist}").noarch.rpm
dnf install epel-release
dnf install kernel-devel
dnf install zfs
modprobe zfs
```

---

## 🧼 2. Preparar Discos (opcional)

```bash
wipefs -a /dev/sdX
```
> 🔁 Limpia firmas anteriores para evitar conflictos al crear el pool.

---

## 🧱 3. Crear un Pool ZFS

### ⚡ RAID 0 (Striped)

```bash
zpool create mi_pool /dev/sdb /dev/sdc /dev/sdd
```

### 🪞 RAID 1 (Mirror)

```bash
zpool create mi_pool mirror /dev/sdb /dev/sdc
```

### 🧩 RAID-Z1

```bash
zpool create mi_pool raidz /dev/sdb /dev/sdc /dev/sdd
```

### 🛡️ RAID-Z2

```bash
zpool create mi_pool raidz2 /dev/sdb /dev/sdc /dev/sdd /dev/sde
```

### 🛡️ RAID-Z3

```bash
zpool create mi_pool raidz3 /dev/sdb /dev/sdc /dev/sdd /dev/sde /dev/sdf /dev/sdg
```

---

## 📂 4. Crear y Configurar un Dataset

```bash
zfs create mi_pool/mis_datos
zfs set quota=10G mi_pool/mis_datos
```
> 📁 Un dataset permite aplicar cuotas, compresión, snapshots, etc.

---

## 🔧 5. Administración del Pool

```bash
zpool list
zpool status
zfs list
zpool scrub mi_pool
zpool export mi_pool
zpool import mi_pool
zpool replace mi_pool /dev/sdX /dev/sdY
zpool destroy mi_pool  # ⚠️ Usar con precaución
```

---

## 🌐 6. Compartir Dataset por NFS (Servidor)

### ✅ A. Compartir directamente con ZFS

```bash
zfs set sharenfs=on mi_pool/mis_datos
```

### 📝 B. Configuración manual

1. Instalar NFS:

```bash
dnf install nfs-utils
```

2. Editar `/etc/exports`:

```bash
echo "/mi_pool/mis_datos *(rw,sync,no_root_squash)" >> /etc/exports
```

3. Activar servicio NFS:

```bash
exportfs -rav
systemctl enable --now nfs-server
```

4. 🔥 Configurar firewall:

```bash
firewall-cmd --permanent --add-service=nfs
firewall-cmd --permanent --add-service=mountd
firewall-cmd --permanent --add-service=rpc-bind
firewall-cmd --reload
```

---

## 💻 7. Configurar Cliente NFS

### 🧰 Instalar cliente NFS

```bash
dnf install nfs-utils       # AlmaLinux
apt install nfs-common      # Debian/Ubuntu
```

### 📁 Crear punto de montaje

```bash
mkdir -p /mnt/mis_datos
```

### 🔗 Montar el recurso compartido

```bash
mount -t nfs <IP-del-servidor>:/mi_pool/mis_datos /mnt/mis_datos
```

### 🔍 Verificar montajes

```bash
df -h | grep nfs
mount | grep nfs
```

### 🔒 Montaje persistente (opcional)

```bash
echo "<IP-del-servidor>:/mi_pool/mis_datos /mnt/mis_datos nfs defaults 0 0" >> /etc/fstab
```

---

## 🧪 8. Pruebas

### 📄 Crear archivo de prueba

```bash
echo "Hola ZFS" > /mnt/mis_datos/archivo.txt
```

### 📡 Ver exportaciones NFS disponibles

```bash
showmount -e <IP-del-servidor>
```

---

## 📊 9. Tabla Comparativa: ZFS vs RAID Tradicional

| ⚙️ Tipo ZFS | 🛠️ Equivalente RAID     | 🔢 Discos Mínimos | 📦 Capacidad Útil       | 🔁 Tolerancia a Fallos |
|------------|--------------------------|-------------------|-------------------------|-------------------------|
| Striped    | RAID 0                   | 1                 | 100%                    | 0 discos                |
| Mirror     | RAID 1                   | 2                 | 50% (o 1/N si N > 2)    | N-1 discos              |
| RAID-Z1    | RAID 5                   | 3                 | N-1 discos              | 1 disco                 |
| RAID-Z2    | RAID 6                   | 4                 | N-2 discos              | 2 discos                |
| RAID-Z3    | RAID 7 (no oficial)      | 5                 | N-3 discos              | 3 discos                |

---


---
