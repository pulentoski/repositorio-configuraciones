# ThingsBoard + Docker: Instalación profesional

Guía técnica y resumida para instalar ThingsBoard usando Docker en **Raspberry Pi** o **Ubuntu**.

---

## 🧰 Requisitos

- Sistema operativo: Raspberry Pi OS 64-bit (Bookworm) o Ubuntu 20.04+.
- Docker y Docker Compose instalados.
- Acceso como root o usuario con `sudo`.

---

## ⚙️ Instalación de Docker (si no está instalado)

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🚀 Clonar el repositorio oficial de ThingsBoard

```bash
git clone https://github.com/thingsboard/thingsboard.git
cd thingsboard/docker
```

---

## ⚙️ Crear archivo `.env` personalizado (opcional)

Puedes definir el token, puerto y parámetros si deseas modificar la configuración. Por defecto, el sistema usa:

- HTTP: 8080 → 9090
- MQTT: 1883
- COAP: 5683

### ✍️ Ejemplo de `.env`

```env
# Puertos
HTTP_PORT=8080
MQTT_PORT=1883
COAP_PORT=5683
LWM2M_PORT=5685
SNMP_PORT=162

# Usuario administrador de ThingsBoard
TB_ADMIN_USER=admin@thingsboard.org
TB_ADMIN_PASSWORD=admin

# Configuración de demo
DEMO=true
DEMO_TOKEN=hQwQ8OSYXufnWW2LGekf

# Base de datos PostgreSQL
POSTGRES_DB=thingsboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=tb-postgres
POSTGRES_PORT=5432

# Volúmenes de datos
DATA_DIR=./data
LOGS_DIR=./logs

```

Guarda este archivo en `thingsboard/docker/.env`.

---

## 🧱 Iniciar ThingsBoard

```bash
docker compose up -d
```

Accede vía navegador a:

```text
http://<TU_IP_LOCAL>:8080
```

Usuario por defecto:

- **admin@thingsboard.org**
- **admin**

---

## 🛠️ Ver logs y verificar estado

```bash
docker ps
docker logs -f thingsboard
```

---

## ❗ Problemas comunes

| Error                              | Solución                                                                 |
|-----------------------------------|--------------------------------------------------------------------------|
| `ERR_CONNECTION_REFUSED`          | Verifica que el contenedor esté corriendo: `docker ps`                   |
| `ModuleNotFoundError` en Python   | Usa entorno virtual o instala con: `pip install --break-system-packages` |
| No carga en el navegador          | Espera 2-3 min tras `docker-compose up`, o revisa logs                   |

---

## 🧼 Parar o reiniciar

```bash
docker compose down        # Detiene y elimina contenedores
docker compose restart     # Reinicia contenedores
```

---

## 📦 Desinstalación

```bash
docker compose down -v     # Borra contenedores y volúmenes
```

---

## 🧪 Probado en

- Raspberry Pi 3 / 4 (aarch64)
- Ubuntu 22.04 LTS
