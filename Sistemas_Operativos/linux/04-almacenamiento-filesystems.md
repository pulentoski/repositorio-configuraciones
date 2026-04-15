# 04 — Almacenamiento y filesystems

> El disco es donde vive todo. Saber gestionarlo — ver el espacio, crear particiones, montar filesystems y diagnosticar errores — es una habilidad crítica para cualquier sysadmin.

---

## Ver espacio en disco

```bash
df -h                       # Uso de disco por filesystem, formato legible
df -hT                      # Incluye tipo de filesystem
df -i                       # Inodos usados (puede llenarse independiente del espacio)
du -sh /ruta                # Tamaño de un directorio
du -sh /*                   # Tamaño de cada directorio en raíz
du -sh /var/* | sort -h     # Ordenado por tamaño
du -ah /ruta | sort -rh | head -20  # Top 20 archivos/dirs más grandes
```

---

## Ver discos y particiones

```bash
lsblk                       # Árbol de discos, particiones y puntos de montaje
lsblk -f                    # Incluye filesystem, UUID y etiqueta
fdisk -l                    # Lista detallada de particiones (requiere root)
parted -l                   # Alternativa moderna a fdisk
blkid                       # UUID y tipo de filesystem de cada dispositivo
```

---

## Particionado

```bash
# Con fdisk (MBR y GPT básico)
fdisk /dev/sdb              # Iniciar particionado interactivo
# Dentro de fdisk: n=nueva, d=borrar, p=imprimir, w=escribir, q=salir

# Con parted (recomendado para GPT y discos >2TB)
parted /dev/sdb
  mklabel gpt               # Crear tabla GPT
  mkpart primary ext4 0% 100%   # Partición usando todo el disco
  print                     # Ver particiones
  quit

# Con gdisk (GPT nativo)
gdisk /dev/sdb
```

---

## Crear filesystems

```bash
mkfs.ext4 /dev/sdb1         # Formatear como ext4
mkfs.xfs /dev/sdb1          # Formatear como XFS
mkfs.btrfs /dev/sdb1        # Formatear como Btrfs
mkswap /dev/sdb2            # Crear área de swap
```

---

## Montar y desmontar

```bash
mount /dev/sdb1 /mnt/datos  # Montar partición
mount -t ext4 /dev/sdb1 /mnt/datos   # Especificando tipo
umount /mnt/datos           # Desmontar
umount -l /mnt/datos        # Desmontaje lazy (si está ocupado)
mount | column -t           # Ver todo lo montado actualmente
```

### Montaje permanente con /etc/fstab

```bash
# Formato: dispositivo  punto_montaje  tipo  opciones  dump  pass
UUID=xxxx-xxxx  /mnt/datos  ext4  defaults  0  2

# Obtener UUID:
blkid /dev/sdb1

# Probar fstab sin reiniciar:
mount -a
```

---

## Swap

```bash
swapon --show               # Ver swap activa
free -h                     # RAM y swap
swapon /dev/sdb2            # Activar swap
swapoff /dev/sdb2           # Desactivar swap

# Crear swap file (alternativa a partición)
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab   # Permanente
```

---

## LVM — Logical Volume Manager

```bash
# Ver estado
pvs                         # Physical Volumes
vgs                         # Volume Groups
lvs                         # Logical Volumes
pvdisplay / vgdisplay / lvdisplay   # Detalles completos

# Crear LVM desde cero
pvcreate /dev/sdb           # Inicializar disco como PV
vgcreate datos_vg /dev/sdb  # Crear Volume Group
lvcreate -L 50G -n datos_lv datos_vg   # Crear Logical Volume de 50GB
mkfs.ext4 /dev/datos_vg/datos_lv       # Formatear
mount /dev/datos_vg/datos_lv /mnt/datos

# Extender un LV
lvextend -L +20G /dev/datos_vg/datos_lv
resize2fs /dev/datos_vg/datos_lv       # Extender filesystem ext4
xfs_growfs /mnt/datos                  # Extender filesystem XFS
```

---

## Salud del disco con SMART

```bash
smartctl -a /dev/sda        # Reporte completo SMART
smartctl -H /dev/sda        # Solo resultado de salud: PASSED o FAILED
smartctl -t short /dev/sda  # Iniciar test corto
smartctl -t long /dev/sda   # Iniciar test largo (horas)
```

> Instalar: `apt install smartmontools`

---

## Verificar y reparar filesystems

```bash
# Solo en filesystems DESMONTADOS
fsck /dev/sdb1              # Verificar y reparar
fsck -y /dev/sdb1           # Reparar automáticamente sin preguntar
e2fsck -f /dev/sdb1         # Verificación forzada ext2/3/4
xfs_repair /dev/sdb1        # Reparar XFS
```

---

## Operaciones con archivos grandes / disco

```bash
dd if=/dev/zero of=/dev/sdb bs=4M      # Limpiar disco (cuidado: DESTRUCTIVO)
dd if=/dev/sda of=/backup.img bs=4M    # Clonar disco a imagen
dd if=/dev/zero of=test.img bs=1M count=1000 oflag=direct   # Test de escritura
```

---

## Casos de uso reales

**Disco lleno, encontrar el culpable:**
```bash
du -sh /* 2>/dev/null | sort -rh | head -10
du -sh /var/log/* | sort -rh | head -10
```

**Agregar disco nuevo a un servidor:**
```bash
lsblk                       # Identificar el disco nuevo (ej: /dev/sdb)
parted /dev/sdb mklabel gpt
parted /dev/sdb mkpart primary ext4 0% 100%
mkfs.ext4 /dev/sdb1
mkdir /mnt/nuevo_disco
mount /dev/sdb1 /mnt/nuevo_disco
blkid /dev/sdb1             # Obtener UUID para fstab
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| Disco lleno pero `df` no muestra nada | `df -i` (inodos llenos) |
| Filesystem montado read-only | `dmesg \| grep -i "error\|remount"` |
| No puedo desmontar (ocupado) | `lsof \| grep /mnt/punto` |
| Disco con errores | `smartctl -H /dev/sda` |
| Partición no aparece en fstab al boot | `blkid` y verificar UUID en fstab |
