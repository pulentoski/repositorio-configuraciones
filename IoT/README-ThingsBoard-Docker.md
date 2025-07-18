# ThingsBoard CE en Raspberry Pi con Docker

Instalación y despliegue de ThingsBoard Community Edition (`v3.6.4`) en una Raspberry Pi (ARM64) usando Docker y Docker Compose.

---

## ✅ Requisitos

- Raspberry Pi 3 o superior (64-bit, con Debian Bookworm o compatible)
- Docker y Docker Compose instalados
- Acceso a red local o Internet
- 1 GB de RAM mínimo (recomendado 2 GB)

---

## ⚙️ Instalación paso a paso

### 1. Clonar repositorio oficial

```bash
git clone https://github.com/thingsboard/thingsboard.git
cd thingsboard/docker
```

### 2. Crear archivo `.env` personalizado (opcional)

Puedes definir el token, puerto y parámetros si deseas modificar la configuración. Por defecto, el sistema usa:

- HTTP: `8080 → 9090`
- MQTT: `1883`
- COAP: `5683`

### 3. Iniciar contenedores

```bash
docker compose -f docker-compose.yml up -d
```

Esto iniciará:

- `tb-postgres` (base de datos PostgreSQL)
- `thingsboard` (servidor principal)

> El sistema se desplegará en `http://<IP_RASPBERRY>:8080`

### 4. Verifica contenedores activos

```bash
docker ps
```

Debe mostrar ambos contenedores corriendo (`STATUS: Up`).

---

## 🔑 Acceso

Por defecto:

- URL: `http://192.168.x.x:8080`
- Usuario admin: `tenant@thingsboard.org`
- Contraseña: `tenant`

---

## 🛠️ Errores comunes y soluciones

| Problema                                         | Solución                                                                 |
|--------------------------------------------------|--------------------------------------------------------------------------|
| `ERR_CONNECTION_REFUSED`                         | Verifica que el contenedor esté en `Up`, que el puerto `8080` esté abierto |
| `docker logs thingsboard` no muestra errores     | Asegúrate que el puerto `9090` esté asignado correctamente al host (`8080`) |
| No carga interfaz web                            | Espera 2-3 minutos tras primer inicio; ThingsBoard tarda en levantar     |
| PostgreSQL error `already running`               | Otro contenedor ya usa `5432`. Reinicia con `docker compose restart`     |
| No se puede editar config (sin `nano`, `vi`)     | Usa `cat`, `echo` o instala con `apt update && apt install nano -y` dentro del contenedor |

---

## ▶️ Arranque manual

Si detienes la Raspberry Pi o apagas Docker:

```bash
cd ~/thingsboard/docker
docker compose up -d
```

---

## 🧹 Parar y eliminar contenedores

```bash
docker compose down
```

---

## 📁 Archivos importantes

| Archivo                         | Descripción                        |
|---------------------------------|------------------------------------|
| `docker-compose.yml`            | Define los servicios de Docker     |
| `thingsboard.yml`               | Configuración principal del servidor ThingsBoard |
| `docker/.env` (opcional)        | Variables de entorno del despliegue |

---

## 📝 Recursos adicionales

- [ThingsBoard Docs](https://thingsboard.io/docs/)
- [Community Forum](https://groups.google.com/g/thingsboard)

---

**Autor:** Tu nombre  
**Repositorio:** https://github.com/tuusuario/tu-repo  
**Licencia:** MIT
