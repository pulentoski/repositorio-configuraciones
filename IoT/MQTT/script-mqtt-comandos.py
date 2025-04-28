#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import subprocess
import os
from datetime import datetime

# Configuración
BROKER_RECEPTOR = "192.168.0.17"
BROKER_EMISOR = "192.168.0.17"
PUERTO = 1883
TOPICO_COMANDOS = "comandos"
TOPICO_RESULTADOS = "resultados"
CLIENT_ID = "ejecutor_comandos_v6"
DIR_ACTUAL = os.getcwd()  # Mantiene el directorio actual

def ejecutar_comando(comando):
    """
    Ejecuta un comando en el sistema. Si el comando es `cd`, cambia el directorio actual.
    Devuelve el resultado del comando y el directorio actual.
    """
    global DIR_ACTUAL

    # Comando para cambiar de directorio
    if comando.startswith('cd '):
        try:
            nuevo_dir = comando[3:].strip()
            if nuevo_dir == "..":
                DIR_ACTUAL = os.path.dirname(DIR_ACTUAL) or "/"
            else:
                os.chdir(nuevo_dir)
                DIR_ACTUAL = os.getcwd()
            return f"$: pwd: {DIR_ACTUAL}"
        except Exception as e:
            return f"$: Error al cambiar de directorio: {str(e)}"

    # Ejecutar otros comandos
    try:
        proceso = subprocess.run(
            comando,
            shell=True,
            cwd=DIR_ACTUAL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        resultado = proceso.stdout if proceso.returncode == 0 else proceso.stderr
        return f"$: {resultado.strip()}"
    except subprocess.TimeoutExpired:
        return "$: Error: Tiempo de espera agotado"
    except Exception as e:
        return f"$: Error al ejecutar el comando: {str(e)}"

def publicar_resultado(mensaje):
    """
    Publica el mensaje resultante en el topic de resultados.
    """
    try:
        pub_client = mqtt.Client(client_id=f"{CLIENT_ID}_pub")
        pub_client.connect(BROKER_EMISOR, PUERTO)
        pub_client.publish(TOPICO_RESULTADOS, mensaje)
        pub_client.disconnect()
    except Exception as e:
        print(f"Error al publicar resultado: {str(e)}")

def on_message(client, userdata, msg):
    """
    Callback ejecutado al recibir un mensaje.
    """
    comando = msg.payload.decode('utf-8').strip()
    if not comando:
        return

    print(f"Comando recibido: {comando}")
    resultado = ejecutar_comando(comando)
    print(resultado)
    publicar_resultado(resultado)

def configurar_cliente_receptor():
    """
    Configura y devuelve el cliente MQTT receptor.
    """
    cliente = mqtt.Client(client_id=f"{CLIENT_ID}_sub")
    cliente.on_message = on_message
    return cliente

def main():
    """
    Función principal para conectar al broker MQTT y escuchar comandos.
    """
    try:
        receptor = configurar_cliente_receptor()
        print(f"Conectando a {BROKER_RECEPTOR}...")
        receptor.connect(BROKER_RECEPTOR, PUERTO)
        receptor.subscribe(TOPICO_COMANDOS)
        print(f"Escuchando en '{TOPICO_COMANDOS}'. Directorio actual: {DIR_ACTUAL}")
        receptor.loop_forever()
    except KeyboardInterrupt:
        print("Desconectando...")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
