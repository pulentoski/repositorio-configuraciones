#!/usr/bin/env python3
"""
Script de automatización para TACACS+ Docker + GNS3
Genera Dockerfile, entrypoint.sh, tac_plus.conf
Compila la imagen y exporta tacacs-server.tar
"""
import os
import subprocess
import sys

DOCKERFILE_CONTENT = """FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar herramientas de compilación y dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    bison \
    flex \
    libpam0g-dev \
    libwrap0-dev \
    curl \
    iproute2 \
    iputils-ping \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Descargar y compilar TACACS+ desde fuente oficial (Shrubbery Networks)
WORKDIR /tmp
RUN curl -sL ftp://ftp.shrubbery.net/pub/tac_plus/tacacs-F4.0.4.28.tar.gz -o tacacs.tar.gz || \
    curl -sL https://ftp.gwdg.de/pub/misc/shrubbery/tac_plus/tacacs-F4.0.4.28.tar.gz -o tacacs.tar.gz && \
    tar -xzf tacacs.tar.gz && \
    cd tacacs-F4.0.4.28 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd / && rm -rf /tmp/tacacs*

RUN mkdir -p /etc/tacacs+

COPY tac_plus.conf /etc/tacacs+/tac_plus.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 49

ENTRYPOINT ["/entrypoint.sh"]
"""

ENTRYPOINT_CONTENT = """#!/bin/bash
echo "Verificando sintaxis de TACACS+..."
/usr/local/sbin/tac_plus -P /etc/tacacs+/tac_plus.conf

if [ $? -eq 0 ]; then
    echo "Sintaxis correcta. Iniciando servicio TACACS+ en puerto 49..."
    /usr/local/sbin/tac_plus -G -c /etc/tacacs+/tac_plus.conf &
    TACACS_PID=$!
    echo "Servicio TACACS+ iniciado. PID: $TACACS_PID"
    echo "Contenedor listo. Puedes ejecutar comandos en esta consola."
    bash
else
    echo "ERROR: La configuración de TACACS+ tiene fallos de sintaxis."
    echo "Manteniendo contenedor abierto para inspeccionar..."
    bash
fi
"""

TAC_CONF_CONTENT = """accounting file = /var/log/tac_plus.acct
key = 12345

group = admins {
    default service = permit
    service = exec {
        priv-lvl = 15
    }
}

group = limited {
    default service = deny
    service = exec {
        priv-lvl = 1
    }
    cmd = show {
        permit ip
        permit interface
        permit running-config
        deny .*
    }
}

user = diego {
    member = admins
    login = cleartext diego
}

user = seba {
    member = limited
    login = cleartext seba
}
"""

def create_files():
    print("[+] Generando carpeta y archivos de configuración...")
    os.makedirs("tacacs-gns3-lab", exist_ok=True)
    os.chdir("tacacs-gns3-lab")

    with open("Dockerfile", "w", encoding="utf-8", newline='\n') as f:
        f.write(DOCKERFILE_CONTENT)

    with open("entrypoint.sh", "w", encoding="utf-8", newline='\n') as f:
        f.write(ENTRYPOINT_CONTENT)
    
    os.chmod("entrypoint.sh", 0o755)

    with open("tac_plus.conf", "w", encoding="utf-8", newline='\n') as f:
        f.write(TAC_CONF_CONTENT)
        
    print("[✓] Archivos creados exitosamente.")

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\n[X] Error al ejecutar: {cmd}")
        sys.exit(1)

def fix_permissions():
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        print(f"[+] Ajustando permisos para el usuario: {sudo_user}...")
        subprocess.run(f"chown -R {sudo_user}:{sudo_user} .", shell=True)

def main():
    create_files()

    print("\n[+] Construyendo la imagen Docker (Compilando TACACS+ desde fuente)...")
    run_command("docker build -t tacacs-server:v1 .")

    print("\n[+] Exportando imagen 'tacacs-server.tar' para GNS3...")
    run_command("docker save -o tacacs-server.tar tacacs-server:v1")

    fix_permissions()

    print("\n" + "="*50)
    print(" ¡PROCESO COMPLETADO EXITOSAMENTE! ")
    print("="*50)
    print("✓ Archivo 'tacacs-server.tar' generado en:")
    print(f"  {os.path.abspath('tacacs-server.tar')}")
    print("\n📋 Próximos pasos:")
    print("  1. Importa en GNS3: Edit → Preferences → Docker Containers → New")
    print("  2. Selecciona 'Import an image file' → tacacs-server.tar")
    print("  3. Nombre: TACACS_Server")
    print("  4. Arrastra a la topología y abre la consola")

if __name__ == "__main__":
    main()
