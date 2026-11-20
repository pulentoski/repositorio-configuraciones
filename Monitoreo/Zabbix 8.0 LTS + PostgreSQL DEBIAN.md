# 📊 Zabbix 8.0 LTS + PostgreSQL - Guía de Instalación

**Debian 13 Trixie | PostgreSQL 17 | Apache 2.4**

Instalación de Zabbix Server, Frontend y Agent utilizando PostgreSQL y Apache. Esta guía está preparada para ejecutar los comandos desde una sesión administrativa `root`, por lo que no es necesario utilizar `sudo`.

---

## 📋 Requisitos Previos

- Debian 13 Trixie (`amd64` / `arm64`).
- Acceso a la cuenta `root`.
- 2 GB de RAM mínimo (recomendado dimensionar según la cantidad de equipos y métricas).
- 10 GB de disco disponible como punto de partida.
- Conexión a Internet.

> En instalaciones mínimas de Debian pueden faltar herramientas como `wget` o `nano`. Se instalarán durante la preparación del sistema.

### 🔑 Acceder como superusuario (`root`)

Si estás conectado con un usuario normal (por ejemplo, `inacap`), cambia a `root`:

```bash
su -
```

Ingresa la contraseña de `root` (no la contraseña del usuario `inacap`).

Verifica que estás trabajando como superusuario:

```bash
whoami
```

El resultado debe ser:

```text
root
```

> **Importante:** ejecuta los comandos de esta guía desde esta sesión. No antepongas `sudo`. Para salir de la sesión administrativa, utiliza `exit`.

---

## 🚀 Instalación Rápida

### 1️⃣ Preparar Debian e instalar PostgreSQL

```bash
apt update
apt full-upgrade -y
apt install -y wget ca-certificates nano postgresql postgresql-client

systemctl enable --now postgresql
```

**Verificación:**

```bash
systemctl is-active postgresql
psql --version
pg_lsclusters
```

El servicio debe indicar `active`. En Debian 13 se espera PostgreSQL 17; confirma la versión y el clúster con los comandos anteriores.

### 2️⃣ Instalar el repositorio oficial de Zabbix 8.0

```bash
cd /tmp
wget https://repo.zabbix.com/zabbix/8.0/release/debian/pool/main/z/zabbix-release/zabbix-release_latest_8.0+debian13_all.deb

dpkg -i zabbix-release_latest_8.0+debian13_all.deb
apt update
```

**Verificación:**

```bash
apt-cache policy zabbix-server-pgsql
```

Comprueba que exista una versión candidata de la rama `8.0`.

### 3️⃣ Instalar Zabbix Server, Frontend y Agent

```bash
apt install -y zabbix-server-pgsql zabbix-frontend-php php8.4-pgsql zabbix-apache-conf zabbix-sql-scripts zabbix-agent
```

**Verificación:**

```bash
zabbix_server -V
dpkg -l | grep -E 'zabbix-server-pgsql|zabbix-frontend-php|zabbix-agent'
```

Si APT no encuentra `php8.4-pgsql`, comprueba los paquetes disponibles antes de continuar:

```bash
php -v
apt-cache policy php-pgsql php8.4-pgsql
```

### 4️⃣ Crear la base de datos y el usuario Zabbix

Crear el usuario PostgreSQL `zabbix`. El comando solicitará ingresar y confirmar una contraseña:

```bash
su - postgres -c "createuser --pwprompt zabbix"
```

Crear la base de datos y asignar su propiedad al usuario `zabbix`:

```bash
su - postgres -c "createdb -O zabbix -E Unicode -T template0 zabbix"
```

**Verificación:**

```bash
su - postgres -c "psql -c '\du zabbix'"
su - postgres -c "psql -l"
```

Confirma que existan el rol `zabbix` y la base de datos `zabbix`. Guarda la contraseña: la necesitarás en el paso 6.

### 5️⃣ Importar el esquema de Zabbix

Importa el esquema inicial en la base de datos:

```bash
zcat /usr/share/zabbix/sql-scripts/postgresql/server.sql.gz | runuser -u zabbix -- psql zabbix
```

Espera a que termine la importación antes de continuar.

**Verificación:**

```bash
runuser -u zabbix -- psql zabbix -c '\dt'
```

También puedes comprobar la cantidad de tablas:

```bash
runuser -u zabbix -- psql zabbix -Atc "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';"
```

El resultado debe ser mayor que cero.

> Si no existe el archivo SQL, revisa la ruta instalada por el paquete:
>
> ```bash
> dpkg -L zabbix-sql-scripts | grep 'postgresql/server.sql'
> ```
>
> **No importes el esquema repetidamente sobre una base ya inicializada.** Si la importación falla, revisa el error antes de decidir si debes recrear la base de datos.

### 6️⃣ Configurar la contraseña de PostgreSQL en Zabbix

Edita el archivo de configuración:

```bash
nano /etc/zabbix/zabbix_server.conf
```

Busca y configura los siguientes parámetros. Si están comentados con `#`, elimina el carácter de comentario:

```ini
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=TuPasswordAqui
```

Reemplaza `TuPasswordAqui` por la contraseña que definiste al crear el usuario PostgreSQL.

Guarda con `Ctrl + O`, confirma con `Enter` y sal con `Ctrl + X`.

**Verificación:**

```bash
grep -E '^(DBHost|DBName|DBUser|DBPassword)=' /etc/zabbix/zabbix_server.conf
```

> El valor de `DBPassword` debe coincidir exactamente con la contraseña del usuario PostgreSQL `zabbix`. Este archivo contiene una credencial; no publiques su contenido.

### 7️⃣ Iniciar y habilitar los servicios

```bash
systemctl enable zabbix-server zabbix-agent apache2 postgresql
systemctl restart postgresql
systemctl restart zabbix-server zabbix-agent apache2
```

**Verificación:**

```bash
systemctl is-active zabbix-server zabbix-agent apache2 postgresql
```

Los cuatro servicios deben indicar `active`. Si alguno falla, revisa los registros antes de continuar.

---

## 🌐 Acceso Web

Obtén la dirección IP del servidor:

```bash
hostname -I
```

**URL:**

```text
http://IP_SERVIDOR/zabbix
```

Abre la dirección desde un navegador de la misma red y completa el asistente web.

**Parámetros de conexión a la base de datos:**

| Campo | Valor |
|---|---|
| Tipo de base de datos | PostgreSQL |
| Host | `localhost` |
| Puerto | `5432` |
| Base de datos | `zabbix` |
| Usuario | `zabbix` |
| Contraseña | La definida en el paso 4 |

**Credenciales iniciales de Zabbix:**

- Usuario: `Admin`
- Contraseña: `zabbix`

> Cambia inmediatamente la contraseña del usuario `Admin` después del primer acceso.

---

## ✅ Verificación

### Estado de los servicios

```bash
systemctl status zabbix-server zabbix-agent apache2 postgresql --no-pager
```

### Listar tablas de la base de datos Zabbix

```bash
runuser -u zabbix -- psql zabbix -c '\dt' | head -15
```

### Revisar los puertos en escucha

```bash
ss -lntp
```

Comprueba que Apache y Zabbix estén escuchando en los puertos que correspondan a tu instalación.

### Revisar logs de Zabbix

```bash
tail -f /var/log/zabbix/zabbix_server.log
```

Presiona `Ctrl + C` para salir del seguimiento.

### Revisar logs de servicios

```bash
journalctl -u zabbix-server -n 50 --no-pager
journalctl -u apache2 -n 50 --no-pager
journalctl -u postgresql -n 50 --no-pager
```

---

## ⚠️ Troubleshooting

| Error | Solución |
|---|---|
| `inacap is not in the sudoers file` | Esta guía se ejecuta como `root`. Ingresa con `su -`; no necesitas `sudo`. |
| `su: Authentication failure` | Comprueba la contraseña de `root`. |
| `could not connect to server` | Comprueba PostgreSQL con `systemctl status postgresql` y `pg_lsclusters`. |
| `password authentication failed for user "zabbix"` | Comprueba que `DBPassword` coincida con la contraseña del rol PostgreSQL `zabbix`. |
| `role "zabbix" does not exist` | Comprueba la creación del usuario con `su - postgres -c "psql -c '\du'"`. |
| `database "zabbix" does not exist` | Comprueba la base de datos con `su - postgres -c "psql -l"`. |
| `server.sql.gz: No such file` | Comprueba la ruta del esquema con `dpkg -L zabbix-sql-scripts`. |
| `Apache2 no responde` | Ejecuta `apache2ctl configtest` y revisa `journalctl -u apache2 -n 100 --no-pager`. |
| Frontend sin soporte PostgreSQL | Comprueba `php8.4-pgsql` con `apt-cache policy php8.4-pgsql` y reinicia Apache. |
| Zabbix Server no inicia | Revisa `/var/log/zabbix/zabbix_server.log` y `journalctl -u zabbix-server -n 100 --no-pager`. |

---

## 🔐 Seguridad (Post-Instalación)

1. **Cambiar la contraseña de `Admin`** desde la interfaz web de Zabbix.
2. **Restringir PostgreSQL a conexiones locales:** comprueba el parámetro `listen_addresses` en el archivo `postgresql.conf` del clúster instalado. Para una instalación local, utiliza:

   ```ini
   listen_addresses = 'localhost'
   ```

   Aplica el cambio:

   ```bash
   systemctl restart postgresql
   ```

3. **Configurar firewall:** Debian no instala necesariamente UFW por defecto. Si administras el servidor por SSH, permite primero el puerto SSH que realmente utilizas.

   ```bash
   apt install -y ufw
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw status verbose
   ```

   Cuando hayas comprobado las reglas, habilita el firewall:

   ```bash
   ufw enable
   ufw status
   ```

4. **No exponer PostgreSQL:** no abras el puerto `5432` a la red si Zabbix y PostgreSQL están en el mismo servidor.
5. **Configurar HTTPS:** utiliza TLS para proteger el acceso web, especialmente si la interfaz será accesible desde otras redes.
6. **Mantener el sistema actualizado:** instala periódicamente las actualizaciones de seguridad de Debian y Zabbix.
7. **Realizar respaldos:** programa copias de seguridad de la base de datos y conserva los archivos de configuración.

### Respaldo básico de la base de datos

Ejecutar como `root`:

```bash
install -d -m 700 /var/backups/zabbix
runuser -u postgres -- pg_dump -Fc zabbix > "/var/backups/zabbix/zabbix_$(date +%F_%H%M).dump"
```

Comprobar el archivo generado:

```bash
ls -lh /var/backups/zabbix/
```

Copia los respaldos a un almacenamiento independiente y comprueba periódicamente que puedan restaurarse.

---

## 📚 Referencias

- [Documentación Oficial Zabbix 8.0](https://www.zabbix.com/documentation/8.0/en)
- [Instalación desde paquetes](https://www.zabbix.com/documentation/8.0/en/manual/installation/install/packages)
- [Database Creation](https://www.zabbix.com/documentation/8.0/en/manual/appendix/install/db_scripts)
- [Requisitos de instalación Zabbix 8.0](https://www.zabbix.com/documentation/8.0/en/manual/installation/requirements)
- [Repositorio oficial Zabbix 8.0 para Debian](https://repo.zabbix.com/zabbix/8.0/release/debian/)

---

**Última actualización:** Noviembre 2026  
**Sistema:** Debian 13 Trixie  
**Método de administración:** `root` mediante `su -`
