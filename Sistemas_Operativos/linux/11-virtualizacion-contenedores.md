# 11 — Virtualización y contenedores

> Gestionar VMs, contenedores y el hipervisor es el día a día en entornos modernos. Este módulo cubre Proxmox, Docker, LXC y los comandos esenciales de cada uno.

---

## Proxmox VE — Gestión desde CLI

### Información del cluster y nodos

```bash
pvesh get /nodes                        # Ver nodos del cluster
pvesh get /nodes/prox/status            # Estado del nodo
pvesh get /cluster/status               # Estado del cluster
pveversion                              # Versión de Proxmox
pveceph status                          # Estado de Ceph (si aplica)
```

### Gestión de VMs con `qm`

```bash
qm list                                 # Listar todas las VMs
qm status VMID                          # Estado de una VM
qm start VMID                           # Iniciar VM
qm stop VMID                            # Apagar VM (fuerza)
qm shutdown VMID                        # Apagado graceful
qm reset VMID                           # Reiniciar VM (fuerza)
qm reboot VMID                          # Reiniciar graceful
qm suspend VMID                         # Suspender VM
qm resume VMID                          # Reanudar VM

# Información de la VM
qm config VMID                          # Ver configuración completa
qm showcmd VMID                         # Ver comando QEMU que se ejecuta

# Consola
qm terminal VMID                        # Conectar a consola serial
qm vncproxy VMID                        # Iniciar proxy VNC

# Snapshots
qm snapshot VMID nombre_snap --description "Antes de actualización"
qm listsnapshot VMID                    # Listar snapshots
qm rollback VMID nombre_snap            # Revertir a snapshot
qm delsnapshot VMID nombre_snap         # Eliminar snapshot

# Migración
qm migrate VMID nodo_destino            # Migrar VM a otro nodo
qm migrate VMID nodo_destino --online   # Migración en vivo (live migration)

# Crear VM desde CLI
qm create 101 --name "ubuntu-server" --memory 2048 --cores 2 \
  --net0 virtio,bridge=vmbr0 \
  --scsi0 local-lvm:32 \
  --ide2 local:iso/ubuntu-22.04.iso,media=cdrom \
  --boot order=ide2
```

### Gestión de contenedores LXC con `pct`

```bash
pct list                                # Listar contenedores
pct status CTID                         # Estado de un contenedor
pct start CTID                          # Iniciar contenedor
pct stop CTID                           # Detener contenedor
pct restart CTID                        # Reiniciar contenedor
pct shutdown CTID                       # Apagado graceful

# Acceder al contenedor
pct enter CTID                          # Shell dentro del contenedor
pct exec CTID -- comando                # Ejecutar comando en el contenedor
pct exec CTID -- bash -c "apt update"

# Configuración
pct config CTID                         # Ver configuración
pct set CTID --memory 2048              # Cambiar RAM
pct set CTID --cores 4                  # Cambiar CPUs

# Snapshots
pct snapshot CTID nombre_snap
pct listsnapshot CTID
pct rollback CTID nombre_snap
pct delsnapshot CTID nombre_snap

# Crear contenedor desde CLI
pct create 200 local:vztmpl/debian-12-standard_12.0-1_amd64.tar.zst \
  --hostname mi-contenedor \
  --memory 1024 \
  --cores 2 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --unprivileged 1
```

### Storage en Proxmox

```bash
pvesm status                            # Estado de los storages
pvesm list local                        # Listar contenido de storage "local"
pvesm list local-lvm                    # Listar volúmenes LVM
pvesm alloc local-lvm VMID vm-VMID-disk-0 10G   # Crear volumen
pvesm free local-lvm:vm-VMID-disk-0    # Liberar volumen
```

### Red en Proxmox

```bash
cat /etc/network/interfaces             # Configuración de red del host
brctl show                              # Ver bridges configurados
ip link show                            # Interfaces del host
```

---

## Docker

```bash
# Información del sistema
docker info                             # Info general del daemon
docker version                          # Versión cliente y servidor
docker system df                        # Espacio usado por Docker
docker system prune                     # Limpiar recursos no utilizados
docker system prune -a                  # Limpiar todo (incluye imágenes)

# Imágenes
docker images                           # Listar imágenes locales
docker pull ubuntu:22.04                # Descargar imagen
docker rmi ubuntu:22.04                 # Eliminar imagen
docker build -t mi-app:1.0 .            # Construir imagen desde Dockerfile
docker history mi-app:1.0               # Ver capas de una imagen

# Contenedores
docker ps                               # Contenedores en ejecución
docker ps -a                            # Todos, incluyendo detenidos
docker run -d --name web -p 80:80 nginx # Ejecutar en background
docker run -it ubuntu bash              # Interactivo con shell
docker start/stop/restart nombre        # Gestión básica
docker rm nombre                        # Eliminar contenedor detenido
docker rm -f nombre                     # Eliminar incluso si está corriendo
docker logs nombre                      # Ver logs
docker logs -f nombre                   # Seguir logs en tiempo real
docker exec -it nombre bash             # Shell dentro del contenedor
docker inspect nombre                   # Info detallada en JSON
docker stats                            # Uso de recursos en tiempo real
docker top nombre                       # Procesos dentro del contenedor

# Volúmenes
docker volume ls
docker volume create mi_volumen
docker volume rm mi_volumen
docker run -v mi_volumen:/datos nginx   # Usar volumen nombrado
docker run -v /host/ruta:/contenedor/ruta nginx   # Bind mount

# Redes
docker network ls
docker network create mi_red
docker run --network mi_red nginx
```

### Docker Compose

```bash
docker compose up -d                    # Levantar servicios en background
docker compose down                     # Detener y eliminar contenedores
docker compose down -v                  # También eliminar volúmenes
docker compose ps                       # Estado de los servicios
docker compose logs -f                  # Seguir logs de todos los servicios
docker compose logs -f servicio         # Logs de servicio específico
docker compose restart servicio         # Reiniciar un servicio
docker compose exec servicio bash       # Shell en un servicio
docker compose pull                     # Actualizar imágenes
docker compose build                    # Reconstruir imágenes
```

---

## LXC nativo (sin Proxmox)

```bash
# Instalar
apt install lxc

# Gestión básica
lxc-ls                                  # Listar contenedores
lxc-ls --fancy                          # Con estado y IP
lxc-info -n nombre                      # Info de un contenedor
lxc-start -n nombre                     # Iniciar
lxc-stop -n nombre                      # Detener
lxc-destroy -n nombre                   # Eliminar
lxc-attach -n nombre                    # Acceder al contenedor
lxc-execute -n nombre -- comando        # Ejecutar comando

# Crear contenedor
lxc-create -t download -n mi-contenedor -- -d ubuntu -r jammy -a amd64
```

---

## virsh — KVM/QEMU nativo

```bash
virsh list                              # VMs activas
virsh list --all                        # Todas
virsh start nombre                      # Iniciar
virsh shutdown nombre                   # Apagado graceful
virsh destroy nombre                    # Fuerza bruta
virsh reboot nombre                     # Reiniciar
virsh dominfo nombre                    # Info de la VM
virsh console nombre                    # Conectar a consola
virsh snapshot-create-as nombre snap1   # Crear snapshot
virsh snapshot-list nombre              # Listar snapshots
virsh snapshot-revert nombre snap1      # Revertir
```

---

## Casos de uso reales en Proxmox

**Ver el estado de todas las VMs y contenedores de un vistazo:**
```bash
qm list && pct list
```

**Hacer snapshot de todas las VMs antes de un cambio:**
```bash
FECHA=$(date +%Y-%m-%d)
for VMID in $(qm list | awk 'NR>1 {print $1}'); do
    qm snapshot $VMID "pre-cambio-$FECHA" --description "Antes de actualización"
    echo "Snapshot de VM $VMID creado"
done
```

**Verificar uso de recursos del nodo Proxmox:**
```bash
pvesh get /nodes/prox/status | grep -E 'cpu|mem'
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| VM no arranca | `qm start VMID && journalctl -u qemu\* -n 50` |
| Contenedor LXC no tiene red | `pct config CTID` — verificar net0 |
| Docker: puerto ya en uso | `ss -tulnp \| grep :PUERTO` |
| Proxmox: storage lleno | `pvesm status` y `df -h` |
| VM migración falla | Verificar que el storage sea compartido entre nodos |
