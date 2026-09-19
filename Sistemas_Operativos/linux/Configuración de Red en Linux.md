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

## Rutas Estáticas 🛣️

### Netplan (persistente):
```yaml
network:
  version: 2
  ethernets:
    ens2:
      dhcp4: true
      routes:
        - to: 10.0.0.0/8
          via: 192.168.0.1
        - to: 172.16.0.0/12
          via: 192.168.0.1
```

### Temporal (no persiste tras reboot):
```bash
sudo ip route add 10.0.0.0/8 via 192.168.0.1
sudo ip route del 10.0.0.0/8 via 192.168.0.1
```

Ver rutas:
```bash
ip route
ip route show table all
```

---

## Troubleshooting Avanzado 🔧

| Comando | Qué muestra |
|---------|------------|
| `ethtool ens2` | Velocidad, duplex, estado de enlace |
| `ip link show ens2` | MTU, estado UP/DOWN, MAC address |
| `arp -a` | Tabla ARP (resolución IP→MAC) |
| `ss -tulpn` | Puertos escuchando (TCP/UDP) |
| `netstat -rn` | Tabla de rutas (legacy) |
| `traceroute 8.8.8.8` | Ruta de paquetes hacia destino |
| `dig google.com` | Consulta DNS detallada |
| `nslookup google.com` | Resolución DNS |
| `journalctl -u networking -n 20` | Últimos 20 logs de red |
| `dmesg \| grep -i network` | Logs del kernel sobre red |
| `cat /proc/net/arp` | Tabla ARP desde /proc |

---

## Múltiples IPs en Una Interfaz 🔢

### Netplan (Debian/Ubuntu):
```yaml
network:
  version: 2
  ethernets:
    ens2:
      dhcp4: false
      addresses:
        - 192.168.0.10/24
        - 192.168.0.11/24
        - 192.168.0.12/24
      gateway4: 192.168.0.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Aplicar:
```bash
sudo netplan apply
```

Verificar:
```bash
ip addr show ens2
```

---

## Bridging (Switches Virtuales) 🌉

Útil para labs con múltiples interfaces conectadas:

```yaml
network:
  version: 2
  ethernets:
    ens2:
      dhcp4: false
    ens3:
      dhcp4: false
  bridges:
    br0:
      interfaces: [ens2, ens3]
      dhcp4: true
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Verificar bridge:
```bash
ip link show br0
brctl show
```

---

## Script Generador de Configs Netplan 🤖

Crear `gen-netplan.sh`:

```bash
#!/bin/bash

# USO: ./gen-netplan.sh <hostname> <ip> <netmask> <gateway> <dns1> <dns2>
# EJEMPLO: ./gen-netplan.sh ubnt-1 192.168.0.10 24 192.168.0.1 8.8.8.8 8.8.4.4

HOSTNAME=$1
IP=$2
NETMASK=$3
GATEWAY=$4
DNS1=$5
DNS2=$6

if [ -z "$HOSTNAME" ]; then
    echo "USO: $0 <hostname> <ip> <netmask> <gateway> <dns1> <dns2>"
    exit 1
fi

cat > 01-netcfg.yaml << EOF
network:
  version: 2
  ethernets:
    ens2:
      dhcp4: false
      addresses:
        - ${IP}/${NETMASK}
      gateway4: ${GATEWAY}
      nameservers:
        addresses: [${DNS1}, ${DNS2}]
  hostname: ${HOSTNAME}
EOF

echo "✓ Config generada: 01-netcfg.yaml"
echo "  Aplicar con: sudo cp 01-netcfg.yaml /etc/netplan/ && sudo netplan apply"
```

Uso:
```bash
chmod +x gen-netplan.sh
./gen-netplan.sh ubnt-1 192.168.0.10 24 192.168.0.1 8.8.8.8 8.8.4.4
./gen-netplan.sh ubnt-2 192.168.0.11 24 192.168.0.1 8.8.8.8 8.8.4.4
```

---

## Comparativa: nmcli vs netplan 📊

| Aspecto | `nmcli` | `netplan` |
|--------|--------|----------|
| **Sistema** | RedHat, Ubuntu con NetworkManager | Debian, Ubuntu (moderno) |
| **Persistencia** | Automática en `/etc/NetworkManager/` | Manual: `/etc/netplan/` |
| **Sintaxis** | CLI o interactivo (`nmtui`) | YAML |
| **Complejidad** | Más intuitivo para usuarios | Más legible en código |
| **Mejor para** | Máquinas desktop/laptops | Servidores, infraestructura |
| **Aplicar cambios** | `nmcli connection reload` | `netplan apply` |

### nmcli (conexión DHCP):
```bash
sudo nmcli connection add type ethernet ifname ens2 con-name LAN autoconnect yes
sudo nmcli connection modify LAN ipv4.method auto
sudo nmcli connection up LAN
```

### nmcli (IP estática):
```bash
sudo nmcli connection add type ethernet ifname ens2 con-name LAN \
  ipv4.addresses 192.168.0.10/24 \
  ipv4.gateway 192.168.0.1 \
  ipv4.method manual \
  ipv4.dns "8.8.8.8 8.8.4.4"
sudo nmcli connection up LAN
```

Ver conexiones:
```bash
nmcli connection show
nmcli device status
```

---

