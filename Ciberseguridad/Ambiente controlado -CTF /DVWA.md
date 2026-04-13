# DVWA — Damn Vulnerable Web Application

## ¿Qué es?

**DVWA** (Damn Vulnerable Web Application) es una aplicación web intencionalmente vulnerable, desarrollada en PHP con base de datos MySQL. Está diseñada para que estudiantes y profesionales de seguridad practiquen técnicas de ataque y defensa en un entorno legal y controlado.

Es una de las herramientas más usadas en diplomados, bootcamps y laboratorios de ciberseguridad por su facilidad de despliegue y la variedad de vulnerabilidades que cubre.

---

## Características

- Cubre las vulnerabilidades web más comunes del estándar **OWASP Top 10**.
- Permite ajustar el nivel de dificultad: **Low**, **Medium**, **High** e **Impossible**.
- Cada módulo incluye documentación con pistas y explicación técnica de la vulnerabilidad.
- Panel de administración para resetear la base de datos y cambiar configuraciones.
- Compatible con herramientas como **Burp Suite**, **sqlmap**, **Hydra**, entre otras.

---

## Vulnerabilidades disponibles

| Módulo | Tipo de ataque |
|---|---|
| Brute Force | Fuerza bruta en formularios de login |
| Command Injection | Inyección de comandos del sistema operativo |
| CSRF | Cross-Site Request Forgery |
| File Inclusion | Local File Inclusion (LFI) y Remote File Inclusion (RFI) |
| File Upload | Subida de archivos maliciosos |
| SQL Injection | Inyección SQL manual |
| SQL Injection (Blind) | Inyección SQL a ciegas |
| Weak Session IDs | Análisis y predicción de IDs de sesión débiles |
| XSS (DOM) | Cross-Site Scripting basado en el DOM |
| XSS (Reflected) | XSS reflejado |
| XSS (Stored) | XSS persistente |

---

## Instalación con Docker

La forma más rápida y recomendada para usar DVWA es mediante Docker.

### Requisitos previos

- Tener **Docker** instalado. Puedes verificarlo con:

```bash
docker --version
```

### Instalar y ejecutar el contenedor

```bash
docker pull vulnerables/web-dvwa
```

```bash
docker run -d -p 8080:80 vulnerables/web-dvwa
```

Esto descarga la imagen oficial y levanta el contenedor exponiendo DVWA en el puerto `8080` de tu máquina local.

---

## Iniciar y acceder a DVWA

1. Abre tu navegador y ve a:

```
http://localhost:8080
```

2. Inicia sesión con las credenciales por defecto:

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `password` |

3. En la pantalla de bienvenida, haz clic en **"Create / Reset Database"** para inicializar la base de datos. Serás redirigido al login automáticamente.

4. Vuelve a iniciar sesión con las mismas credenciales.

---

## Configurar el nivel de dificultad

Una vez dentro, ve a **DVWA Security** en el menú lateral y selecciona el nivel deseado:

| Nivel | Descripción |
|---|---|
| **Low** | Sin protecciones. Ideal para aprender el ataque básico. |
| **Medium** | Protecciones parciales. Requiere evadir filtros simples. |
| **High** | Protecciones avanzadas. Exige técnicas más elaboradas. |
| **Impossible** | Código seguro de referencia. Útil para comparar con los niveles vulnerables. |

---

## Detener el contenedor

Para detener DVWA cuando termines la práctica:

```bash
# Ver el ID del contenedor en ejecución
docker ps

# Detener el contenedor
docker stop <CONTAINER_ID>
```

---

## ⚠️ Aviso de seguridad

> DVWA está diseñado exclusivamente para entornos de laboratorio. **Nunca lo expongas en una red pública ni en producción.** Usa modo de red `Host-Only` o `Internal Network` en tu virtualizador.
