Guía Completa
Requisitos previos

 Hardware:

Raspberry Pi (o cualquier dispositivo compatible con Linux).

Pantalla OLED compatible con I2C (por ejemplo, SSD1306).

Conexiones I2C correctamente cableadas (SDA, SCL, GND, VCC).

Software:

Sistema operativo basado en Linux (por ejemplo, Raspberry Pi OS).

Python 3 instalado.

Biblioteca luma.oled para controlar la pantalla OLED.

Biblioteca psutil para obtener el uso de la CPU.

Paso 1: Configurar el entorno virtual
Navegar al directorio del proyecto:


    cd /home/daniel/Documents

Crear el entorno virtual:

    python3 -m venv oled_env

Activar el entorno virtual:

    source oled_env/bin/activate
Después de activar el entorno virtual, verás (oled_env) en la terminal.

Paso 2: Instalar dependencias
Instalar las bibliotecas necesarias:

    pip install luma.oled psutil

Generar el archivo requirements.txt:

    pip freeze > requirements.txt

Este archivo contiene todas las dependencias instaladas y facilita su instalación en el futuro.

Paso 3: Crear el script codigo.py
Crear el archivo codigo.py:

    nano /home/daniel/Documents/codigo.py

Pegar el siguiente código:

    python
    Copy

    from luma.oled.device import ssd1306
    from luma.core.interface.serial import i2c
    from luma.core.render import canvas
    import time
    import psutil
    import socket

    # Configuración del dispositivo OLED
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    def get_ip_address(interface='eth0'):
        """Obtiene la dirección IP de la interfaz especificada."""
        try:
            interfaces = psutil.net_if_addrs()
            if interface in interfaces:
                for addr in interfaces[interface]:
                    if addr.family == socket.AF_INET:  # IPv4
                        return addr.address
            return "Sin IP"
        except Exception as e:
            return "Error IP"

    def get_cpu_usage():
        """Obtiene el porcentaje de uso de la CPU."""
        return psutil.cpu_percent(interval=1)

    try:
        while True:
            # Obtener la IP y el uso de la CPU
            ip_address = get_ip_address('eth0')  # Cambia 'eth0' por 'wlan0' si usas Wi-Fi
            cpu_usage = get_cpu_usage()

            # Mostrar la información en la pantalla OLED
            with canvas(device) as draw:
                draw.text((0, 0), f"IP: {ip_address}", fill="white")
                draw.text((0, 20), f"CPU: {cpu_usage}%", fill="white")

            # Esperar 2 segundos antes de la siguiente actualización
            time.sleep(2)
    except KeyboardInterrupt:
        print("Script detenido manualmente.")
    except Exception as e:
        print(f"Error: {e}")

Guardar y cerrar el archivo:

- Presiona Ctrl + O para guardar.
- Presiona Ctrl + X para salir.

Paso 4: Crear el archivo de servicio systemd
Crear el archivo de servicio:

    sudo nano /etc/systemd/system/run_oled.service

Pegar el siguiente contenido:


    [Unit]
    Description=OLED script to display CPU and IP
    After=network.target

    [Service]
    Type=simple
    ExecStart=/home/daniel/Documents/oled_env/bin/python /home/daniel/Documents/codigo.py
    WorkingDirectory=/home/daniel/Documents
    User=daniel
    Group=daniel
    Restart=on-failure
    RestartSec=3

    [Install]
    WantedBy=multi-user.target

Guardar y cerrar el archivo:
- Presiona Ctrl + O para guardar.
- Presiona Ctrl + X para salir.

Paso 5: Habilitar y ejecutar el servicio
Recargar systemd para aplicar los cambios:

    sudo systemctl daemon-reload

Habilitar el servicio para que se inicie automáticamente al arrancar:

    sudo systemctl enable run_oled.service
Iniciar el servicio manualmente:

    sudo systemctl start run_oled.service

Verificar el estado del servicio:

    sudo systemctl status run_oled.service

Si todo está bien, deberías ver active (running).

Paso 6: Solución de problemas
1. La pantalla OLED no muestra nada
Verifica las conexiones I2C:

Asegúrate de que los cables estén bien conectados (SDA, SCL, GND, VCC).

Usa i2cdetect para confirmar que la pantalla está conectada:

        sudo i2cdetect -y 1

Deberías ver la dirección 0x3C (o 0x3D, dependiendo de la pantalla).

Verifica el voltaje:
Asegúrate de que la pantalla esté conectada a 3.3V, no a 5V.

2. El servicio no se inicia

        sudo journalctl -u run_oled.service
 Busca mensajes de error que indiquen qué está fallando.

Verifica las rutas:

- Asegúrate de que las rutas en ExecStart y WorkingDirectory sean correctas.

3. La dirección IP es incorrecta

Cambia la interfaz de red:
Si usas Wi-Fi, cambia eth0 por wlan0 en el script:

        ip_address = get_ip_address('wlan0')

4. La pantalla parpadea

    Reduce la frecuencia de actualización:

        Aumenta el tiempo de espera en el bucle principal:
        python
        Copy

        time.sleep(5)  # Cambia 5 por el número de segundos que desees.

Resumen

- Configura el entorno virtual e instala las dependencias.
- Crea el script codigo.py para mostrar la IP y el uso de la CPU en la pantalla OLED.

- Configura el servicio systemd para ejecuta
- r el script automáticamente al iniciar el sistema.

    Habilita y verifica el servicio.

    Soluciona problemas comunes si es necesario.
