#!/usr/bin/env python3
"""
Script simple para Zabbix Docker + GNS3
Uso: python3 zabbix.py
"""
import subprocess
import os

print("[+] Sistema: Linux")
print("\n" + "="*60)
print(" ZABBIX DOCKER - CONSTRUYENDO CONTENEDOR ÚNICO ")
print("="*60)

try:
    print("\n[+] Compilando imagen...")
    subprocess.run("docker build -t zabbix-server:v1 .", shell=True, check=True)
    
    print("[+] Exportando para GNS3...")
    subprocess.run("docker save -o zabbix-server.tar zabbix-server:v1", shell=True, check=True)
    
    print("\n" + "="*60)
    print(" ✅ ¡CONSTRUCCIÓN COMPLETADA! ")
    print("="*60)
    print(f"\n📦 Archivo: {os.path.abspath('zabbix-server.tar')}")
    print("\n📋 PRÓXIMOS PASOS:")
    print("  1. GNS3 → Edit → Preferences → Docker Containers → New")
    print("  2. Import image file → zabbix-server.tar")
    print("  3. Nombre: Zabbix-Server")
    print("  4. Finish")
    print("\n🌐 Web: http://localhost")
    print("👤 Usuario: Admin / zabbix")
    
except Exception as e:
    print(f"\n[X] Error: {e}")
