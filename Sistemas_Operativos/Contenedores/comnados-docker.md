# 🐳 Docker 

Repositorio de referencia rápida: conceptos esenciales y comandos de consola.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Tabla de contenidos

- [¿Qué es Docker?](#qué-es-docker)
- [¿Para qué se usa?](#para-qué-se-usa)
- [Nomenclaturas](#nomenclaturas)
- [Comandos — Imágenes](#comandos--imágenes)
- [Comandos — Contenedores](#comandos--contenedores)
- [Comandos — Volúmenes](#comandos--volúmenes)
- [Comandos — Redes](#comandos--redes)
- [Comandos — Sistema](#comandos--sistema)

---

## ¿Qué es Docker?

Docker es una plataforma de **contenedorización** que permite empaquetar una aplicación junto con todas sus dependencias en una unidad estándar llamada **contenedor**.

A diferencia de las máquinas virtuales, los contenedores comparten el kernel del sistema operativo anfitrión, lo que los hace mucho más livianos y rápidos.

| | VM | Contenedor |
|---|---|---|
| SO | Completo (kernel propio) | Comparte kernel del host |
| Peso | Varios GB | Decenas de MB |
| Arranque | Minutos | Milisegundos |
| Portabilidad | Limitada | Alta |

---

## ¿Para qué se usa?

- **Desarrollo local** — elimina el "funciona en mi máquina", todos usan el mismo entorno.
- **CI/CD** — entornos reproducibles y desechables en pipelines.
- **Microservicios** — cada servicio corre en su propio contenedor aislado.
- **Despliegue** — el mismo artefacto viaja de desarrollo a producción sin cambios.
- **Versiones** — rollback instantáneo usando tags de imagen.

---

## Nomenclaturas

Estos son los placeholders que aparecen en los comandos de este documento:

| Placeholder | Significado | Ejemplo |
|---|---|---|
| `<img>` | Nombre o ID de una imagen | `nginx`, `ubuntu:22.04`, `myapp:latest` |
| `<id>` | ID o nombre de un contenedor | `a3f8b2c1d4e5`, `mi-contenedor` |
| `<nombre>` / `<n>` | Nombre que le asignás al recurso | `mi-app`, `red-backend` |
| `<tag>` | Versión o etiqueta de una imagen | `latest`, `1.0`, `stable` |
| `<ruta>` | Ruta dentro del sistema de archivos | `/app/data`, `/etc/nginx/nginx.conf` |
| `<vol>` | Nombre de un volumen Docker | `db-data`, `static-files` |
| `<puerto_host>` | Puerto en tu máquina local | `8080`, `3000` |
| `<puerto_cont>` | Puerto expuesto por el contenedor | `80`, `3000` |
| `<var>` | Variable de entorno | `NODE_ENV=production` |
| `<red>` | Nombre de una red Docker | `backend-net`, `bridge` |
| `<nuevo>` | Nuevo nombre o tag para una imagen | `myapp:v2`, `user/repo:latest` |

---

## Comandos — Imágenes

Las **imágenes** son plantillas de solo lectura a partir de las cuales se crean los contenedores.

```bash
# Listar imágenes descargadas localmente
docker images

# Descargar imagen desde Docker Hub (o registry configurado)
docker pull <img>
docker pull <img>:<tag>          # con tag específico, ej: docker pull node:20

# Construir imagen desde un Dockerfile en el directorio actual
docker build -t <nombre> .
docker build -t <nombre>:<tag> . # con tag, ej: docker build -t miapp:1.0 .

# Crear un alias/tag para una imagen existente
docker tag <img> <nuevo>         # ej: docker tag miapp:latest usuario/miapp:1.0

# Subir imagen a un registry (Docker Hub u otro)
docker push <img>
docker push <nombre>:<tag>

# Eliminar imagen local
docker rmi <img>
docker rmi <img> <img2>          # eliminar varias a la vez

# Buscar imágenes en Docker Hub
docker search <nombre>

# Eliminar imágenes sin tag ni uso (dangling images)
docker image prune

# Eliminar TODAS las imágenes no usadas por ningún contenedor
docker image prune -a
```

---

## Comandos — Contenedores

Un **contenedor** es una instancia en ejecución de una imagen. Es efímero por diseño.

```bash
# Crear y arrancar un contenedor (se elimina solo al detenerlo con --rm)
docker run <img>
docker run --rm <img>

# Modo detached (background) + mapeo de puertos
docker run -d -p <puerto_host>:<puerto_cont> <img>
# ej: docker run -d -p 8080:80 nginx

# Asignar nombre + variable de entorno + volumen + red
docker run -d \
  --name <nombre> \
  -p <puerto_host>:<puerto_cont> \
  -e <var> \
  -v <vol>:<ruta> \
  --network <red> \
  <img>

# Listar contenedores activos
docker ps

# Listar todos los contenedores (incluye detenidos)
docker ps -a

# Detener contenedor (envía SIGTERM, espera, luego SIGKILL)
docker stop <id>

# Detener todos los contenedores activos
docker stop $(docker ps -q)

# Iniciar contenedor detenido
docker start <id>

# Reiniciar contenedor
docker restart <id>

# Eliminar contenedor detenido
docker rm <id>

# Forzar eliminación aunque esté corriendo
docker rm -f <id>

# Eliminar todos los contenedores detenidos
docker container prune

# Ver logs del contenedor
docker logs <id>
docker logs -f <id>              # seguir logs en tiempo real
docker logs --tail 100 <id>      # últimas 100 líneas

# Abrir shell interactiva dentro del contenedor
docker exec -it <id> bash        # si tiene bash
docker exec -it <id> sh          # alternativa con sh

# Ejecutar comando puntual dentro del contenedor
docker exec <id> <comando>       # ej: docker exec mi-db env

# Ver detalles completos del contenedor en JSON
docker inspect <id>

# Monitoreo de CPU, memoria y red en tiempo real
docker stats
docker stats <id>                # solo un contenedor

# Copiar archivos entre host y contenedor
docker cp <id>:<ruta> .          # contenedor → host
docker cp ./archivo <id>:<ruta>  # host → contenedor

# Ver procesos corriendo dentro del contenedor
docker top <id>

# Ver puertos mapeados del contenedor
docker port <id>
```

---

## Comandos — Volúmenes

Los **volúmenes** permiten persistir datos más allá del ciclo de vida del contenedor.

```bash
# Listar volúmenes
docker volume ls

# Crear volumen nombrado
docker volume create <n>

# Ver detalles de un volumen
docker volume inspect <n>

# Eliminar volumen
docker volume rm <n>

# Eliminar todos los volúmenes sin uso
docker volume prune

# Montar volumen al crear contenedor
docker run -v <vol>:<ruta> <img>
# ej: docker run -v db-data:/var/lib/mysql mysql

# Bind mount: montar directorio del host directamente
docker run -v $(pwd):<ruta> <img>
# ej: docker run -v $(pwd):/app node
# o con ruta absoluta:
docker run -v /home/user/proyecto:/app <img>

# Volumen de solo lectura
docker run -v <vol>:<ruta>:ro <img>
```

---

## Comandos — Redes

Las **redes** controlan cómo se comunican los contenedores entre sí y con el exterior.

```bash
# Listar redes
docker network ls

# Crear red personalizada (tipo bridge por defecto)
docker network create <n>
docker network create --driver bridge <n>

# Ver detalles de una red (contenedores conectados, etc.)
docker network inspect <n>

# Conectar contenedor en ejecución a una red
docker network connect <red> <id>

# Desconectar contenedor de una red
docker network disconnect <red> <id>

# Eliminar red
docker network rm <n>

# Eliminar todas las redes sin uso
docker network prune

# Crear contenedor y conectarlo a una red
docker run --network <red> <img>
```

> Tip: los contenedores en la misma red bridge personalizada se pueden comunicar
> usando el **nombre del contenedor** como hostname, sin necesidad de IPs.

---

## Comandos — Sistema

```bash
# Información general del daemon Docker
docker info

# Versión del cliente y del servidor
docker version

# Uso de disco: imágenes, contenedores y volúmenes
docker system df
docker system df -v              # detalle por recurso

# Limpieza general: elimina contenedores detenidos,
# redes sin uso, imágenes dangling y cache de build
docker system prune

# Limpieza total: incluye imágenes sin contenedor asociado
docker system prune -a

# Limpieza total incluyendo volúmenes (¡cuidado con datos persistidos!)
docker system prune -a --volumes

# --- Docker Compose ---

# Levantar servicios definidos en compose.yml (modo background)
docker compose up -d

# Detener y eliminar contenedores del compose (mantiene volúmenes)
docker compose down

# Detener y eliminar contenedores + volúmenes
docker compose down -v

# Ver logs de todos los servicios
docker compose logs -f

# Reconstruir imágenes antes de levantar
docker compose up -d --build

# Escalar un servicio
docker compose up -d --scale <servicio>=<n>
# ej: docker compose up -d --scale worker=3

# Ver estado de los servicios
docker compose ps
```

---

> Tip: en cualquier comando usá `--help` para ver todas las opciones disponibles.
> Ejemplo: `docker run --help` o `docker network --help`
