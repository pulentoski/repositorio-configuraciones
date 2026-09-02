# 🐳 Guía de Implementación TACACS+ en Docker + GNS3

## Paso 1: Crear la carpeta del proyecto

### 🐧 En Linux (Terminal)

```bash
mkdir tacacs-gns3-lab
cd tacacs-gns3-lab
```

### 🪟 En Windows (PowerShell)

```powershell
mkdir tacacs-gns3-lab
cd tacacs-gns3-lab
```

---

## Paso 2: Crear los 3 Archivos de Configuración

### Archivo 1: `Dockerfile`

#### 🐧 Linux (usando editor Nano)

1. Ejecuta:

```bash
nano Dockerfile
```

2. Pega el código de abajo.
3. Guarda con `Ctrl + O`.
4. Presiona `Enter`.
5. Sal con `Ctrl + X`.

#### 🪟 Windows (usando Bloc de Notas desde PowerShell)

1. Ejecuta:

```powershell
notepad Dockerfile
```

2. Cuando pregunte si deseas crear un archivo nuevo, haz clic en **Sí**.
3. Pega el contenido y guarda.

### Contenido de `Dockerfile`

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tacacs+ \
    iproute2 \
    iputils-ping \
    nano \
    && rm -rf /var/lib/apt/lists/*

COPY tac_plus.conf /etc/tacacs+/tac_plus.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 49

ENTRYPOINT ["/entrypoint.sh"]
```

---

### Archivo 2: `entrypoint.sh`

#### 🐧 Linux

```bash
nano entrypoint.sh
```

#### 🪟 Windows

```powershell
notepad entrypoint.sh
```

### Contenido de `entrypoint.sh`

```bash
#!/bin/bash
echo "Verificando sintaxis de TACACS+..."
tac_plus -P /etc/tacacs+/tac_plus.conf

if [ $? -eq 0 ]; then
    echo "Sintaxis correcta. Iniciando servicio TACACS+..."
    exec tac_plus -G -c /etc/tacacs+/tac_plus.conf
else
    echo "ERROR en la configuración de TACACS+."
    exit 1
fi
```

---

### Archivo 3: `tac_plus.conf`

#### 🐧 Linux

```bash
nano tac_plus.conf
```

#### 🪟 Windows

```powershell
notepad tac_plus.conf
```

### Contenido de `tac_plus.conf`

```text
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

Una vez guardados los 3 archivos en la misma carpeta, ejecuta los siguientes comandos en la consola:

| Acción                        | Comando en Linux                                         | Comando en Windows (PowerShell)                     |
| ----------------------------- | -------------------------------------------------------- | --------------------------------------------------- |
| **1. Construir la Imagen**    | `sudo docker build -t tacacs-server:v1 .`                | `docker build -t tacacs-server:v1 .`                |
| **2. Exportar a formato TAR** | `sudo docker save -o tacacs-server.tar tacacs-server:v1` | `docker save -o tacacs-server.tar tacacs-server:v1` |

Al finalizar, se debe haber creado el archivo:

```text
tacacs-server.tar
```

Este archivo contiene la imagen Docker que posteriormente será importada en GNS3.

---

# Paso 4: Cargar en GNS3

1. En la aplicación GNS3 ve a:

**Edit → Preferences → Docker Containers → New**

2. Marca la opción **Import an image file** y selecciona el archivo generado:

```text
tacacs-server.tar
```

3. Asigna de nombre:

```text
TACACS_Server
```

4. Deja **1 interfaz** y finaliza la importación.

5. Arrastra el nodo `TACACS_Server` a la topología de GNS3.

6. Conecta el contenedor al switch correspondiente.

---

## 🌐 Configuración de la dirección IP

El contenedor necesita una dirección IP para comunicarse con los routers y switches Cisco.

Existen dos alternativas:

### Opción A — 🔒 IP fija

Para el laboratorio TACACS+ se recomienda utilizar una IP fija, ya que los routers y switches deben conocer la dirección del servidor TACACS+.

En este ejemplo:

```text
IP:       192.168.1.100
Máscara:  255.255.255.0
Gateway:  192.168.1.1
```

En **Edit config** del contenedor se puede utilizar:

```text
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
```

La dirección del servidor TACACS+ será:

```text
192.168.1.100
```

Los equipos Cisco deberán utilizar posteriormente esta dirección para comunicarse con TACACS+.

---

### Opción B — 🌐 IP automática mediante DHCP

Si la red de GNS3 dispone de un **servidor DHCP**, el contenedor puede obtener automáticamente su configuración de red.

En **Edit config** se puede utilizar:

```text
auto eth0
iface eth0 inet dhcp
```

En este caso, el servidor DHCP entregará automáticamente:

```text
IP
Máscara
Gateway
```

La dirección obtenida puede comprobarse posteriormente desde el contenedor.

Por ejemplo:

```bash
ip addr
```

o:

```bash
ip -4 addr show eth0
```

También se puede comprobar la ruta:

```bash
ip route
```

### ⚠️ Consideración importante

Si se utiliza DHCP, **la dirección IP del servidor TACACS+ puede cambiar**.

Esto puede generar un problema porque los routers y switches Cisco deben saber dónde se encuentra el servidor TACACS+.

Por esta razón, para el laboratorio se recomienda:

```text
                    TACACS+
                       │
                       │
                IP conocida
                       │
                       ▼
                192.168.1.100
```

La alternativa ideal es utilizar una **reserva DHCP**, de manera que el servidor obtenga automáticamente su configuración pero reciba siempre la misma dirección IP.

---

## 🧪 Comprobar la conectividad

Una vez configurada la dirección IP, comprobar desde el contenedor:

```bash
ip addr
```

Verificar que `eth0` tenga una dirección IPv4.

Luego comprobar el gateway:

```bash
ping 192.168.1.1
```

Y posteriormente comprobar la conectividad con un equipo Cisco de la red:

```bash
ping 192.168.1.X
```

Finalmente, desde el equipo Cisco se debe comprobar la conectividad hacia el servidor TACACS+:

```cisco
ping 192.168.1.100
```

> 🎓 **Regla fundamental del laboratorio:** primero debe existir conectividad IP entre Cisco y el servidor. Después se configura y prueba TACACS+.

---

## 📌 Configuración recomendada para este laboratorio

Para mantener una topología sencilla y reproducible, se recomienda utilizar:

```text
TACACS+ Server
IP:       192.168.1.100
Mask:     255.255.255.0
Gateway:  192.168.1.1
Port:     TCP/49
```

De esta forma, todos los routers y switches Cisco podrán utilizar:

```text
192.168.1.100
```

como dirección del servidor TACACS+.
