# 02 — Red y conectividad

> La red es la columna vertebral de cualquier servidor. Estos comandos te permiten ver, diagnosticar y configurar todo lo relacionado con conectividad.

---

## Ver interfaces y direcciones IP

```bash
ip addr show                # Todas las interfaces con IPs
ip addr show eth0           # Interfaz específica
ip -br addr                 # Formato compacto y legible
ifconfig                    # Alternativa clásica (puede requerir net-tools)
```

---

## Rutas

```bash
ip route show               # Tabla de rutas activa
ip route get 8.8.8.8        # Qué interfaz usa para llegar a esa IP
route -n                    # Alternativa clásica
```

---

## Conexiones activas y puertos

```bash
ss -tuln                    # Puertos escuchando (TCP/UDP), sin resolver nombres
ss -tulnp                   # Igual + proceso que abrió el puerto
ss -s                       # Resumen de conexiones
netstat -tulnp              # Alternativa clásica (requiere net-tools)
lsof -i :8006               # Qué proceso usa el puerto 8006
lsof -i tcp                 # Todas las conexiones TCP abiertas
```

---

## Diagnóstico de conectividad

```bash
ping 8.8.8.8                # Prueba conectividad básica
ping -c 4 google.com        # Solo 4 paquetes
traceroute google.com       # Ruta por saltos hasta el destino
tracepath google.com        # Similar, sin root
mtr google.com              # Traceroute dinámico en tiempo real (instalar: apt install mtr)
```

---

## DNS

```bash
dig google.com              # Consulta DNS completa
dig google.com +short       # Solo la IP
dig @8.8.8.8 google.com     # Consultar contra DNS específico
nslookup google.com         # Alternativa clásica
host google.com             # Resolución rápida
cat /etc/resolv.conf        # DNS configurados en el sistema
resolvectl status           # Estado del resolver (systemd)
```

---

## Firewall

```bash
# UFW (Ubuntu/Debian)
ufw status verbose          # Estado del firewall
ufw allow 22/tcp            # Permitir SSH
ufw deny 8080               # Bloquear puerto
ufw enable / ufw disable    # Activar / desactivar

# iptables (bajo nivel)
iptables -L -n -v           # Ver todas las reglas
iptables -L INPUT -n        # Solo cadena INPUT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT   # Permitir HTTP

# firewalld (CentOS/RHEL/Proxmox)
firewall-cmd --list-all     # Ver configuración activa
firewall-cmd --add-port=8006/tcp --permanent    # Abrir puerto
firewall-cmd --reload       # Aplicar cambios
```

---

## Transferencia de archivos por red

```bash
scp archivo.txt user@10.0.0.2:/ruta/     # Copiar archivo a servidor remoto
scp -r carpeta/ user@10.0.0.2:/ruta/     # Copiar carpeta completa
rsync -avz origen/ user@host:/destino/   # Sincronización eficiente
wget https://ejemplo.com/archivo.tar.gz  # Descargar archivo
curl -O https://ejemplo.com/archivo.tar.gz   # Alternativa a wget
curl -I https://ejemplo.com             # Solo headers HTTP
```

---

## Escaneo de red

```bash
nmap -sn 10.0.0.0/24        # Descubrir hosts activos en la red (ping scan)
nmap -p 22,80,443 10.0.0.2  # Escanear puertos específicos
nmap -sV 10.0.0.2           # Detectar versiones de servicios
arp -n                      # Tabla ARP local (IP → MAC)
ip neigh                    # Alternativa moderna a arp
```

---

## Configuración de red (temporal vs permanente)

```bash
# Temporal (se pierde al reiniciar)
ip addr add 192.168.1.100/24 dev eth0
ip link set eth0 up
ip route add default via 192.168.1.1

# Permanente con Netplan (Ubuntu)
# Editar /etc/netplan/00-installer-config.yaml
netplan apply               # Aplicar cambios

# Permanente con nmcli (NetworkManager)
nmcli con show              # Ver conexiones
nmcli con mod "Wired" ipv4.addresses 10.0.0.10/24
nmcli con up "Wired"
```

---

## Casos de uso reales

**Ver qué proceso está usando un puerto antes de lanzar un servicio:**
```bash
ss -tulnp | grep :80
```

**Diagnosticar por qué no hay internet:**
```bash
ping 8.8.8.8        # Si falla: problema de red física o ruta
ping google.com     # Si falla pero 8.8.8.8 funciona: problema DNS
```

**Ver todas las IPs activas en tu segmento:**
```bash
nmap -sn 10.0.0.0/24 | grep report
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| No sé qué IP tiene el servidor | `ip -br addr` |
| Puerto ocupado | `ss -tulnp \| grep :PUERTO` |
| DNS no resuelve | `dig @8.8.8.8 dominio.com` |
| No hay ruta al destino | `ip route get IP_DESTINO` |
| Conexión lenta / pérdida de paquetes | `mtr destino` |
| Quiero ver tráfico en tiempo real | `tcpdump -i eth0 -n` |
