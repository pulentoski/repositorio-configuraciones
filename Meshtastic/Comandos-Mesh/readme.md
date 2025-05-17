este es un script para utiliar Meshtastic y ejecutar comandos a un host linux.
El host debe estar conectado por puerto serial (usb) a una placa con Meshtastic y mediante un script en python, se podra ejecutar comandos en el host.

Instalar dependencias del sistema:

    apt update
    apt install python3-venv python3-pip python3-dev libjpeg-dev zlib1g-dev


Entorno virtual

    python3 -m venv ~/oled_env  
    source ~/oled_env/bin/activate
    pip install luma.oled psutil meshtastic pillow


script que interpreta comandos:

    nano /etc/systemd/system/oled_mqtt.service

Crear servicio systemd:

    nano /etc/systemd/system/oled_mqtt.service

Pegar configuración del servicio:

    [Unit]
    Description=OLED MQTT Service
    After=network.target
    
    [Service]
    User=root
    WorkingDirectory=/opt/oled_mqtt
    ExecStart=/root/oled_env/bin/python /opt/oled_mqtt/oled_mqtt.py
    Restart=always
    RestartSec=10s
    
    [Install]
    WantedBy=multi-user.target



Habilitar y ejecutar:

    chmod +x /opt/oled_mqtt/oled_mqtt.py
    systemctl daemon-reload
    systemctl enable oled_mqtt.service
    systemctl enable oled_mqtt.service
