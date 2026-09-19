# Configuración de Red en Linux 🌐

## Ver IPs — Comandos Generales 📋

| Comando | Función |
|---------|---------|
| `ip addr` o `ip a` | Listar todas las interfaces y IPs (moderno) |
| `ifconfig` | Listar interfaces y IPs (legacy, a veces no instalado) |
| `hostname -I` | Mostrar solo IPs asignadas |
| `ip route` | Ver rutas y gateway |
| `ip link` | Ver estado de interfaces (up/down) |
| `cat /etc/resolv.conf` | Ver servidores DNS configurados |

---

## Por Tipo de Sistema 🖥️

### **Debian/Ubuntu (netplan)**
```bash
sudo nano /etc/netplan/01-netcfg.yaml
```

**DHCP dinámico:**
```yaml
network:
  version: 2
  ethernets:
    ens2:
      dhcp4: true
```

**IP estática:**
```yaml
network:
  version: 2
  ethernets:
    ens2:
      dhcp4: false
      addresses:
        - 192.168.0.10/24
      gateway4: 192.168.0.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Aplicar cambios:
```bash
sudo netplan apply
```

---

### **RedHat/CentOS/Fedora (nmtui o ficheros)**
```bash
sudo nmtui  # Interfaz gráfica en terminal (recomendado)
```

O editar directamente:
```bash
sudo nano /etc/sysconfig/network-scripts/ifcfg-eth0
```

DHCP:
```
BOOTPROTO=dhcp
ONBOOT=yes
```

Estática:
```
BOOTPROTO=static
IPADDR=192.168.0.10
NETMASK=255.255.255.0
GATEWAY=192.168.0.1
DNS1=8.8.8.8
ONBOOT=yes
```

Reiniciar red:
```bash
sudo systemctl restart network
```

---

### **Alpine Linux**
```bash
sudo vi /etc/network/interfaces
```

DHCP:
```
auto eth0
iface eth0 inet dhcp
```

Estática:
```
auto eth0
iface eth0 inet static
    address 192.168.0.10
    netmask 255.255.255.0
    gateway 192.168.0.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

Reiniciar:
```bash
sudo service networking restart
```

---

### **TinyCore Linux**
```bash
ifconfig  # Ver IPs (ip no está instalado)
```

Configurar DHCP en `/opt/bootlocal.sh` o editar `/etc/hostname`.

---

## Acciones Comunes ⚡

| Acción | Comando |
|--------|---------|
| Reiniciar interfaz específica | `sudo ip link set ens2 down && sudo ip link set ens2 up` |
| Solicitar DHCP manual | `sudo dhclient ens2` (Debian/Ubuntu) |
| Liberar lease DHCP | `sudo dhclient -r ens2` |
| Asignar IP temporal (sin persistencia) | `sudo ip addr add 192.168.0.10/24 dev ens2` |
| Eliminar IP temporal | `sudo ip addr del 192.168.0.10/24 dev ens2` |
| Ver histórico DNS | `cat /etc/resolv.conf` |
| Probar conectividad | `ping 8.8.8.8` |
| Verificar sintaxis netplan | `sudo netplan validate` |

---

## Checklist Diagnóstico 🔍

- ✓ `ip a` → ¿Interfaz tiene IP?
- ✓ `ip route` → ¿Hay gateway?
- ✓ `cat /etc/resolv.conf` → ¿DNS configurado?
- ✓ `ping 8.8.8.8` → ¿Conecta internet?
- ✓ `sudo netplan apply` o equiv. → ¿Configuración persistente?

---

**Última revisión:** 2025 | CML Labs 🔧
