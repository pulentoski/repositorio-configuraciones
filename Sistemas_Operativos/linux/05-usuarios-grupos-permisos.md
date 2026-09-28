# 05 — Usuarios, grupos y permisos

> El control de acceso es la primera línea de seguridad de cualquier sistema. Saber gestionar usuarios, grupos y permisos correctamente evita brechas graves.

---

## Usuarios

> **Qué es:** Cada persona o servicio que usa el sistema tiene una cuenta con un identificador único (UID).
>
> **Para qué sirve:** Identificar quién hace qué: base de la trazabilidad y del control de acceso (NIST AC-2).

```bash
# Ver usuarios
cat /etc/passwd             # Lista de todos los usuarios del sistema
id usuario                  # UID, GID y grupos de un usuario
whoami                      # Usuario actual
who                         # Usuarios conectados ahora
last                        # Historial de logins
lastlog                     # Último login de cada usuario
sudo lastb                  # Historial de logins fallidos

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

> **Qué es:** Credencial secreta asociada a la cuenta, con reglas de expiración y bloqueo.
>
> **Para qué sirve:** Controlar la vida útil de las credenciales y bloquear cuentas que ya no se usan.

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

> **Qué es:** Conjunto de usuarios que comparten permisos. Se asignan permisos al grupo, no a cada persona.
>
> **Para qué sirve:** Implementar control de acceso basado en roles (RBAC): el grupo representa el rol (sysops, auditores).

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

> **Qué es:** Cada archivo define qué pueden hacer su dueño, su grupo y el resto: leer (r), escribir (w) y ejecutar (x).
>
> **Para qué sirve:** Evitar que usuarios lean o modifiquen archivos que no les corresponden.

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

> **Qué es:** Todo archivo pertenece a un usuario y a un grupo, y los permisos se evalúan contra ellos.
>
> **Para qué sirve:** Asignar correctamente la propiedad de archivos de aplicaciones, respaldos o datos compartidos.

```bash
chown usuario archivo                   # Cambiar dueño
chown usuario:grupo archivo             # Cambiar dueño y grupo
chown :grupo archivo                    # Solo cambiar grupo
chown -R usuario:grupo /directorio      # Recursivo
chgrp grupo archivo                     # Cambiar solo el grupo
```

---

## Permisos especiales

> **Qué es:** SUID, SGID y sticky bit modifican cómo se ejecutan o borran archivos.
>
> **Para qué sirve:** Entenderlos es clave en seguridad: un binario con SUID mal configurado permite escalar a root.

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

> **Qué es:** Herramienta que permite ejecutar comandos con privilegios de otro usuario (normalmente root), según reglas definidas en sudoers.
>
> **Para qué sirve:** Aplicar mínimo privilegio: cada usuario recibe solo los comandos que necesita, y todo uso queda registrado en auth.log (NIST AC-6).

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

# Solo ciertos comandos (sin paginador, para evitar escape a shell)
usuario ALL=(ALL) /usr/bin/systemctl restart nginx, /usr/bin/journalctl --no-pager -u nginx
```

### Permisos por grupo con /etc/sudoers.d/ (RBAC)

Buena práctica: no editar `/etc/sudoers` directamente, sino crear un archivo por rol dentro de `/etc/sudoers.d/`. El `%` indica que la regla aplica a un grupo.

```bash
sudo visudo -f /etc/sudoers.d/sysops       # Crear/editar el archivo del rol
sudo visudo -f /etc/sudoers.d/auditores
```

```bash
# /etc/sudoers.d/sysops — administración completa
%sysops    ALL=(ALL:ALL) ALL

# /etc/sudoers.d/auditores — solo lectura de registros, comandos exactos
%auditores ALL=(root) /usr/bin/tail -n 200 /var/log/auth.log, /usr/bin/journalctl --no-pager -u ssh, /usr/bin/lastb
```

```bash
sudo -l -U usr_auditor                     # Ver qué puede ejecutar un usuario
sudo visudo -c                             # Validar la sintaxis de todos los archivos
```

> Los usuarios nuevos necesitan contraseña para usar sudo aunque SSH entre con llave: `sudo passwd usr_admin`.

**Alternativa sin sudo para auditores:** en Ubuntu, el grupo `adm` puede leer `/var/log/auth.log` sin privilegios de root.

```bash
sudo usermod -aG adm usr_auditor
```

### ⚠️ Escape a shell y comodines

Algunos comandos permiten abrir una shell desde dentro. Si se autorizan con sudo, el usuario obtiene root:

| Comando | Escape |
|---|---|
| `less`, `more`, `man` | `!sh` |
| `vi`, `vim`, `nano` | `:!sh` / `^R^X` |
| `journalctl` (sin `--no-pager`) | abre `less` → `!sh` |
| `find` | `-exec /bin/sh \;` |

Los comodines también son peligrosos: `journalctl --no-pager *` permitiría `--vacuum-time=1s`, que **borra los logs**, rompiendo la separación de funciones.

Regla: autorizar comandos exactos, con sus argumentos, sin paginador y sin `*`. Referencia: [GTFOBins](https://gtfobins.github.io/)

---

## ACL — Listas de Control de Acceso

> **Qué es:** Permisos adicionales que se asignan a usuarios o grupos específicos, más allá de dueño/grupo/otros.
>
> **Para qué sirve:** Dar acceso puntual a alguien sin cambiar el dueño ni abrir el archivo a todos.

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
