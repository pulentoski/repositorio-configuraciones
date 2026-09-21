# 📊 Zabbix 7.4 + MySQL - Guía de Instalación

**Ubuntu 24.04 LTS | MySQL 8.0 | Apache 2.4**

---

## 📋 Requisitos Previos

- Ubuntu 24.04 LTS
- Acceso root o sudo
- 2GB RAM mínimo
- 10GB disco disponible

---

## 🚀 Instalación Rápida

### 1️⃣ Instalar MySQL Server

```bash
sudo apt update
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 2️⃣ Crear Base de Datos Zabbix

```bash
sudo mysql
```

```sql
CREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER 'zabbix'@'localhost' IDENTIFIED BY 'TuPasswordAqui';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
QUIT;
```

### 3️⃣ Instalar Zabbix

```bash
sudo -s
wget https://repo.zabbix.com/zabbix/7.4/release/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_7.4+ubuntu24.04_all.deb
dpkg -i zabbix-release_latest_7.4+ubuntu24.04_all.deb
apt update
apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent -y
```

### 4️⃣ Importar Schema de Zabbix

```bash
zcat /usr/share/zabbix/sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix
```

Deshabilitar flag después de importar:

```bash
sudo mysql -e "SET GLOBAL log_bin_trust_function_creators = 0;"
```

### 5️⃣ Configurar DBPassword

```bash
sudo nano /etc/zabbix/zabbix_server.conf
```

Buscar y editar:

```ini
DBPassword=TuPasswordAqui
```

### 6️⃣ Iniciar Servicios

```bash
sudo systemctl restart zabbix-server zabbix-agent apache2
sudo systemctl enable zabbix-server zabbix-agent apache2
```

---

## 🌐 Acceso Web

**URL:** `http://IP_SERVIDOR/zabbix`

**Credenciales por defecto:**
- Usuario: `Admin`
- Contraseña: `zabbix`

---

## ✅ Verificación

```bash
# Estado de servicios
sudo systemctl status zabbix-server zabbix-agent apache2

# Conectar a MySQL como usuario zabbix
mysql -uzabbix -p -e "USE zabbix; SHOW TABLES;" | head -10

# Revisar logs
tail -f /var/log/zabbix/zabbix_server.log
```

---

## ⚠️ Troubleshooting

| Error | Solución |
|-------|----------|
| `Can't connect to MySQL socket` | `sudo systemctl start mysql` |
| `Access denied for user 'zabbix'` | Verificar contraseña en `/etc/zabbix/zabbix_server.conf` |
| `Apache2 no responde` | `sudo systemctl restart apache2` |

---

## 🔐 Seguridad (Post-Instalación)

1. Cambiar contraseña Admin en web UI
2. Desabilitar acceso remoto MySQL: editar `/etc/mysql/mysql.conf.d/mysqld.cnf` → `bind-address = 127.0.0.1`
3. Configurar firewall: `sudo ufw allow 80/tcp`

---

## 📚 Referencias

- [Documentación Oficial Zabbix 7.4](https://www.zabbix.com/documentation/7.4/en)
- [MySQL Database Creation](https://www.zabbix.com/documentation/7.4/en/manual/installation/databases)

---

**Última actualización:** Septiembre 2026
