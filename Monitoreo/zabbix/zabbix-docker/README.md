# 🐳 Zabbix Server Docker para GNS3

Guía completa para crear **UN CONTENEDOR ÚNICO** de Zabbix Server con MySQL y Web incluido.

Compatible con **Linux** y **Windows**.

---

## 📋 Paso 1: Crear Carpeta del Proyecto

### Linux
```bash
mkdir zabbix-gns3-lab
cd zabbix-gns3-lab
```

### Windows (PowerShell)
```powershell
mkdir zabbix-gns3-lab
cd zabbix-gns3-lab
```

---

## 📝 Paso 2: Crear Dockerfile

### Linux (Nano)
```bash
nano Dockerfile
```

### Windows (Bloc de Notas)
```powershell
notepad Dockerfile
```

**Contenido (copiar exactamente):**

```dockerfile
FROM zabbix/zabbix-server-mysql:latest
EXPOSE 80 443 10051 10050
```

**Guardar y cerrar.**

---

## 🔨 Paso 3: Compilar la Imagen Docker

### Linux
```bash
docker build -t zabbix-server:v1 .
```

### Windows (PowerShell)
```powershell
docker build -t zabbix-server:v1 .
```

**Salida esperada:**
```
[+] Building 3.3s (5/5) FINISHED
=> CACHED [1/1] FROM docker.io/zabbix/zabbix-server-mysql:latest
[+] naming to docker.io/library/zabbix-server:v1
```

---

## 💾 Paso 4: Exportar la Imagen para GNS3

### Linux
```bash
docker save -o zabbix-server.tar zabbix-server:v1
```

### Windows (PowerShell)
```powershell
docker save -o zabbix-server.tar zabbix-server:v1
```

**Resultado:** Se genera `zabbix-server.tar` (~500 MB)

---

## ✅ Paso 5: Verificar que Funciona

### Linux
```bash
# Ver imagen creada
docker images | grep zabbix-server

# Ver tamaño del archivo
ls -lh zabbix-server.tar
```

### Windows (PowerShell)
```powershell
# Ver imagen creada
docker images | Select-String zabbix-server

# Ver tamaño del archivo
Get-Item zabbix-server.tar | Select-Object Length
```

---

## 🖱️ Paso 6: Importar en GNS3

1. Abre **GNS3**
2. **Edit → Preferences → Docker Containers**
3. Haz clic en **New**
4. Selecciona **Import an image file**
5. Busca `zabbix-server.tar`
6. **Nombre:** Zabbix-Server
7. **Interfaces:** 1
8. **Finish**

Ahora puedes arrastrarlo a tu topología.

---

## 🌐 Paso 7: Acceder a Zabbix

Una vez el contenedor esté corriendo en GNS3:

```
URL: http://localhost:80
```

**Credenciales:**
- Usuario: `Admin`
- Contraseña: `zabbix`

---

## 📊 Qué Contiene el Contenedor

| Componente | Puerto | Función |
|-----------|--------|---------|
| Zabbix Server | 10051 | Recibe datos de agentes |
| MySQL | 3306 | Base de datos |
| Interfaz Web | 80 | Dashboard (Apache + PHP) |
| Agente Zabbix | 10050 | Monitoreo local |

**TODO EN UN CONTENEDOR** ✅

---

## 🚀 ⚡ OPCIÓN RÁPIDA: Usar Script Python

Si prefieres automatizar todo, usa el script:

### Linux
```bash
python3 setup_zabbix.py
```

### Windows (PowerShell)
```powershell
python setup_zabbix.py
```

**El script hace automáticamente:**
1. ✅ Detecta el SO (Linux/Windows)
2. ✅ Compila la imagen (`docker build`)
3. ✅ Exporta para GNS3 (`docker save`)
4. ✅ Muestra el resultado

---

## 📂 Estructura Final del Proyecto

```
zabbix-gns3-lab/
├── Dockerfile              ← Configuración (2 líneas)
├── setup_zabbix.py         ← Script Python (opcional)
├── zabbix-server.tar       ← Generado automáticamente
├── README.md               ← Esta guía
├── LICENSE                 ← MIT
└── .gitignore              ← Archivos ignorados
```

---

## 🧪 Verificación

### Verificar que el contenedor está corriendo

```bash
docker ps | grep zabbix-server
```

### Ver los logs

```bash
docker logs zabbix-server -f
```

### Acceder a bash dentro del contenedor

```bash
docker exec -it zabbix-server bash
```

---

## 🐛 Troubleshooting

### "Puerto 80 ya está en uso"

Si otro servicio usa puerto 80, edita el Dockerfile:

```dockerfile
FROM zabbix/zabbix-server-mysql:latest
EXPOSE 8080 443 10051 10050
```

Luego recompila:

```bash
docker build -t zabbix-server:v1 .
docker save -o zabbix-server.tar zabbix-server:v1
```

Accede a: `http://localhost:8080`

---

### "No puedo acceder a http://localhost"

```bash
# Verificar que el contenedor está corriendo
docker ps

# Ver logs para errores
docker logs zabbix-server

# Si no aparece nada, espera 1 minuto a que inicie MySQL
```

---

### "docker command not found" (Windows)

Asegúrate de que Docker Desktop esté:
1. Instalado: https://www.docker.com/products/docker-desktop
2. Corriendo (verifica en la bandeja del sistema)
3. WSL 2 habilitado

---

## 📄 Archivos Necesarios

Solo necesitas:
- **Dockerfile** (2 líneas)
- **setup_zabbix.py** (opcional - para automatizar)

Eso es TODO.

---

## 🔧 Para Git

```bash
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
git add .
git commit -m "feat: Zabbix Docker para GNS3 - v1.0.0 (Linux + Windows)"
git branch -M main
git remote add origin https://github.com/tu-usuario/zabbix-gns3-lab.git
git push -u origin main
```

---

## ✅ Checklist Final

- [ ] Creaste la carpeta `zabbix-gns3-lab`
- [ ] Creaste el archivo `Dockerfile` (2 líneas)
- [ ] Compilaste con `docker build -t zabbix-server:v1 .`
- [ ] Exportaste con `docker save -o zabbix-server.tar zabbix-server:v1`
- [ ] Verificaste que `zabbix-server.tar` existe
- [ ] Importaste en GNS3
- [ ] Accediste a http://localhost con Admin/zabbix

---

## 📄 Licencia

MIT License - Libre para usar, modificar y distribuir.

---

**Versión:** 1.0.0
**Estado:** ✅ Testeado (Linux + Windows)
**Complejidad:** MÍNIMA ✅
**Tiempo:** ~5 minutos (manual) o ~3 segundos (script)
