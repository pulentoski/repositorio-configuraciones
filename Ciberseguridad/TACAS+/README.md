# 🐳 Guía de Implementación TACACS+ en Docker + GNS3

Esta guía detalla el procedimiento paso a paso para construir e implementar un servidor **TACACS+** sobre Docker y exportarlo como un nodo portable para **GNS3**.

---

## ⚠️ Nota Importante

El paquete `tacacs+` fue descontinuado en los repositorios oficiales de Ubuntu/Debian a partir de las versiones recientes. Por esta razón, esta guía **compila TACACS+ desde el código fuente oficial de Shrubbery Networks** dentro del contenedor Docker, garantizando compatibilidad universal en cualquier distribución de Linux.

---

## 🚀 Inicio Rápido (Automático)

Si tienes Python 3 instalado, simplemente ejecuta:

```bash
python3 setup_tacacs.py
```

El script genera automáticamente:
- Carpeta `tacacs-gns3-lab`
- Dockerfile, entrypoint.sh, tac_plus.conf
- Compila la imagen Docker
- Exporta `tacacs-server.tar` para GNS3

---

## Paso 1: Crear la carpeta del proyecto

Abre la consola de comandos en tu sistema operativo y ejecuta los siguientes comandos para preparar el directorio de trabajo:

### 🐧 En Linux (Terminal):

```bash
mkdir tacacs-gns3-lab
cd tacacs-gns3-lab
```

### 🪟 En Windows (PowerShell):

```powershell
mkdir tacacs-gns3-lab
cd tacacs-gns3-lab
```

---

## Paso 2: Crear los 3 Archivos de Configuración

Dentro de la carpeta `tacacs-gns3-lab`, debes crear los tres archivos base del proyecto:

### Archivo 1: Dockerfile

🐧 **Linux (usando Nano):**

```bash
nano Dockerfile
```

(Pega el contenido, guarda con Ctrl + O, presiona Enter y sal con Ctrl + X)

🪟 **Windows (usando Bloc de Notas):**

```powershell
notepad Dockerfile
```

**Contenido de Dockerfile:**

```dockerfile
FROM debian:bullseye-slim

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
```

---

### Archivo 2: entrypoint.sh

🐧 **Linux:** 
```bash
nano entrypoint.sh
```

🪟 **Windows:** 
```powershell
notepad entrypoint.sh
```

**Contenido de entrypoint.sh:**

```bash
#!/bin/bash
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
```

---

### Archivo 3: tac_plus.conf

🐧 **Linux:** 
```bash
nano tac_plus.conf
```

🪟 **Windows:** 
```powershell
notepad tac_plus.conf
```

**Contenido de tac_plus.conf:**

```plaintext
accounting file = /var/log/tac_plus.acct
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
```

---

## Paso 3: Construir y Exportar el Contenedor

Una vez guardados los 3 archivos en la misma carpeta, ejecuta los siguientes comandos según tu sistema operativo:

| Acción | Comando en Linux | Comando en Windows (PowerShell) |
|--------|------------------|--------------------------------|
| 1. Construir la Imagen | `sudo docker build -t tacacs-server:v1 .` | `docker build -t tacacs-server:v1 .` |
| 2. Exportar a formato TAR | `sudo docker save -o tacacs-server.tar tacacs-server:v1` | `docker save -o tacacs-server.tar tacacs-server:v1` |

Al finalizar el proceso, se habrá generado el archivo comprimido:

```
tacacs-server.tar
```

**Tiempo estimado:** ~2-3 minutos (depende de tu conexión, se descarga y compila TACACS+)

---

## Paso 4: Cargar en GNS3

En la aplicación GNS3 ve a: **Edit → Preferences → Docker Containers → New**.

1. ✅ Marca la opción **Import an image file** y selecciona el archivo generado: `tacacs-server.tar`

2. 📝 Asigna de nombre: `TACACS_Server`

3. 🔌 Deja **1 interfaz** asignada y finaliza la importación.

4. 🖱️ Arrastra el nodo **TACACS_Server** a la área de trabajo de GNS3 y conéctalo al switch correspondiente.

---

## 🌐 Configuración de la Dirección IP

El contenedor requiere parámetros de red para comunicarse con los routers y switches Cisco. Puedes optar por cualquiera de las dos alternativas según la necesidad de la topología:

### Opción A — 🔒 IP Fija (Recomendada)

Para laboratorios de TACACS+ se aconseja utilizar direccionamiento estático, ya que los dispositivos de red deben conocer la IP exacta del servidor AAA.

**Parámetros de ejemplo:**

- **IP:** 192.168.1.100
- **Máscara:** 255.255.255.0
- **Gateway:** 192.168.1.1

En la opción **Edit config** del nodo en GNS3, define la siguiente interfaz:

```bash
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
```

---

### Opción B — 🌐 IP Automática mediante DHCP

Si la topología de GNS3 integra un servidor DHCP activo, el contenedor puede obtener sus parámetros de red de forma dinámica.

En **Edit config** del nodo en GNS3, reemplaza la configuración por:

```bash
auto eth0
iface eth0 inet dhcp
```

Para verificar la IP obtenida por el contenedor, ejecuta en la consola del nodo:

```bash
ip addr
```

O bien:

```bash
ip -4 addr show eth0
```

Para comprobar las rutas activas:

```bash
ip route
```

#### ⚠️ Consideración Importante:

Si utilizas DHCP, la dirección IP asignada al contenedor **podría cambiar al reiniciar la topología**, provocando que los routers o switches pierdan contacto con el servidor TACACS+. 

Si se requiere DHCP, se recomienda **configurar una reserva de dirección MAC** en el servidor DHCP para garantizar que mantenga siempre la IP `192.168.1.100`.

---

## 🧪 Comprobación de Conectividad

Una vez configurada la dirección IP, es fundamental verificar la conectividad bidireccional entre el servidor TACACS+ y los equipos Cisco antes de realizar pruebas de autenticación.

### En el servidor TACACS+:

Verifica que TACACS+ está corriendo:
```bash
ps aux | grep tac_plus
```

Verifica la dirección asignada:
```bash
ip addr
```

Valida la conectividad hacia el Gateway:
```bash
ping 192.168.1.1
```

Comprueba la conectividad hacia el router/switch Cisco:
```bash
ping 192.168.1.X
```

### En el equipo Cisco:

Verifica el alcance al servidor de autenticación:
```bash
ping 192.168.1.100
```

---

## 🎓 Regla Fundamental

**Debe existir conectividad IP bidireccional mediante ping entre el equipo Cisco y el servidor TACACS+ antes de proceder a la prueba y envío de paquetes de autenticación/autorización.**

---

## 📌 Resumen de Parámetros del Laboratorio

Para mantener una topología sencilla, consistente y reproducible, se recomienda utilizar el siguiente esquema básico:

| Parámetro | Valor |
|-----------|-------|
| **Nombre de Nodo** | TACACS_Server |
| **IP** | 192.168.1.100 |
| **Máscara** | 255.255.255.0 |
| **Gateway** | 192.168.1.1 |
| **Puerto del Servicio** | TCP/49 |
| **Llave TACACS+** | 12345 |

---

## 📝 Configuración en Cisco IOS (Ejemplo Básico)

Una vez que el contenedor esté corriendo y la conectividad IP esté verificada, configura un router o switch Cisco de la siguiente forma:

```cisco
aaa new-model
aaa authentication login default group tacacs+ local
aaa authorization exec default group tacacs+ local
aaa accounting exec default start-stop group tacacs+

tacacs-server host 192.168.1.100 key 12345
tacacs-server timeout 5
```

Ejemplo de login:
```cisco
Router# telnet 192.168.1.100
Trying 192.168.1.100...
Connected to 192.168.1.100.
Escape character is '^]'.

Username: diego
Password: diego

Router>
```

---

## 🐛 Troubleshooting

### La consola se cierra inmediatamente

**Causa:** El entrypoint.sh antiguo finalizaba cuando terminaba `tac_plus`.

**Solución:** Asegúrate de usar el `entrypoint.sh` correcto que inicia `tac_plus` en background y mantiene `bash` abierto.

---

### El contenedor no inicia

Verifica en la consola de GNS3:
```bash
ps aux | grep tac_plus
# Si no aparece nada, revisa:
/usr/local/sbin/tac_plus -P /etc/tacacs+/tac_plus.conf
```

---

### Error de sintaxis en tac_plus.conf

Verifica el archivo:
```bash
cat /etc/tacacs+/tac_plus.conf
```

O reconstruye la imagen si modificaste el archivo.

---

### Sin conectividad IP

Verifica la configuración:
```bash
ip addr
ip route
ping 192.168.1.1
```

---

## ✅ Checklist Final

- [ ] Descargaste o clonaste el repositorio
- [ ] Creaste los 3 archivos (Dockerfile, entrypoint.sh, tac_plus.conf)
- [ ] Ejecutaste `docker build` y generaste la imagen
- [ ] Generaste el archivo `tacacs-server.tar`
- [ ] Importaste la imagen en GNS3
- [ ] Configuraste la IP del nodo TACACS_Server (fija o DHCP)
- [ ] Abriste la consola y se mantiene abierta
- [ ] Verificaste que `tac_plus` está corriendo con `ps aux | grep tac_plus`
- [ ] Verificaste conectividad ping bidireccional
- [ ] Configuraste los equipos Cisco con comandos `tacacs-server host`

---

## 📄 Licencia

Este proyecto es de código abierto bajo licencia **MIT**.

**Última actualización:** 2026
**Estado:** ✅ Testeado y funcional en GNS3
