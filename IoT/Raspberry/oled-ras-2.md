# Configuración del Script Automático con Entorno Virtual para OLED en Raspberry Pi

Este documento explica cómo configurar un script en Raspberry Pi para ejecutar automáticamente un programa de pantalla OLED utilizando un entorno virtual de Python cada vez que la Raspberry Pi se reinicie o se inicie.
Requisitos Previos

    Raspberry Pi con sistema operativo Linux (Raspberry Pi OS).

    Python 3 instalado.

    Entorno virtual de Python (creado previamente).

    Paquetes necesarios instalados (como Adafruit-SSD1306).

## Paso 1: Crear un Script de Ejecución
###1.1 Crear el archivo run_oled.sh

Este script activará el entorno virtual y ejecutará el script de la pantalla OLED.

    nano /home/daniel/Documents/run_oled.sh

Contenido del archivo run_oled.sh:

    #!/bin/bash
    source /home/daniel/Documents/oled_env/bin/activate  # Activar entorno virtual
    python3 /home/daniel/Documents/codigo.py  # Ejecutar el script

### 1.2 Dar permisos de ejecución

Una vez creado el archivo, es necesario darle permisos para que pueda ejecutarse:

    chmod +x /home/daniel/Documents/run_oled.sh

## Paso 2: Crear el Servicio systemd
### 2.1 Crear el archivo del servicio

Este servicio se configurará para ejecutar el script run_oled.sh cada vez que la Raspberry Pi inicie.

    sudo nano /etc/systemd/system/run_oled.service

Contenido del archivo run_oled.service:

    [Unit]
    Description=OLED script in virtualenv
    After=network.target  # Asegura que el script se ejecute después de que la red esté disponible
    
    [Service]
    ExecStart=/home/daniel/Documents/run_oled.sh  # Ruta al script de ejecución
    WorkingDirectory=/home/daniel/Documents  # Directorio de trabajo
    User=daniel  # Usuario para ejecutar el script
    Group=daniel  # Grupo asociado
    Restart=always  # Asegura que el servicio se reinicie si se detiene
    
    [Install]
    WantedBy=multi-user.target  # El servicio se inicia con el sistema

### 2.2 Recargar systemd y habilitar el servicio

Una vez creado el archivo del servicio, recarga systemd para que reconozca el nuevo servicio y habilítalo para que se inicie automáticamente.

    sudo systemctl daemon-reload  # Recargar los servicios
    sudo systemctl enable run_oled.service  # Habilitar el servicio

### 2.3 Iniciar el servicio

Para probar si todo está funcionando correctamente, inicia el servicio manualmente.

    sudo systemctl start run_oled.service

## Paso 3: Verificación y Reinicio
### 3.1 Verificar la ejecución

Para comprobar que el servicio se está ejecutando correctamente, puedes revisar el estado del servicio con:

    sudo systemctl status run_oled.service

### 3.2 Reiniciar la Raspberry Pi

Para asegurarte de que todo funcione correctamente después de un reinicio, reinicia la Raspberry Pi:

    sudo reboot

El script debería ejecutarse automáticamente cada vez que se reinicie o encienda la Raspberry Pi.
Notas

    Entorno Virtual: El script se ejecutará dentro de un entorno virtual de Python para evitar conflictos de dependencias o versiones de paquetes del sistema.

    Servicio systemd: Este servicio se configura para que se ejecute en el inicio del sistema y reinicie automáticamente si falla.

    Paquetes Python: Asegúrate de tener todos los paquetes necesarios instalados dentro del entorno virtual para que el script funcione correctamente (como Adafruit-SSD1306).
