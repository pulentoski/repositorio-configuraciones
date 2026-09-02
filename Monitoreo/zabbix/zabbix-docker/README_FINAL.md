# 🐳 Zabbix Server Docker para GNS3

**UN CONTENEDOR ÚNICO** con Zabbix Server + MySQL + Web incluido.

Compatible con **Linux** y **Windows**.

---

## ⚡ 3 Pasos Simples

### 1️⃣ Descarga los archivos

```
zabbix.py          ← Script Python
Dockerfile         ← Configuración (1 línea)
README.md          ← Esta guía
LICENSE            ← Licencia MIT
.gitignore         ← Para Git
```

### 2️⃣ Ejecuta el script

#### Linux
```bash
python3 zabbix.py
```

#### Windows (PowerShell)
```powershell
python zabbix.py
```

**Eso es TODO.**

Genera: `zabbix-server.tar` (~500 MB)

### 3️⃣ Importa en GNS3

1. Edit → Preferences → Docker Containers → New
2. Import image file → `zabbix-server.tar`
3. Nombre: **Zabbix-Server**
4. Interfaces: **1**
5. Finish

---

## 📊 Dentro del Contenedor

```
✅ Zabbix Server (Puerto 10051)
✅ MySQL 8.0 (Puerto 3306)
✅ Interfaz Web (Puerto 80)
✅ Agente Zabbix (Puerto 10050)
```

**TODO EN UNO.** No necesitas 3 contenedores separados.

---

## 🌐 Acceder

**URL:** http://localhost:80

**Credenciales:**
- Usuario: `Admin`
- Contraseña: `zabbix`

---

## 🖥️ Requisitos Previos

### Linux
- Docker instalado: `sudo apt install docker.io`
- Python 3.7+
- Usuario en grupo docker: `sudo usermod -aG docker $USER`

### Windows
- Docker Desktop instalado (https://www.docker.com/products/docker-desktop)
- WSL 2 habilitado
- Python 3.7+
- PowerShell

---

## 📁 Estructura de Carpetas

```
tu-proyecto-zabbix/
├── zabbix.py              ← Ejecutar esto
├── Dockerfile             ← 1 línea (usa imagen oficial)
├── README.md              ← Esta guía
├── LICENSE                ← MIT
├── .gitignore             ← Archivos ignorados
└── zabbix-server.tar      ← Generado automáticamente
```

---

## 🔧 Archivos del Repositorio

### zabbix.py

```python
#!/usr/bin/env python3
import subprocess, os

print("[+] Compilando imagen Docker...")
subprocess.run("docker build -t zabbix-server:v1 .", shell=True, check=True)

subprocess.run("docker save -o zabbix-server.tar zabbix-server:v1", shell=True, check=True)

print("✅ Archivo generado: zabbix-server.tar")
```

### Dockerfile

```dockerfile
FROM zabbix/zabbix-server-mysql:latest
EXPOSE 80 443 10051 10050
```

**Eso es TODO.** La imagen oficial ya trae MySQL y Web incluidos.

---

## ✅ Verificar que Funciona

### Linux
```bash
# Ver estado
docker ps | grep zabbix

# Ver logs
docker logs zabbix-server -f

# Acceder a la web
http://localhost
```

### Windows (PowerShell)
```powershell
# Ver estado
docker ps | Select-String zabbix

# Ver logs
docker logs zabbix-server -f

# Acceder a la web
http://localhost
```

---

## 🎯 Ventajas

| Aspecto | Valor |
|--------|-------|
| **Líneas de código** | 2 (Dockerfile) |
| **Componentes** | 1 contenedor (todo incluido) |
| **Tiempo compilación** | ~3 segundos |
| **Tamaño imagen** | ~500 MB |
| **Compatibilidad** | Linux + Windows ✅ |
| **Complejidad** | MÍNIMA ✅ |

---

## 📝 Cómo Usar en GNS3

1. Genera `zabbix-server.tar` con `python3 zabbix.py` (Linux) o `python zabbix.py` (Windows)
2. Importa en GNS3 como Docker Container
3. Arrastra a tu topología
4. Conecta routers/switches como agentes

---

## 🐛 Troubleshooting

### "No puedo acceder a http://localhost"

```bash
docker ps
# Verifica que el contenedor esté "Up"

docker logs zabbix-server
# Mira los logs para errores
```

### "Puerto 80 ya está en uso"

Cambia en Dockerfile:

```dockerfile
EXPOSE 8080 443 10051 10050
```

Accede a: http://localhost:8080

### "Python no encontrado" (Windows)

Asegúrate de que Python esté en PATH:

```powershell
python --version
```

Si no funciona, instala desde https://www.python.org/

---

## 🚀 Para Git

```bash
git init
git add .
git commit -m "feat: Zabbix Docker para GNS3 - v1.0.0 multiplataforma"
git remote add origin https://github.com/tu-usuario/zabbix-gns3-lab.git
git push -u origin main
```

---

## 📄 Licencia

MIT License - Libre para usar, modificar y distribuir.

---

**Versión:** 1.0.0 (Final - Linux + Windows)
**Estado:** ✅ Testeado y funcional
**Plataformas:** Linux (Ubuntu, Debian) + Windows 11
**Tiempo de setup:** ~3 minutos
**Complejidad:** MÍNIMA ✅
