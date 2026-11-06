# 📊 Zabbix 8.0 LTS + PostgreSQL - Guía de Instalación

**Debian 13 Trixie | PostgreSQL 17 | Apache 2.4**

---

## 📋 Requisitos Previos

- Debian 13 Trixie (amd64 / arm64)
- Acceso root o sudo
- 2GB RAM mínimo
- 10GB disco disponible

> En instalaciones mínimas de Debian puede faltar `wget` o `sudo`: `apt install wget sudo -y`

---

## 🚀 Instalación Rápida

### 1️⃣ Instalar PostgreSQL

```bash
sudo apt update
sudo apt install postgresql -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2️⃣ Instalar Repositorio Zabbix

```bash
sudo -s
wget https://repo.zabbix.com/zabbix/8.0/release/debian/pool/main/z/zabbix-release/zabbix-release_latest_8.0+debian13_all.deb
dpkg -i zabbix-release_latest_8.0+debian13_all.deb
apt update
```

### 3️⃣ Instalar Zabbix Server, Frontend y Agent

```bash
apt install zabbix-server-pgsql zabbix-frontend-php php8.4-pgsql zabbix-apache-conf zabbix-sql-scripts zabbix-agent -y
```

### 4️⃣ Crear Base de Datos Zabbix

```bash
sudo -u postgres createuser --pwprompt zabbix
sudo -u postgres createdb -O zabbix zabbix
```

### 5️⃣ Importar Schema de Zabbix

```bash
zcat /usr/share/zabbix/sql-scripts/postgresql/server.sql.gz | sudo -u zabbix psql zabbix
```

### 6️⃣ Configurar DBPassword

```bash
sudo nano /etc/zabbix/zabbix_server.conf
```

Buscar y editar:

```ini
DBPassword=TuPasswordAqui
```

### 7️⃣ Iniciar Servicios

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
sudo systemctl status zabbix-server zabbix-agent apache2 postgresql

# Listar tablas de la BD zabbix
sudo -u zabbix psql zabbix -c "\dt" | head -15

# Revisar logs
tail -f /var/log/zabbix/zabbix_server.log
```

---

## ⚠️ Troubleshooting

| Error | Solución |
|-------|----------|
| `could not connect to server` | `sudo systemctl start postgresql` |
| `password authentication failed for user "zabbix"` | Verificar contraseña en `/etc/zabbix/zabbix_server.conf` |
| `role "zabbix" does not exist` | Repetir paso 4 (`createuser`) |
| `Apache2 no responde` | `sudo systemctl restart apache2` |
| Frontend sin soporte PostgreSQL | Verificar `php8.4-pgsql` instalado y reiniciar Apache |

---

## 🔐 Seguridad (Post-Instalación)

1. Cambiar contraseña Admin en web UI
2. Restringir PostgreSQL a local: editar `/etc/postgresql/17/main/postgresql.conf` → `listen_addresses = 'localhost'`
3. Configurar firewall (Debian no trae `ufw` por defecto):
   ```bash
   sudo apt install ufw -y
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw enable
   ```

---

## 📚 Referencias

- [Documentación Oficial Zabbix 8.0](https://www.zabbix.com/documentation/8.0/en)
- [Database Creation](https://www.zabbix.com/documentation/8.0/en/manual/installation/databases)
- [Release Notes 8.0](https://www.zabbix.com/rn/rn8.0.0)

---

**Última actualización:** Noviembre 2026
