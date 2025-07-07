# Meshtastic Control Script

Este repositorio contiene un script en Python para controlar un nodo Meshtastic conectado por USB (o serial) desde una Raspberry Pi (o cualquier Linux). El script permite ejecutar comandos de sistema remotamente a través de mensajes enviados por la red Meshtastic, y responde con el resultado del comando. Ideal para automatización, diagnóstico y administración remota de dispositivos mesh.

---

## ¿Qué hace este script?

- **Escucha** mensajes de texto enviados por la red Meshtastic que empiecen con `cmd:`.
- **Ejecuta** el comando de consola recibido (ejemplo: `cmd:uptime`).
- **Responde** por la red Meshtastic con la salida del comando.
- **Detecta automáticamente** el puerto serial del nodo (`/dev/ttyUSB*` o `/dev/ttyACM*`).
- **Evita errores** si el puerto está ocupado o no hay dispositivos conectados.
- **Registra logs** en consola y en el archivo `meshtastic_control.log`.

---

## Instalación y Primeros Pasos

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/meshtastic-control.git
cd meshtastic-control
```

### 2. Crear y activar un entorno virtual

```bash
python3 -m venv meshtastic_env
source meshtastic_env/bin/activate
```

### 3. Actualizar pip y herramientas

```bash
pip install --upgrade pip setuptools wheel
```

### 4. Instalar dependencias

```bash
pip install meshtastic pyserial pypubsub
```

> Si usas Raspberry Pi y tienes problemas de compilación, prueba:
> ```bash
> pip install --no-cache-dir --index-url https://pypi.org/simple meshtastic
> ```

---

## Ejecución del Script

Asegúrate de tener conectado tu nodo Meshtastic por USB.

```bash
python3 meshtastic_control.py
```

El script buscará automáticamente el puerto correcto y quedará escuchando mensajes.

---

## Ejemplo de Uso

Desde otro nodo Meshtastic, envía un mensaje de texto con el formato:

```
cmd:ls
```
O, por ejemplo:
```
cmd:uptime
```

El resultado del comando aparecerá como respuesta por la red Meshtastic.

---

## Notas y Seguridad

- **¡Cuidado!** Cualquier usuario de la red mesh que conozca este formato podrá ejecutar comandos en tu sistema. Usa solo en entornos controlados.
- Si detienes el script con `Ctrl+Z`, deberás liberar el puerto con `kill %n` (ver [FAQ](#faq)).
- Todos los logs quedan en `meshtastic_control.log`.

---

## FAQ

### ¿Qué hago si me da error de puerto ocupado?
1. Ejecuta `jobs` para ver procesos suspendidos.
2. Libera el proceso con `kill %n` (donde `n` es el número del job).
3. Si el puerto sigue ocupado, busca procesos Python y mátalos con `kill -9 PID`.

### ¿Cómo agrego más comandos permitidos?
Edita el script y personaliza la función `on_receive` para filtrar o validar los comandos recibidos.

---


