#!/usr/bin/env python3
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import psutil
import time
import subprocess
import meshtastic.serial_interface
from datetime import datetime

class OLEDMonitor:
    def __init__(self):
        # Hardware OLED
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial)
        self.font = ImageFont.load_default()
        
        # Estado del sistema
        self.mesh_interface = None
        self.last_error = ""

    def get_interface_ip(self, interface):
        """Obtiene IP de interfaz sin depender de netifaces"""
        try:
            cmd = f"ip -4 addr show {interface} | grep inet | awk '{{print $2}}' | cut -d/ -f1"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip() or "Sin IP"
        except:
            return "Error"

    def connect_meshtastic(self):
        """Conexión con manejo de errores"""
        try:
            if self.mesh_interface:
                self.mesh_interface.close()
            self.mesh_interface = meshtastic.serial_interface.SerialInterface(
                devPath="/dev/ttyUSB0",
                noProto=True  # Modo no bloqueante
            )
            self.last_error = ""
            return True
        except Exception as e:
            self.last_error = f"{type(e).__name__}:{str(e)[:15]}"
            return False

    def update_display(self):
        """Dibuja en la pantalla OLED"""
        with canvas(self.device) as draw:
            # Línea 1: Estado Meshtastic
            status = "✅" if self.mesh_interface else f"❌{self.last_error}"
            nodes = len(self.mesh_interface.nodes) if self.mesh_interface else 0
            draw.text((0, 0), f"MESH:{status} NODOS:{nodes}", font=self.font, fill="white")
            
            # Línea 2: Ethernet
            draw.text((0, 12), f"ETH:{self.get_interface_ip('eth0')}", font=self.font, fill="white")
            
            # Línea 3: WiFi
            draw.text((0, 24), f"WLAN:{self.get_interface_ip('wlan0')}", font=self.font, fill="white")
            
            # Línea 4: Sistema
            draw.text((0, 36), 
                     f"CPU:{psutil.cpu_percent()}% RAM:{psutil.virtual_memory().percent}%", 
                     font=self.font, fill="white")
            
            # Línea 5: Hora
            draw.text((0, 48), datetime.now().strftime("%H:%M:%S"), font=self.font, fill="white")

    def run(self):
        """Bucle principal"""
        while True:
            if not self.mesh_interface:
                self.connect_meshtastic()
            self.update_display()
            time.sleep(5)

if __name__ == "__main__":
    monitor = OLEDMonitor()
    try:
        monitor.run()
    except KeyboardInterrupt:
        if monitor.mesh_interface:
            monitor.mesh_interface.close()
        monitor.device.clear()
