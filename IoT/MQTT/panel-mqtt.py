import paho.mqtt.client as mqtt
import threading
import time
from colorama import Fore, Style, init

# Inicializar colorama para habilitar colores en la terminal
init(autoreset=True)

# Configuración del broker MQTT
BROKER = "192.168.0.17"
PORT = 1883
TOPIC_COMMANDS = "comandos"
TOPIC_RESULTS = "resultados"

# Indicador de conexión
connected = False

# Callback para conexión
def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print(f"{Fore.GREEN}[Conectado] Conectado al broker MQTT")
        connected = True
        # Suscribirse al tópico de resultados
        client.subscribe(TOPIC_RESULTS)
    else:
        print(f"{Fore.RED}[Error] Error al conectar (código {rc})")

# Callback para mensajes recibidos
def on_message(client, userdata, msg):
    print(f"\n{Style.BRIGHT}[Respuesta]{Style.RESET_ALL} {msg.payload.decode('utf-8')}")

# Función para mantener la conexión MQTT en un hilo
def mqtt_loop(client):
    client.loop_start()
    while True:
        if not connected:
            print(f"{Fore.YELLOW}[Reconexión] Intentando reconectar...")
        time.sleep(5)

# Configurar cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker
client.connect(BROKER, PORT)

# Iniciar el hilo para el loop MQTT
threading.Thread(target=mqtt_loop, daemon=True, args=(client,)).start()

# Shell interactiva
print(f"{Style.BRIGHT}Bienvenido a la shell MQTT. Escribe '{Fore.CYAN}exit{Style.RESET_ALL}' para salir.")
while True:
    if connected:
        command = input(f"{Fore.CYAN}> {Style.RESET_ALL}")
        if command.lower() == "exit":
            print(f"{Fore.BLUE}[Saliendo] Cerrando la conexión...")
            client.loop_stop()
            client.disconnect()
            break
        # Publicar el comando en el tópico correspondiente
        client.publish(TOPIC_COMMANDS, command)
    else:
        print(f"{Fore.YELLOW}[Esperando] Conexión al broker...")
        time.sleep(1)
