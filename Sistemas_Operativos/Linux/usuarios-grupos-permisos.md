Guía Práctica: Gestión de Usuarios, Grupos y Permisos en Linux

Esta guía te enseñará a manejar usuarios, grupos y permisos en un sistema Linux. Aprenderás a crear y eliminar usuarios y grupos, asignar contraseñas, 
gestionar membresías y configurar permisos avanzados para archivos y carpetas. Al final, hay un ejercicio práctico para aplicar lo aprendido.

# 1. Gestión de Usuarios

## 1.1. Crear un usuario

    sudo adduser nombre_usuario

Ejemplo:

    sudo adduser juan

Se crea un directorio /home/nombre_usuario y se asignan configuraciones básicas.

## 1.2. Eliminar un usuario

    sudo deluser nombre_usuario

Para borrar también su directorio /home:

    sudo deluser --remove-home nombre_usuario

## 1.3. Cambiar contraseña de un usuario

    sudo passwd nombre_usuario

Ejemplo:

    sudo passwd juan

- El sistema pedirá ingresar y confirmar la nueva contraseña.

# 2. Gestión de Grupos
## 2.1. Crear un grupo

    sudo groupadd nombre_grupo

Ejemplo:

    sudo groupadd desarrolladores

## 2.2. Eliminar un grupo

    sudo groupdel nombre_grupo

Ejemplo:

    sudo groupdel desarrolladores

## 2.3. Agregar un usuario a un grupo

    sudo usermod -aG nombre_grupo nombre_usuario

-aG asegura que el usuario no sea removido de otros grupos.

Ejemplo:
    
    sudo usermod -aG desarrolladores juan

## 2.4. Quitar un usuario de un grupo

    sudo deluser nombre_usuario nombre_grupo

Ejemplo:
    
    sudo deluser juan desarrolladores

## 2.5. Ver grupos de un usuario

groups nombre_usuario

Ejemplo:
    
    groups juan

# 3. Gestión de Permisos
3.1. Permisos básicos en archivos/carpetas

    Lectura (r) → 4

    Escritura (w) → 2

    Ejecución (x) → 1

Cambiar permisos con chmod


chmod permisos archivo_o_carpeta

Ejemplo 1 (Dar todos los permisos al dueño, solo lectura al grupo y nada a otros):

    chmod 750 archivo.txt

 - 7 (dueño: rwx), 5 (grupo: r-x), 0 (otros: ---).

Cambiar dueño y grupo con chown

    sudo chown usuario:grupo archivo_o_carpeta

Ejemplo:

    sudo chown juan:desarrolladores proyecto/

# 4. Permisos Avanzados
## 4.1. Restringir acceso a un archivo a un solo usuario

Quitar permisos a grupo y otros:

    chmod 700 archivo.txt

- Solo el dueño (juan) puede leer, escribir y ejecutar.

## 4.2. Restringir acceso a una carpeta a un grupo específico

Asignar el grupo a la carpeta:

    sudo chown :desarrolladores /ruta/carpeta

Quitar permisos a otros:

    chmod 770 /ruta/carpeta

Solo el dueño y el grupo desarrolladores tienen acceso.
