# 🔐 Administración de TACACS+ con tac_plus-ng

Guía práctica para administrar un servidor TACACS+ (tac_plus-ng) en Ubuntu, desde la operación básica hasta autorización por comandos y auditoría.

> 📌 Requisito previo: tac_plus-ng instalado y routers Cisco con SSH + AAA apuntando al servidor (ver guía de instalación).

---

## 📋 Contenido

- [Conceptos AAA](#-1-conceptos-aaa)
- [Nivel 1 — Operación Básica](#-nivel-1--operación-básica)
- [Nivel 2 — Gestión de Usuarios](#-nivel-2--gestión-de-usuarios)
- [Nivel 3 — Servicio y Logs](#-nivel-3--servicio-y-logs)
- [Nivel 4 — Perfiles y Privilegios](#-nivel-4--perfiles-y-privilegios)
- [Nivel 5 — Autorización por Comandos](#-nivel-5--autorización-por-comandos)
- [Nivel 6 — Grupos y Dispositivos](#-nivel-6--grupos-y-dispositivos)
- [Nivel 7 — Auditoría y Monitoreo](#-nivel-7--auditoría-y-monitoreo)
- [Referencia Rápida](#-referencia-rápida)
- [Ejercicios](#-ejercicios)

---

## 📘 1. Conceptos AAA

| Letra | Significado | Pregunta que responde | En TACACS+ |
|---|---|---|---|
| **A** | Authentication | ¿Quién eres? | Usuario y contraseña |
| **A** | Authorization | ¿Qué puedes hacer? | Nivel de privilegio y comandos permitidos |
| **A** | Accounting | ¿Qué hiciste? | Registro de sesiones y comandos |

TACACS+ separa las tres funciones. Por eso se puede autenticar con TACACS+ y, además, controlar y registrar cada comando.

### Archivos clave

| Ruta | Contenido |
|---|---|
| `/etc/tac_plus-ng/tac_plus-ng.cfg` | Configuración (usuarios, claves, perfiles) |
| `/usr/local/sbin/tac_plus-ng` | Binario del servidor |
| `/var/log/tac_plus-ng/` | Logs |

---

## 🟢 Nivel 1 — Operación Básica

### Ver si el servidor está corriendo

```bash
ps aux | grep tac_plus-ng
ss -tlnp | grep :49
```

### Validar la configuración (siempre antes de reiniciar)

```bash
tac_plus-ng -P /etc/tac_plus-ng/tac_plus-ng.cfg
```

> ✅ Sin salida = configuración válida.
> ⚠️ Si muestra un error, indica la línea. No reinicie hasta corregirlo.

### Iniciar, detener y reiniciar (modo manual)

```bash
tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg &   # iniciar
killall tac_plus-ng                                  # detener
```

Reiniciar = detener + iniciar.

### Estructura mínima del archivo

```
id = spawnd {
    background = no
    listen { port = 49 }
}

id = tac_plus-ng {
    host world {
        address = 0.0.0.0/0
        key = demo
    }

    profile admin {
        script {
            if (service == shell) { permit }
        }
    }

    user test {
        password login = clear testpass
        password pap = login
        profile = admin
    }
}
```

| Bloque | Función |
|---|---|
| `spawnd` | Proceso que escucha en TCP 49 |
| `host` | Qué equipos pueden consultar y con qué clave |
| `profile` | Qué se permite al usuario |
| `user` | Credenciales y perfil asignado |

---

## 🟢 Nivel 2 — Gestión de Usuarios

### 👤 Agregar un usuario

```bash
nano /etc/tac_plus-ng/tac_plus-ng.cfg
```

Dentro de `id = tac_plus-ng { ... }`:

```
    user daniel {
        password login = clear Daniel123
        password pap = login
        profile = admin
    }
```

```bash
tac_plus-ng -P /etc/tac_plus-ng/tac_plus-ng.cfg
killall tac_plus-ng
tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg &
```

### 🔑 Cambiar contraseña

Edite la línea `password login = clear ...` del usuario, valide y reinicie.

### 🗑️ Eliminar usuario

Borre el bloque `user nombre { ... }` completo, valide y reinicie.

### 📃 Listar usuarios

```bash
grep -E "^\s*user " /etc/tac_plus-ng/tac_plus-ng.cfg
```

### 🔒 Contraseñas cifradas (en vez de texto plano)

Genere el hash:

```bash
openssl passwd -6 'Daniel123'
# $6$Xy...$Ab...
```

Úselo en el usuario:

```
    user daniel {
        password login = crypt $6$Xy...$Ab...
        password pap = login
        profile = admin
    }
```

> 💡 Con `crypt`, quien lea el archivo no ve las contraseñas. Es la práctica recomendada.

### Probar desde un cliente

```bash
ssh daniel@10.0.0.1
```

---

## 🟡 Nivel 3 — Servicio y Logs

### ⚙️ Ejecutar como servicio (systemd)

Así el servidor arranca solo y se reinicia si falla.

```bash
nano /etc/systemd/system/tac_plus-ng.service
```

```ini
[Unit]
Description=TACACS+ Server (tac_plus-ng)
After=network-online.target
Wants=network-online.target

[Service]
ExecStartPre=/usr/local/sbin/tac_plus-ng -P /etc/tac_plus-ng/tac_plus-ng.cfg
ExecStart=/usr/local/sbin/tac_plus-ng -f /etc/tac_plus-ng/tac_plus-ng.cfg
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
killall tac_plus-ng
systemctl daemon-reload
systemctl enable --now tac_plus-ng
```

Desde ahora:

```bash
systemctl status tac_plus-ng
systemctl restart tac_plus-ng
systemctl stop tac_plus-ng
journalctl -u tac_plus-ng -f
```

> 💡 `ExecStartPre` valida la configuración antes de iniciar. Si hay un error, el servicio no arranca con una configuración rota.

### 📝 Configurar logs

Dentro de `id = tac_plus-ng { ... }`:

```
    log authc { destination = /var/log/tac_plus-ng/authc.log }
    log authz { destination = /var/log/tac_plus-ng/authz.log }
    log acct  { destination = /var/log/tac_plus-ng/acct.log }

    authentication log = authc
    authorization log = authz
    accounting log = acct
```

| Log | Registra |
|---|---|
| `authc.log` | Logins exitosos y fallidos |
| `authz.log` | Decisiones de permitir o denegar |
| `acct.log` | Inicio y fin de sesión, comandos ejecutados |

```bash
mkdir -p /var/log/tac_plus-ng
systemctl restart tac_plus-ng
```

### Ver actividad

```bash
tail -f /var/log/tac_plus-ng/authc.log            # logins en vivo
grep daniel /var/log/tac_plus-ng/*.log            # todo de un usuario
grep -i fail /var/log/tac_plus-ng/authc.log       # intentos fallidos
```

---

## 🟡 Nivel 4 — Perfiles y Privilegios

Objetivo: que cada usuario entre **directo** con su nivel de privilegio, sin depender de `enable`.

### Servidor: perfiles por nivel

```
    profile admin {
        script {
            if (service == shell) {
                if (cmd == "") {
                    set priv-lvl = 15
                    permit
                }
                permit
            }
        }
    }

    profile soporte {
        script {
            if (service == shell) {
                if (cmd == "") {
                    set priv-lvl = 1
                    permit
                }
                permit
            }
        }
    }

    user daniel {
        password login = clear Daniel123
        password pap = login
        profile = admin
    }

    user alumno {
        password login = clear Alumno123
        password pap = login
        profile = soporte
    }
```

### Router: activar autorización de sesión

```
configure terminal
 aaa authorization exec default group tacacs+ local
end
```

### Resultado

```
ssh daniel@10.0.0.1   →  RT-EDGE#   (nivel 15)
ssh alumno@10.0.0.1   →  RT-EDGE>   (nivel 1)
```

```
show privilege
! Current privilege level is 15
```

---

## 🔴 Nivel 5 — Autorización por Comandos

Objetivo: controlar **qué comandos** puede ejecutar cada usuario.

### Servidor: perfil de solo lectura

```
    profile readonly {
        script {
            if (service == shell) {
                if (cmd == "") {
                    set priv-lvl = 15
                    permit
                }
                if (cmd =~ /^show /) { permit }
                if (cmd =~ /^ping /) { permit }
                if (cmd =~ /^traceroute /) { permit }
                if (cmd =~ /^exit/) { permit }
                deny
            }
        }
    }

    user auditor {
        password login = clear Auditor123
        password pap = login
        profile = readonly
    }
```

> 💡 Recibe nivel 15 para poder usar todos los `show`, pero el servidor deniega cualquier otro comando.

### Router: activar autorización de comandos

```
configure terminal
 aaa authorization commands 1 default group tacacs+ local
 aaa authorization commands 15 default group tacacs+ local
end
```

> ⚠️ **Antes de aplicarlo**, compruebe que tiene acceso por consola. Un error en el perfil puede bloquear todos los comandos por SSH. Por defecto la consola no usa autorización de comandos.

### Prueba

```
RT-EDGE# show ip interface brief      ✅ permitido
RT-EDGE# configure terminal
Command authorization failed.          ❌ denegado
```

---

## 🔴 Nivel 6 — Grupos y Dispositivos

### Grupos de usuarios

En lugar de asignar el perfil a cada usuario, se asigna por grupo:

```
    group netadmins
    group auditores

    user daniel {
        password login = clear Daniel123
        password pap = login
        member = netadmins
    }

    user auditor {
        password login = clear Auditor123
        password pap = login
        member = auditores
    }

    ruleset {
        rule {
            script {
                if (member == netadmins) { profile = admin permit }
                if (member == auditores) { profile = readonly permit }
                deny
            }
        }
    }
```

> 💡 Para agregar un administrador nuevo basta con `member = netadmins`.

### Dispositivos por red (con claves distintas)

En lugar de `0.0.0.0/0`, restrinja quién puede consultar:

```
    host core {
        address = 172.16.0.0/24
        key = ClaveCore2026
    }

    host acceso {
        address = 10.0.0.0/8
        key = ClaveAcceso2026
    }
```

> 💡 Si llega una consulta desde una IP no declarada, se ignora. Cada segmento tiene su propia clave.

### Varios servidores en el router (redundancia)

```
configure terminal
 tacacs server TACACS-1
  address ipv4 172.16.99.10
  key ClaveCore2026
 tacacs server TACACS-2
  address ipv4 172.16.99.11
  key ClaveCore2026
 aaa group server tacacs+ TACACS-GROUP
  server name TACACS-1
  server name TACACS-2
 aaa authentication login TACACS_LOGIN group TACACS-GROUP local
end
```

Si TACACS-1 no responde, el router consulta TACACS-2. Si ninguno responde, usa el usuario local.

---

## 🔴 Nivel 7 — Auditoría y Monitoreo

### Router: accounting completo

```
configure terminal
 aaa accounting exec default start-stop group tacacs+
 aaa accounting commands 1 default start-stop group tacacs+
 aaa accounting commands 15 default start-stop group tacacs+
end
```

### Consultas útiles

```bash
# Logins fallidos agrupados por usuario
grep -i fail /var/log/tac_plus-ng/authc.log | awk '{print $0}' | sort | uniq -c

# Comandos ejecutados por un usuario
grep daniel /var/log/tac_plus-ng/acct.log | grep cmd

# Actividad de hoy
grep "$(date +%Y-%m-%d)" /var/log/tac_plus-ng/acct.log
```

### Desde el router

```
show users          ! sesiones activas
show tacacs         ! contadores y estado del servidor
debug tacacs        ! ver el intercambio en vivo (undebug all para detener)
debug aaa authentication
```

### Visualización con Splunk (opcional)

Si hay un Splunk en el lab, se agregan los archivos de log como entrada monitoreada (`/var/log/tac_plus-ng/*.log`) con el Universal Forwarder o con rsyslog. Así se pueden armar tableros de:

- Logins por usuario y por hora
- Intentos fallidos (posible fuerza bruta)
- Comandos de configuración ejecutados

---

## 📑 Referencia Rápida

### Servidor

| Tarea | Comando |
|---|---|
| Validar configuración | `tac_plus-ng -P /etc/tac_plus-ng/tac_plus-ng.cfg` |
| Estado | `systemctl status tac_plus-ng` |
| Reiniciar | `systemctl restart tac_plus-ng` |
| Logs del servicio | `journalctl -u tac_plus-ng -f` |
| Puerto | `ss -tlnp \| grep :49` |
| Listar usuarios | `grep -E "^\s*user " /etc/tac_plus-ng/tac_plus-ng.cfg` |
| Hash de contraseña | `openssl passwd -6 'Clave'` |

### Router

| Tarea | Comando |
|---|---|
| Login con TACACS+ | `aaa authentication login TACACS_LOGIN group tacacs+ local` |
| Nivel de privilegio | `aaa authorization exec default group tacacs+ local` |
| Control de comandos | `aaa authorization commands 15 default group tacacs+ local` |
| Registro de sesiones | `aaa accounting exec default start-stop group tacacs+` |
| Registro de comandos | `aaa accounting commands 15 default start-stop group tacacs+` |
| Estado | `show tacacs` |

### Flujo para cualquier cambio

```
Editar .cfg  →  Validar (-P)  →  Reiniciar  →  Probar login  →  Revisar logs
```

---

## 🎓 Ejercicios

### 🟢 Básico

1. Agregue los usuarios `ana` y `pedro` y pruebe el login de ambos.
2. Cambie la contraseña de `ana` y verifique que la anterior ya no funciona.
3. Elimine a `pedro` y confirme que ya no puede entrar.

### 🟡 Intermedio

4. Convierta todas las contraseñas a `crypt`.
5. Configure tac_plus-ng como servicio systemd y reinicie el Ubuntu. ¿El servicio levanta solo?
6. Haga que `ana` entre directo con nivel 15 y `alumno` con nivel 1.

### 🔴 Avanzado

7. Cree el perfil `readonly` y verifique que `auditor` no puede entrar a `configure terminal`.
8. Cree los grupos `netadmins` y `auditores` y migre los usuarios a grupos.
9. Restrinja los `host` por segmento con claves distintas.
10. Active accounting de comandos. Entre como `ana`, cambie el hostname de un router y encuentre el comando en `acct.log`.
11. **Investigación:** desde los logs, identifique quién hizo un cambio en un router, a qué hora y desde qué IP.

---

## 📖 Referencias

| Recurso | Enlace |
|---|---|
| RFC 8907 (TACACS+) | https://www.rfc-editor.org/rfc/rfc8907 |
| tac_plus-ng | https://github.com/MarcJHuber/event-driven-servers |
| Cisco AAA | https://www.cisco.com/c/en/us/support/docs/security/ios-aaa/ |

---

## ✍️ Autor

**Daniel "pulentoski" Soto**
🏢 Docente — INACAP La Serena | Informática, Ciberseguridad y Telecomunicaciones
💼 Co-founder — EscudoNorte
