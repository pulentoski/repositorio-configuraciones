import paho.mqtt.client as mqtt
import threading
import time
import sys
import itertools
from colorama import Fore, Style, init
from random import randint

# Inicializar colorama para habilitar colores en la terminal
init(autoreset=True)

# Función para mostrar el banner de bienvenida con animación
def mostrar_banner():
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
  ███╗   ███╗ ██████╗ ████████╗████████╗
  ████╗ ████║██╔═══██╗╚══██╔══╝╚══██╔══╝
  ██╔████╔██║██║   ██║   ██║      ██║   
  ██║╚██╔╝██║██║   ██║   ██║      ██║   
  ██║ ╚═╝ ██║╚██████╔╝   ██║      ██║   
  ╚═╝     ╚═╝ ╚═════╝    ╚═╝      ╚═╝   
{Style.RESET_ALL}
{Fore.YELLOW}Conéctate, envía comandos y hackea el mundo...{Style.RESET_ALL}
"""
    print(banner)
    animar_mosquitos()

# Animación de "mosquitos" (caracteres aleatorios)
def animar_mosquitos():
    mosquitos = ['.', '-', 'o', '*', '+', 'x']
    for _ in range(20):  # Duración de la animación
        fila = ''.join([Fore.GREEN + mosquitos[randint(0, len(mosquitos) - 1)] for _ in range(50)])
        print(fila)
        time.sleep(0.02)
    print("\n" * 2)

# Preguntar la IP del broker, usuario y contraseña
BROKER = input(f"{Fore.GREEN}[Configuración] {Style.RESET_ALL}Por favor, ingresa la IP del broker MQTT: ")
PORT = 1883
USERNAME = input(f"{Fore.GREEN}[Autenticación] {Style.RESET_ALL}Ingresa el nombre de usuario del broker: ")
PASSWORD = input(f"{Fore.GREEN}[Autenticación] {Style.RESET_ALL}Ingresa la contraseña del broker: ")
TOPIC_COMMANDS = "comandos"
TOPIC_RESULTS = "resultados"

# Indicador de conexión
connected = False

# Callback para conexión
def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print(f"{Fore.LIGHTGREEN_EX}[Conectado] Conectado al broker MQTT")
        connected = True
        # Suscribirse al tópico de resultados
        client.subscribe(TOPIC_RESULTS)
    else:
        print(f"{Fore.RED}[Error] Error al conectar (código {rc})")

# Callback para mensajes recibidos
def on_message(client, userdata, msg):
    print(f"\n{Style.BRIGHT}[Respuesta]{Style.RESET_ALL} {Fore.YELLOW}{msg.payload.decode('utf-8')}")

# Función para mantener la conexión MQTT en un hilo
def mqtt_loop(client):
    client.loop_start()
    while True:
        if not connected:
            print(f"{Fore.YELLOW}[Reconexión] Intentando reconectar...")
        time.sleep(5)

# Mostrar el banner de bienvenida
mostrar_banner()

# Configurar cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)  # Configurar usuario y contraseña
client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker
print(f"{Fore.BLUE}[Conectando] {Style.RESET_ALL}Intentando conectar a {BROKER}:{PORT}...")
client.connect(BROKER, PORT)

# Iniciar el hilo para el loop MQTT
threading.Thread(target=mqtt_loop, daemon=True, args=(client,)).start()

# Shell interactiva
print(f"{Style.BRIGHT}Bienvenido a la shell MQTT. Escribe '{Fore.CYAN}exit{Style.RESET_ALL}' para salir.")
while True:
    if connected:
        command = input(f"{Fore.LIGHTCYAN_EX}> {Style.RESET_ALL}")
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
