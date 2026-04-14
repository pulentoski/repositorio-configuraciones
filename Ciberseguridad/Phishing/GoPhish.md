# Instalación GoPhish v0.12.1 — Kali Linux (VirtualBox)

## Requisitos previos

- Máquina virtual Kali Linux corriendo en VirtualBox
- Conexión a internet en la VM (solo para la descarga)
- Terminal abierta como root o con sudo

---

## Paso 1 — Descargar GoPhish

```bash
wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
```

Verificar la integridad del archivo con SHA256:

```bash
sha256sum gophish-v0.12.1-linux-64bit.zip
```

El hash debe coincidir exactamente con:

```
44f598c1eeb72c3b08fa73d57049022d96cea2872283b87a73d21af78a2c6d47
```

> Si no coincide, no continuar. Volver a descargar el archivo.

---

## Paso 2 — Descomprimir

```bash
unzip gophish-v0.12.1-linux-64bit.zip -d gophish
cd gophish
```

---

## Paso 3 — Dar permisos de ejecución

```bash
chmod +x gophish
```

---

## Paso 4 — Ejecutar GoPhish

```bash
sudo ./gophish
```

Al iniciar por primera vez, GoPhish generará una contraseña temporal y la mostrará en la terminal:

```
time="..." level=info msg="Please login with the username admin and the password <CONTRASEÑA-GENERADA>"
```

> Copiar esa contraseña antes de continuar.

---

## Paso 5 — Acceder al panel de administración

Abrir el navegador en Kali e ingresar:

```
https://127.0.0.1:3333
```

El navegador mostrará una advertencia de certificado SSL. Hacer clic en **Avanzado → Aceptar el riesgo y continuar**.

Iniciar sesión con:
- Usuario: `admin`
- Contraseña: la generada en el paso anterior

El sistema pedirá cambiar la contraseña de inmediato. Establecer una nueva y guardarla.

---

## Paso 6 — Verificar los puertos activos

GoPhish levanta dos servicios simultáneamente:

| Servicio | Puerto | Uso |
|---|---|---|
| Panel de administración | 3333 (HTTPS) | Gestión de campañas |
| Servidor de phishing | 80 (HTTP) | Landing pages y tracking |

Verificar que ambos puertos estén escuchando:

```bash
ss -tlnp | grep -E '80|3333'
```

---

## Paso 7 — Instalar MailHog (servidor SMTP local)

MailHog simula un servidor de correo sin necesidad de internet ni configuración externa.

```bash
sudo apt update
sudo apt install golang-go -y
go install github.com/mailhog/MailHog@latest
~/go/bin/MailHog
```

MailHog levantará:
- Servidor SMTP en el puerto **1025** (para GoPhish)
- Interfaz web en `http://127.0.0.1:8025` (para ver los correos enviados)

---

## Paso 8 — Confirmar que todo funciona

Abrir dos terminales en Kali:
- **Terminal 1:** GoPhish corriendo → `sudo ./gophish`
- **Terminal 2:** MailHog corriendo → `~/go/bin/MailHog`

Desde el navegador verificar acceso a:

| URL | Servicio |
|---|---|
| `https://127.0.0.1:3333` | Panel GoPhish |
| `http://127.0.0.1:8025` | Bandeja MailHog |

Si ambas cargan correctamente, el entorno está listo para el laboratorio.

---

## Notas importantes

- No cerrar ninguna de las dos terminales mientras dure el laboratorio. Cerrarlas detiene los servicios.
- Si el puerto 80 da error de permisos, cambiar el puerto de phishing en `config.json` a uno mayor a 1024, por ejemplo `8080`.
- El archivo `gophish.db` guarda toda la configuración y resultados. No borrarlo entre sesiones si se quiere conservar el trabajo.
