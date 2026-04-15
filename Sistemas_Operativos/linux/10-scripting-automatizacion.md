# 10 — Scripting y automatización en Bash

> Automatizar tareas repetitivas es lo que multiplica la eficiencia de un sysadmin. Bash está en todos los servidores Linux y dominar sus fundamentos es indispensable.

---

## Estructura básica de un script

```bash
#!/bin/bash
# Descripción: Qué hace este script
# Autor: tu_nombre
# Fecha: 2025-01-01

set -e          # Salir si cualquier comando falla
set -u          # Error si se usa variable no definida
set -o pipefail # El pipe falla si cualquier parte falla

echo "Script iniciado"
```

---

## Variables

```bash
# Declaración
NOMBRE="servidor01"
PUERTO=8080
RUTA="/var/log"

# Uso
echo "Servidor: $NOMBRE"
echo "Puerto: ${PUERTO}"          # Llaves para mayor claridad

# Variables especiales
echo $0         # Nombre del script
echo $1 $2      # Argumentos posicionales
echo $#         # Número de argumentos
echo $@         # Todos los argumentos
echo $?         # Código de salida del último comando (0=éxito)
echo $$         # PID del script actual

# Variables de solo lectura
readonly VERSION="1.0"

# Sustitución de comandos
FECHA=$(date +%Y-%m-%d)
USUARIOS=$(cat /etc/passwd | wc -l)
IP=$(hostname -I | awk '{print $1}')
```

---

## Condicionales

```bash
# if básico
if [ $? -eq 0 ]; then
    echo "Comando exitoso"
fi

# if-else
if [ -f /etc/nginx/nginx.conf ]; then
    echo "nginx está instalado"
else
    echo "nginx no encontrado"
fi

# if-elif-else
if [ "$1" == "start" ]; then
    systemctl start nginx
elif [ "$1" == "stop" ]; then
    systemctl stop nginx
else
    echo "Uso: $0 {start|stop}"
    exit 1
fi

# Operadores de comparación numérica
# -eq  igual
# -ne  distinto
# -lt  menor
# -le  menor o igual
# -gt  mayor
# -ge  mayor o igual

# Operadores de cadenas
# ==   igual
# !=   distinto
# -z   cadena vacía
# -n   cadena no vacía

# Operadores de archivos
# -f   es archivo regular
# -d   es directorio
# -e   existe
# -r   tiene permiso de lectura
# -w   tiene permiso de escritura
# -x   tiene permiso de ejecución
# -s   archivo no vacío
```

---

## Bucles

```bash
# for clásico
for i in 1 2 3 4 5; do
    echo "Iteración $i"
done

# for con rango
for i in {1..10}; do
    echo $i
done

# for sobre archivos
for archivo in /var/log/*.log; do
    echo "Procesando: $archivo"
    wc -l "$archivo"
done

# for sobre lista de servidores
SERVIDORES="10.0.0.1 10.0.0.2 10.0.0.3"
for HOST in $SERVIDORES; do
    echo "Verificando $HOST..."
    ping -c 1 "$HOST" > /dev/null && echo "$HOST: OK" || echo "$HOST: FALLA"
done

# while
CONTADOR=0
while [ $CONTADOR -lt 5 ]; do
    echo "Contador: $CONTADOR"
    ((CONTADOR++))
done

# while leyendo un archivo línea a línea
while IFS= read -r linea; do
    echo "Línea: $linea"
done < /etc/hosts

# until (contrario a while)
until [ -f /tmp/archivo_listo ]; do
    echo "Esperando..."
    sleep 5
done
```

---

## Funciones

```bash
# Definición
saludar() {
    local nombre=$1         # Variable local
    echo "Hola, $nombre"
    return 0                # Código de salida
}

# Llamada
saludar "mundo"

# Función con verificación de argumentos
verificar_servicio() {
    local servicio=$1

    if [ -z "$servicio" ]; then
        echo "Error: se requiere nombre del servicio"
        return 1
    fi

    if systemctl is-active --quiet "$servicio"; then
        echo "$servicio: activo"
        return 0
    else
        echo "$servicio: inactivo"
        return 1
    fi
}

verificar_servicio nginx
verificar_servicio postgresql
```

---

## Manejo de errores

```bash
# Verificar código de salida
comando
if [ $? -ne 0 ]; then
    echo "Error al ejecutar comando"
    exit 1
fi

# Forma más concisa
comando || { echo "Error"; exit 1; }

# Trap para limpiar al salir o ante errores
cleanup() {
    echo "Limpiando..."
    rm -f /tmp/archivo_temporal
}
trap cleanup EXIT          # Ejecuta cleanup al salir
trap cleanup ERR           # Ejecuta cleanup ante cualquier error

# Logger para registrar errores
log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a /var/log/mi_script.log >&2
}
log_info() {
    echo "[INFO]  $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a /var/log/mi_script.log
}
```

---

## Scripts de monitoreo útiles

### Verificar servicios críticos

```bash
#!/bin/bash
SERVICIOS="nginx postgresql redis"
ALERTA_EMAIL="admin@miempresa.com"

for SERVICIO in $SERVICIOS; do
    if ! systemctl is-active --quiet "$SERVICIO"; then
        echo "ALERTA: $SERVICIO no está activo" | mail -s "Servicio caído: $SERVICIO" "$ALERTA_EMAIL"
        systemctl start "$SERVICIO"
    fi
done
```

### Monitor de uso de disco

```bash
#!/bin/bash
UMBRAL=80

df -h | grep '^/dev' | while read linea; do
    USO=$(echo "$linea" | awk '{print $5}' | tr -d '%')
    MONTAJE=$(echo "$linea" | awk '{print $6}')

    if [ "$USO" -gt "$UMBRAL" ]; then
        echo "ALERTA: $MONTAJE al ${USO}% de uso"
    fi
done
```

### Verificar conectividad de hosts

```bash
#!/bin/bash
HOSTS_FILE="/etc/monitoreo/hosts.txt"
LOG="/var/log/conectividad.log"

while IFS= read -r host; do
    if ping -c 1 -W 2 "$host" > /dev/null 2>&1; then
        echo "$(date): $host - OK" >> "$LOG"
    else
        echo "$(date): $host - FALLA" >> "$LOG"
    fi
done < "$HOSTS_FILE"
```

---

## Buenas prácticas

```bash
# 1. Siempre validar argumentos
if [ $# -lt 1 ]; then
    echo "Uso: $0 <argumento>"
    exit 1
fi

# 2. Usar comillas en variables (evitar word splitting)
archivo="mi archivo con espacios.txt"
cat "$archivo"          # Correcto
cat $archivo            # Incorrecto: falla con espacios

# 3. Usar $() en vez de backticks
FECHA=$(date +%Y-%m-%d)     # Moderno, anidable
FECHA=`date +%Y-%m-%d`      # Antiguo, evitar

# 4. Probar scripts con bash -n (syntax check) y bash -x (debug)
bash -n script.sh       # Verificar sintaxis sin ejecutar
bash -x script.sh       # Ejecutar con trace de cada comando

# 5. Nunca hardcodear contraseñas
# Mal:
DB_PASS="micontraseña123"
# Bien:
DB_PASS=$(cat /etc/secretos/db_password)
# O con variables de entorno:
DB_PASS="${DB_PASSWORD:?Variable DB_PASSWORD no definida}"
```

---

## Troubleshooting común

| Problema | Solución |
|---|---|
| "Permission denied" al ejecutar | `chmod +x script.sh` |
| Script falla silenciosamente | Agregar `set -e` y `set -x` para debug |
| Variable vacía cuando no debería | `echo ${VAR:-"valor_default"}` |
| Cron no ejecuta el script | Verificar PATH en crontab: `PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin` |
| Loop infinito | `Ctrl+C` o `kill PID` |
