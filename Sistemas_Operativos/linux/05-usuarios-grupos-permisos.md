# 05 — Usuarios, grupos y permisos

> El control de acceso es la primera línea de seguridad de cualquier sistema. Saber gestionar usuarios, grupos y permisos correctamente evita brechas graves.

---

## Usuarios

```bash
# Ver usuarios
cat /etc/passwd             # Lista de todos los usuarios del sistema
id usuario                  # UID, GID y grupos de un usuario
whoami                      # Usuario actual
who                         # Usuarios conectados ahora
last                        # Historial de logins
lastlog                     # Último login de cada usuario

# Crear usuario
useradd -m -s /bin/bash usuario         # Crear con home y shell
useradd -m -G sudo,docker usuario       # Crear y agregar a grupos
adduser usuario                         # Versión interactiva (Debian/Ubuntu)

# Modificar usuario
usermod -aG docker usuario              # Agregar a grupo (sin quitar de otros)
usermod -s /bin/bash usuario            # Cambiar shell
usermod -l nuevo_nombre viejo_nombre    # Renombrar usuario
usermod -L usuario                      # Bloquear cuenta
usermod -U usuario                      # Desbloquear cuenta
usermod -e 2025-12-31 usuario           # Fecha de expiración

# Eliminar usuario
userdel usuario                         # Eliminar usuario (conserva home)
userdel -r usuario                      # Eliminar usuario y su directorio home
```

---

## Contraseñas

```bash
passwd usuario              # Cambiar contraseña de usuario
passwd -l usuario           # Bloquear contraseña (lock)
passwd -u usuario           # Desbloquear contraseña
passwd -e usuario           # Forzar cambio en próximo login
chage -l usuario            # Ver política de expiración de contraseña
chage -M 90 usuario         # Contraseña expira en 90 días
chage -E 2025-12-31 usuario # Cuenta expira en fecha
```

---

## Grupos

```bash
cat /etc/group              # Lista de grupos
groups usuario              # Grupos a los que pertenece un usuario
groupadd nombre_grupo       # Crear grupo
groupdel nombre_grupo       # Eliminar grupo
groupmod -n nuevo viejo     # Renombrar grupo
gpasswd -a usuario grupo    # Agregar usuario al grupo
gpasswd -d usuario grupo    # Quitar usuario del grupo
newgrp nombre_grupo         # Cambiar grupo activo en la sesión
```

---

## Permisos básicos (rwx)

```bash
ls -la                      # Ver permisos de archivos y directorios
```

### Estructura de permisos
```
-rwxr-xr--  1  usuario  grupo  tamaño  fecha  archivo
│└──┬──┘└──┬──┘└──┬──┘
│   │      │      └─ Otros (others)
│   │      └─────── Grupo
│   └────────────── Dueño (owner)
└────────────────── Tipo: - archivo, d directorio, l symlink
```

### Cambiar permisos

```bash
# Modo simbólico
chmod u+x archivo           # Agregar ejecución al dueño
chmod g-w archivo           # Quitar escritura al grupo
chmod o=r archivo           # Otros solo lectura
chmod a+x archivo           # Todos pueden ejecutar
chmod ug+rw archivo         # Dueño y grupo pueden leer y escribir

# Modo octal
chmod 755 archivo           # rwxr-xr-x
chmod 644 archivo           # rw-r--r--
chmod 600 archivo           # rw------- (privado)
chmod 777 archivo           # rwxrwxrwx (peligroso, evitar)
chmod -R 755 /directorio    # Recursivo

# Tabla de valores octal
# 4 = leer (r)
# 2 = escribir (w)
# 1 = ejecutar (x)
# Ejemplos: 7=rwx, 6=rw-, 5=r-x, 4=r--, 0=---
```

---

## Cambiar dueño y grupo

```bash
chown usuario archivo                   # Cambiar dueño
chown usuario:grupo archivo             # Cambiar dueño y grupo
chown :grupo archivo                    # Solo cambiar grupo
chown -R usuario:grupo /directorio      # Recursivo
chgrp grupo archivo                     # Cambiar solo el grupo
```

---

## Permisos especiales

```bash
# SUID (Set User ID) — ejecuta con permisos del dueño
chmod u+s archivo
chmod 4755 archivo          # Octal con SUID

# SGID (Set Group ID) — en dirs: archivos heredan el grupo
chmod g+s directorio
chmod 2755 directorio

# Sticky bit — en dirs: solo el dueño puede borrar sus archivos
chmod +t /directorio
chmod 1777 /tmp             # Ejemplo clásico

# Ver permisos especiales
ls -la /tmp                 # drwxrwxrwt (la 't' es sticky bit)
find / -perm /4000 2>/dev/null   # Buscar archivos con SUID
```

---

## sudo

```bash
sudo comando                # Ejecutar comando como root
sudo -i                     # Shell interactivo como root
sudo -u otro_usuario cmd    # Ejecutar como otro usuario
sudo -l                     # Ver qué puede hacer el usuario con sudo
visudo                      # Editar /etc/sudoers de forma segura
```

### Ejemplos en /etc/sudoers

```bash
# Acceso completo a root
usuario ALL=(ALL:ALL) ALL

# Sin pedir contraseña
usuario ALL=(ALL) NOPASSWD: ALL

# Solo ciertos comandos
usuario ALL=(ALL) /bin/systemctl restart nginx, /bin/journalctl
```

---

## ACL — Listas de Control de Acceso

Para permisos más granulares que los básicos rwx:

```bash
# Requiere filesystem montado con acl (por defecto en ext4 moderno)
getfacl archivo             # Ver ACL de un archivo
setfacl -m u:usuario:rw archivo      # Dar lectura/escritura a usuario específico
setfacl -m g:grupo:r archivo         # Dar lectura a grupo específico
setfacl -m o::- archivo             # Quitar permisos a otros
setfacl -x u:usuario archivo         # Eliminar ACL de un usuario
setfacl -b archivo                   # Eliminar todas las ACL
setfacl -R -m u:usuario:rX /dir     # Recursivo
```

---

## Casos de uso reales

**Crear usuario de servicio (sin login, sin home):**
```bash
useradd -r -s /usr/sbin/nologin -M app_user
```

**Agregar usuario al grupo sudo:**
```bash
usermod -aG sudo usuario
```

**Dar acceso a un archivo solo a un usuario específico sin tocar los permisos del dueño:**
```bash
setfacl -m u:invitado:r archivo.conf
```

**Ver quién tiene acceso a un directorio:**
```bash
ls -la /ruta
getfacl /ruta
```

---

## Troubleshooting común

| Problema | Comando |
|---|---|
| "Permission denied" | `ls -la archivo` y verificar permisos |
| sudo no funciona | `groups usuario` — verificar que esté en sudo/wheel |
| Necesito editar /etc/sudoers | Siempre usar `visudo` |
| Archivo pertenece a usuario eliminado | `find / -nouser 2>/dev/null` |
| Cambio de grupo no toma efecto | Cerrar sesión y volver a entrar, o `newgrp` |
