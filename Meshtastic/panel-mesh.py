#!/usr/bin/env python3
import serial
import subprocess
import meshtastic
import meshtastic.serial_interface
from datetime import datetime
import time
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('meshtastic_control.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Configuración
SERIAL_PORT = "/dev/ttyUSB0"  # Cambiar si es necesario
CHANNEL_NAME = "LongFast"     # Usar canal por defecto

def execute_command(command):
    """Ejecuta comandos en el sistema con manejo de errores"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return f"✅ {datetime.now().strftime('%H:%M:%S')}:\n{result.stdout[:200]}"
    except subprocess.CalledProcessError as e:
        return f"❌ {datetime.now().strftime('%H:%M:%S')}:\n{e.stderr[:200]}"

def main():
    interface = None
    try:
        # Inicializa conexión según documentación oficial
        logger.info(f"Conectando a {SERIAL_PORT}...")
        interface = meshtastic.serial_interface.SerialInterface(devPath=SERIAL_PORT)
        
        # Obtiene información del nodo local
        our_node = interface.getNode('^local')
        logger.info(f"Configuración del nodo:\n{our_node.localConfig}")
        
        logger.info(f"\nEscuchando comandos en canal {CHANNEL_NAME}...")
        logger.info("Formato: cmd:tu_comando (ej: cmd:ls -la)")
        logger.info("!reset para reiniciar dispositivo\n")

        # Configuración del puerto serial directamente
        ser = interface.stream

        while True:
            try:
                # Verifica si hay datos disponibles
                if ser.in_waiting > 0:
                    msg = ser.readline().decode().strip()
                    
                    if msg.startswith("cmd:"):
                        command = msg[4:]
                        logger.info(f"Ejecutando: {command}")
                        response = execute_command(command)
                        interface.sendText(response)
                        logger.info("Respuesta enviada al mesh")
                    
                    elif msg == "!reset":
                        logger.info("Reiniciando dispositivo...")
                        interface.sendText("Reiniciando...")
                        time.sleep(2)
                        interface.close()
                        time.sleep(10)  # Espera a que se reinicie
                        interface = meshtastic.serial_interface.SerialInterface(devPath=SERIAL_PORT)
                        ser = interface.stream
                        
            except KeyboardInterrupt:
                logger.info("Deteniendo por solicitud del usuario...")
                break
            except Exception as e:
                logger.error(f"Error en bucle principal: {str(e)}")
                time.sleep(5)

    except Exception as e:
        logger.error(f"Error inicial: {str(e)}")
    finally:
        if interface:
            interface.close()
        logger.info("Conexión cerrada")

if __name__ == "__main__":
    main()
