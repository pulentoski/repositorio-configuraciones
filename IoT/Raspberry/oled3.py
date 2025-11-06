from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont
import time
import psutil
import socket

# Configuración del dispositivo OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Cargar una fuente más grande para el texto
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = 14  # Tamaño de fuente para el texto
font = ImageFont.truetype(font_path, font_size)

# Cargar una fuente más grande para el emoticón (si es compatible)
try:
    emoji_font_path = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
    emoji_font = ImageFont.truetype(emoji_font_path, 40)  # Fuente grande para los rayos
except:
    emoji_font = ImageFont.truetype(font_path, 40)  # Usar la fuente predeterminada si no se encuentra

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
    return psutil.cpu_percent(interval=None)

def get_ram_usage():
    """Obtiene el porcentaje de uso de la RAM."""
    return psutil.virtual_memory().percent

def draw_centered_text(draw, text, y_offset, font, fill="white"):
    """Dibuja texto centrado en la pantalla."""
    text_width = draw.textlength(text, font=font)  # Obtener el ancho del texto
    x = (device.width - text_width) // 2  # Calcular la posición X para centrar
    draw.text((x, y_offset), text, font=font, fill=fill)

def draw_centered_emoji(draw, emoji, y_offset, font, fill="white"):
    """Dibuja un emoticón centrado en la pantalla."""
    text_width = draw.textlength(emoji, font=font)  # Obtener el ancho del emoticón
    x = (device.width - text_width) // 2  # Calcular la posición X para centrar
    draw.text((x, y_offset), emoji, font=font, fill=fill)

try:
    counter = 0
    while True:
        if counter % 2 == 0:
            # Obtener la IP, el uso de la CPU y el uso de la RAM
            ip_address = get_ip_address('eth0')  # Cambia 'eth0' por 'wlan0' si usas Wi-Fi
            cpu_usage = get_cpu_usage()
            ram_usage = get_ram_usage()

            # Mostrar la información en la pantalla OLED
            with canvas(device) as draw:
                draw_centered_text(draw, f"IP: {ip_address}", 0, font)
                draw_centered_text(draw, f"CPU: {cpu_usage}%", 20, font)
                draw_centered_text(draw, f"RAM: {ram_usage}%", 40, font)
            
            # Esperar 7 segundos antes de la siguiente actualización
            time.sleep(7)
        else:
            # Mostrar dos rayos grandes y centrados
            with canvas(device) as draw:
                # Centrar verticalmente los rayos
                draw_centered_emoji(draw, "☠︎☢☢☠", (device.height - 40) // 2, emoji_font)  # Emoji centrado
            
            # Esperar 3 segundos antes de la siguiente actualización
            time.sleep(3)

        # Incrementar el contador
        counter += 1
except KeyboardInterrupt:
    print("Script detenido manualmente.")
except Exception as e:
    print(f"Error: {e}")
