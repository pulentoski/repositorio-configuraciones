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
