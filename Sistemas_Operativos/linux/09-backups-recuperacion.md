# 09 — Backups y recuperación

> Un backup que no has probado restaurar no es un backup. Estas herramientas y estrategias cubren desde copias simples hasta sistemas de backup automatizado con deduplicación.

---

## rsync — Sincronización eficiente

```bash
# Sincronizar directorio local
rsync -av /origen/ /destino/                # -a: permisos, -v: verbose
rsync -avz /origen/ usuario@servidor:/destino/   # Con compresión, a servidor remoto
rsync -avz --delete /origen/ /destino/     # Eliminar en destino lo que no existe en origen
rsync -avzn /origen/ /destino/             # Dry run: muestra qué haría sin ejecutar
rsync -avz --exclude='*.log' /origen/ /destino/   # Excluir archivos
rsync -avz --exclude-from='/etc/rsync-exclude.txt' /origen/ /destino/

# Opciones útiles
# -a  = archive (preserva permisos, dueño, fechas, symlinks, etc.)
# -v  = verbose
# -z  = compresión durante transferencia
# -n  = dry run
# -P  = progreso + permite resumir transferencias interrumpidas
# --delete = elimina en destino lo que no existe en origen (mirror)
# --bwlimit=1000 = limitar a 1MB/s

# Backup remoto con ssh
rsync -avz -e "ssh -p 2222" /datos/ usuario@10.0.0.5:/backups/servidor1/
```

---

## tar — Archivos comprimidos

```bash
# Crear
tar -czvf backup.tar.gz /directorio/        # Crear archivo comprimido (gzip)
tar -cjvf backup.tar.bz2 /directorio/       # Comprimir con bzip2 (mejor ratio)
tar -cJvf backup.tar.xz /directorio/        # Comprimir con xz (mejor ratio aún)

# Extraer
tar -xzvf backup.tar.gz                     # Extraer en directorio actual
tar -xzvf backup.tar.gz -C /destino/        # Extraer en directorio específico

# Ver contenido sin extraer
tar -tzvf backup.tar.gz

# Backup con fecha en el nombre
tar -czvf backup_$(date +%Y-%m-%d).tar.gz /directorio/

# Excluir directorios
tar -czvf backup.tar.gz --exclude='/var/cache' --exclude='*.log' /var/
```

---

## dd — Clonación de discos e imágenes

```bash
# Clonar disco completo (DESTRUCTIVO en destino)
dd if=/dev/sda of=/dev/sdb bs=4M status=progress

# Crear imagen de disco
dd if=/dev/sda of=/backup/disco.img bs=4M status=progress

# Restaurar imagen
dd if=/backup/disco.img of=/dev/sda bs=4M status=progress

# Clonar partición
dd if=/dev/sda1 of=/backup/particion.img bs=4M status=progress

# Comprimir imagen al vuelo
dd if=/dev/sda bs=4M | gzip > /backup/disco.img.gz

# Restaurar imagen comprimida
gunzip -c /backup/disco.img.gz | dd of=/dev/sda bs=4M status=progress
```

> **Precaución:** `dd` no pregunta nada. Un `of=` equivocado puede destruir el disco erróneo. Verificar dos veces antes de ejecutar.

---

## Borgbackup — Backups deduplicados y cifrados

```bash
# Instalar
apt install borgbackup

# Inicializar repositorio
borg init --encryption=repokey /backups/mi_repo

# Crear backup
borg create /backups/mi_repo::backup-{now:%Y-%m-%d} /home /etc /var/www

# Crear backup con estadísticas
borg create --stats --progress /backups/mi_repo::backup-{now:%Y-%m-%d_%H:%M} /datos/

# Ver backups en el repositorio
borg list /backups/mi_repo

# Ver contenido de un backup
borg list /backups/mi_repo::nombre-del-backup

# Restaurar
borg extract /backups/mi_repo::nombre-del-backup               # En directorio actual
borg extract /backups/mi_repo::nombre-del-backup home/usuario/archivo.txt   # Archivo específico

# Eliminar backup antiguo
borg delete /backups/mi_repo::nombre-del-backup

# Limpiar backups viejos automáticamente
borg prune --keep-daily 7 --keep-weekly 4 --keep-monthly 12 /backups/mi_repo

# Verificar integridad
borg check /backups/mi_repo

# Montar backup para explorar
borg mount /backups/mi_repo::nombre /mnt/restore
ls /mnt/restore
borg umount /mnt/restore
```

---

## Restic — Alternativa moderna a Borg

```bash
# Instalar
apt install restic

# Inicializar repositorio
restic init --repo /backups/restic_repo

# Crear backup
restic -r /backups/restic_repo backup /home /etc

# Listar snapshots
restic -r /backups/restic_repo snapshots

# Restaurar
restic -r /backups/restic_repo restore latest --target /

# Eliminar snapshots viejos
restic -r /backups/restic_repo forget --keep-last 7 --prune

# Verificar integridad
restic -r /backups/restic_repo check
```

---

## Snapshots LVM

```bash
# Crear snapshot (requiere espacio libre en el VG)
lvcreate -L 10G -s -n snap_datos /dev/vg_datos/lv_datos

# Montar snapshot para explorar/restaurar
mount /dev/vg_datos/snap_datos /mnt/snap
ls /mnt/snap

# Restaurar desde snapshot (revertir el LV al estado del snapshot)
umount /mnt/snap
lvconvert --merge /dev/vg_datos/snap_datos   # El LV original se revierte

# Ver snapshots
lvs -a
```

---

## Script de backup básico

```bash
#!/bin/bash
# /scripts/backup_diario.sh

FECHA=$(date +%Y-%m-%d)
ORIGEN="/var/www /etc /home"
DESTINO="/backups"
LOG="/var/log/backup.log"

echo "=== Backup iniciado: $(date) ===" >> $LOG

for DIR in $ORIGEN; do
    NOMBRE=$(echo $DIR | tr '/' '_')
    tar -czvf "$DESTINO/backup${NOMBRE}_${FECHA}.tar.gz" "$DIR" >> $LOG 2>&1
    echo "Backup de $DIR: $?" >> $LOG
done

# Eliminar backups de más de 30 días
find $DESTINO -name "*.tar.gz" -mtime +30 -delete >> $LOG 2>&1

echo "=== Backup finalizado: $(date) ===" >> $LOG
```

```bash
chmod +x /scripts/backup_diario.sh
# Agregar a cron (2 AM diario)
echo "0 2 * * * root /scripts/backup_diario.sh" >> /etc/crontab
```

---

## Verificar y restaurar backups

> **Regla de oro:** Un backup no verificado no vale nada. Restaurar periódicamente en un entorno de prueba.

```bash
# Verificar integridad de un tar.gz
tar -tzvf backup.tar.gz > /dev/null && echo "OK" || echo "CORRUPTO"

# Restaurar archivo específico de un tar
tar -xzvf backup.tar.gz -C /tmp/ etc/nginx/nginx.conf

# Comparar backup con origen
diff <(tar -tzf backup.tar.gz | sort) <(find /etc | sed 's|^/||' | sort)
```

---

## Regla 3-2-1 de backups

| Principio | Descripción |
|---|---|
| **3** copias | Original + 2 backups |
| **2** medios distintos | Disco local + NAS o nube |
| **1** offsite | Una copia fuera del sitio físico |

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| rsync falla por permisos | Agregar `--rsync-path="sudo rsync"` |
| Backup tar.gz corrupto | `gzip -t backup.tar.gz` para verificar |
| Borg: repositorio bloqueado | `borg break-lock /backups/mi_repo` |
| Poco espacio para snapshot LVM | `vgs` para ver espacio libre en el VG |
| Necesito restaurar un solo archivo | `borg extract` o `tar -xzvf` con path específico |
