#!/usr/bin/env python3
import paho.mqtt.client as mqtt                                                                                                                              
import subprocess                                                                                                                                            
import os                                                                                                                                                    
                                                                                                                                                             
# Configuración MQTT                                                                                                                                         
BROKER = "0.0.0.0"                                                                                                                                           
PORT = 1883                                                                                                                                                  
USER = "daniel1"                                                                                                                                             
PASS = "daniel1"                                                                                                                                             
TOPIC_COMANDOS = "comandos"                                                                                                                                  
TOPIC_RESULTADOS = "resultados"                                                                                                                              
                                                                                                                                                             
# Variable global para mantener el directorio actual                                                                                                         
directorio_actual = os.getcwd()                                                                                                                              
                                                                                                                                                             
def ejecutar_comando(comando):                                                                                                                               
    """Ejecuta comandos y mantiene el estado del directorio actual."""                                                                                       
    global directorio_actual                                                                                                                                 
    try:                                                                                                                                                     
        # Manejar el comando 'cd'                                                                                                                            
        if comando.strip().startswith("cd"):                                                                                                                 
            partes = comando.split(maxsplit=1)                                                                                                               
            if len(partes) == 1 or partes[1] == "~":  # 'cd' o 'cd ~'                                                                                        
                directorio_actual = os.path.expanduser("~")                                                                                                  
            else:                                                                                                                                            
                # Resolver rutas relativas y absolutas                                                                                                       
                nuevo_directorio = os.path.abspath(                                                                                                          
                    os.path.join(directorio_actual, partes[1])                                                                                               
                )                                                                                                                                            
                if os.path.isdir(nuevo_directorio):                                                                                                          
                    directorio_actual = nuevo_directorio                                                                                                     
                else:                                                                                                                                        
                    return f"Error: El directorio '{partes[1]}' no existe"                                                                                   
            return f"Directorio cambiado a: {directorio_actual}"                                                                                             
                                                                                                                                                             
        # Comando para mostrar el directorio actual                                                                                                          
        if comando.strip() == "pwd":                                                                                                                         
            return f"Directorio actual: {directorio_actual}"                                                                                                 
                                                                                                                                                             
        # Ejecutar otros comandos en el contexto del directorio actual                                                                                       
        proceso = subprocess.run(                                                                                                                            
            comando,                                                                                                                                         
            shell=True,                                                                                                                                      
            executable="/bin/bash",                                                                                                                          
            cwd=directorio_actual,                                                                                                                           
            stdout=subprocess.PIPE,                                                                                                                          
            stderr=subprocess.PIPE,                                                                                                                          
            text=True,                                                                                                                                       
        )                                                                                                                                                    
        return proceso.stdout if proceso.stdout else proceso.stderr                                                                                          
    except Exception as e:                                                                                                                                   
        return f"Error: {str(e)}"                                                                                                                            
                                                                                                                                                             
def on_message(client, userdata, msg):                                                                                                                       
    """Callback para manejar mensajes MQTT."""                                                                                                               
    comando = msg.payload.decode()                                                                                                                           
    resultado = ejecutar_comando(comando)                                                                                                                    
    client.publish(TOPIC_RESULTADOS, resultado)                                                                                                              
                                                                                                                                                             
# Configuración del cliente MQTT                                                                                                                             
client = mqtt.Client()                                                                                                                                       
client.username_pw_set(USER, PASS)                                                                                                                           
client.on_message = on_message                                                                                                                               
client.connect(BROKER, PORT)                                                                                                                                 
client.subscribe(TOPIC_COMANDOS)                                                                                                                             
print("✅ Servidor MQTT listo (soporte completo para comandos 'cd')")                                                                                        
client.loop_forever()      
