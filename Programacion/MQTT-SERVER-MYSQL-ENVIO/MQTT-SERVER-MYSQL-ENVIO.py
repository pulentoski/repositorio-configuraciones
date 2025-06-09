import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime
import json
import subprocess
import socket
import time
import logging

# Configuración MySQL
MYSQL_CONFIG = {
    'host': '52.6.1.81',
    'user': 'adminsql',
    'password': 'Admin123',
    'database': 'sensores_db',
    'port': 3306
}

# Configuración MQTT
MQTT_CONFIG = {
    'host': 'localhost',  # Broker local
    'port': 1883,
    'keepalive': 60,
    'topic': 'daniel',    # Tópico específico
    'qos': 0
}

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mqtt_mysql.log'),
        logging.StreamHandler()
    ]
)

def verify_mosquitto():
    """Verifica si Mosquitto está instalado y corriendo"""
    try:
        # Verificar servicio systemd
        result = subprocess.run(['systemctl', 'is-active', 'mosquitto'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Mosquitto está corriendo como servicio")
            return True
        
        # Verificar proceso directamente
        result = subprocess.run(['pgrep', 'mosquitto'], capture_output=True)
        if result.returncode == 0:
            logging.info("Mosquitto está corriendo como proceso")
            return True
            
        logging.error("Mosquitto no está corriendo")
        return False
        
    except Exception as e:
        logging.error(f"Error al verificar Mosquitto: {str(e)}")
        return False

def create_table():
    """Crea la tabla si no existe"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mqtt_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            topic VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            qos TINYINT NOT NULL,
            retain BOOLEAN NOT NULL DEFAULT FALSE,
            INDEX(topic),
            INDEX(timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        conn.commit()
        logging.info("Tabla mqtt_messages verificada/creada")
        
    except mysql.connector.Error as err:
        logging.error(f"Error MySQL: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"Conectado al broker MQTT. Suscrito a: {MQTT_CONFIG['topic']}")
        client.subscribe(MQTT_CONFIG['topic'], qos=MQTT_CONFIG['qos'])
    else:
        logging.error(f"Error de conexión MQTT: Código {rc}")

def on_message(client, userdata, msg):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Intentar parsear JSON
        try:
            payload = json.loads(msg.payload.decode())
            message = json.dumps(payload, ensure_ascii=False)
        except:
            message = msg.payload.decode()
        
        cursor.execute("""
        INSERT INTO mqtt_messages 
        (timestamp, topic, message, qos, retain)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            datetime.now(),
            msg.topic,
            message,
            msg.qos,
            msg.retain
        ))
        
        conn.commit()
        logging.info(f"Mensaje almacenado: {msg.topic} - {message[:100]}...")
        
    except mysql.connector.Error as err:
        logging.error(f"Error MySQL: {err}")
    except Exception as e:
        logging.error(f"Error procesando mensaje: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def main():
    # Verificar Mosquitto (solo informativo)
    verify_mosquitto()
    
    # Crear/verificar tabla MySQL
    create_table()
    
    # Configurar cliente MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_CONFIG['host'], MQTT_CONFIG['port'], MQTT_CONFIG['keepalive'])
        logging.info(f"Conectando a broker MQTT en {MQTT_CONFIG['host']}:{MQTT_CONFIG['port']}")
        
        # Iniciar loop en segundo plano
        client.loop_start()
        
        logging.info(f"Servicio iniciado. Escuchando en tópico: {MQTT_CONFIG['topic']}")
        logging.info("Presiona Ctrl+C para detener...")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("Deteniendo servicio...")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        logging.error(f"Error en cliente MQTT: {e}")

if __name__ == "__main__":
    main()
