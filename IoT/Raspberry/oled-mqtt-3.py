#!/usr/bin/env python3
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT
import time
import psutil
import socket
import paho.mqtt.client as mqtt
import threading
import logging

# --- Credenciales MQTT ---
BROKER_MQTT = "192.168.0.19"
PUERTO = 1883
USUARIO_MQTT = "daniel1"
CONTRASENA_MQTT = "daniel1"
TOPICO_COMANDOS = "comandos"
# --------------------------

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

# Variables globales
ultimo_comando = "Esperando comandos"
mqtt_conectado = False

def obtener_direccion_ip(interfaz='eth0'):
    try:
        interfaces = psutil.net_if_addrs()
        if interfaz in interfaces:
            for direccion in interfaces[interfaz]:
                if direccion.family == socket.AF_INET:
                    return direccion.address
        return f"{interfaz}: Sin IP"
    except Exception as e:
        logger.error(f"Error al obtener la IP: {e}")
        return "Error IP"

# Callback al conectar
def al_conectar(cliente, userdata, flags, rc):
    global mqtt_conectado
    if rc == 0:
        mqtt_conectado = True
        cliente.subscribe(TOPICO_COMANDOS)
        logger.info(f"Conectado al broker MQTT en {BROKER_MQTT}:{PUERTO}")
    else:
        mqtt_conectado = False
        logger.error(f"Error al conectar con MQTT (código {rc})")

# Callback al recibir mensaje
def al_recibir_mensaje(cliente, userdata, msg):
    global ultimo_comando
    try:
        if msg.topic == TOPICO_COMANDOS:
            payload = msg.payload.decode()
            ultimo_comando = f"Cmd: {payload[:20]}"
            logger.info(f"Mensaje recibido en '{msg.topic}': {payload}")
    except Exception as e:
        logger.error(f"Error al procesar el mensaje: {e}")

# Hilo MQTT
def hilo_cliente_mqtt():
    cliente = mqtt.Client()
    cliente.on_connect = al_conectar
    cliente.on_message = al_recibir_mensaje
    cliente.username_pw_set(USUARIO_MQTT, CONTRASENA_MQTT)

    try:
        cliente.connect(BROKER_MQTT, PUERTO, 60)
        cliente.loop_forever()
    except Exception as e:
        logger.error(f"Error en el hilo del cliente MQTT: {e}")

# Pantalla: info del sistema
def mostrar_info_sistema():
    uso_cpu = psutil.cpu_percent()
    uso_ram = psutil.virtual_memory().percent
    ip_eth = obtener_direccion_ip('eth0')
    ip_wlan = obtener_direccion_ip('wlan0')

    with canvas(device) as dibujar:
        text(dibujar, (0, 0), f"CPU: {uso_cpu}%", font=proportional(CP437_FONT), fill="white")
        text(dibujar, (0, 10), f"RAM: {uso_ram}%", font=proportional(CP437_FONT), fill="white")
        text(dibujar, (0, 20), f"ETH: {ip_eth}", font=proportional(CP437_FONT), fill="white")
        text(dibujar, (0, 30), f"WLAN: {ip_wlan}", font=proportional(CP437_FONT), fill="white")

# Pantalla: estado MQTT y comando
def mostrar_mensajes_mqtt():
    with canvas(device) as dibujar:
        estado_mqtt = "CONECTADO" if mqtt_conectado else "DESCONECTADO"
        text(dibujar, (0, 0), f"MQTT: {estado_mqtt}", font=proportional(CP437_FONT), fill="white")
        text(dibujar, (0, 10), ultimo_comando, font=proportional(CP437_FONT), fill="white")

# Main loop
def main():
    threading.Thread(target=hilo_cliente_mqtt, daemon=True).start()

    try:
        while True:
            for _ in range(4):
                mostrar_info_sistema()
                time.sleep(1)
            for _ in range(4):
                mostrar_mensajes_mqtt()
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Script detenido manualmente por el usuario.")
    except Exception as e:
        logger.critical(f"¡Error crítico!: {e}")

if __name__ == "__main__":
    main()
