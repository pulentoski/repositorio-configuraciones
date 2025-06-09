# Permisos en Linux: Teoría y Práctica
2.1. Representación de permisos

Los permisos se definen para 3 roles:

    Dueño (u): Usuario propietario del archivo/carpeta.

    Grupo (g): Grupo asignado al archivo/carpeta.

    Otros (o): Resto de usuarios.

2.2. Tipos de permisos:
Símbolo	Número	Descripción
r	4	Lectura (read)
w	2	Escritura (write)
x	1	Ejecución (execute)
2.3. Notación octal:

Cada combinación de r-w-x se representa con un dígito octal (0-7):

    7 = 4+2+1 → rwx (Todos los permisos)

    5 = 4+0+1 → r-x (Lectura y ejecución)

    0 = 0+0+0 → --- (Sin permisos)

## Comandos Clave
3.1. chmod (Cambiar permisos)

Sintaxis:
chmod [opciones] permisos archivo_carpeta

Ejemplos:

    chmod 750 /var/www/html      # Dueño:rwx, Grupo:r-x, Otros:---
    chmod u+x script.sh          # Agrega ejecución al dueño

## chown (Cambiar dueño/grupo)

    chown daniel:www-data /var/www/html
