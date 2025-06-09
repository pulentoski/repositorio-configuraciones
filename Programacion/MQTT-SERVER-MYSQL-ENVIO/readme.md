# Script para iniciar servidor mqtt y enviar datos a MYSQL

## Inicia entorno virtual:
    python3 -m venv mqtt_env
    source mqtt_env/bin/activate

## Instalar dependencias
    apt-get update
    apt-get install -y mosquitto mosquitto-clients python3-pip
    pip install paho-mqtt mysql-connector-python

## niciar Mosquitto:
    sudo systemctl start mosquitto
    sudo systemctl enable mosquitto

# Ejecutar el script:
    python3 mqtt_to_mysql.py
