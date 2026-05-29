# Configuración de acceso Telnet en Cisco IOS

## ¿Qué es y por qué importa?

Cuando trabajamos con equipos Cisco en un laboratorio o entorno de red, necesitamos una forma de **administrarlos de forma remota** sin estar físicamente conectados al puerto de consola. Telnet es el protocolo más básico para lograrlo: permite abrir una sesión de terminal sobre la red TCP/IP.

Para que un router o switch Cisco acepte conexiones Telnet entrantes, hay que configurar las **líneas VTY** (*Virtual Terminal Lines*). Estas líneas son canales virtuales que el IOS reserva para sesiones remotas. Sin esta configuración, el equipo simplemente rechazará cualquier intento de conexión.

> ⚠️ **Nota importante:** Telnet transmite todo en texto plano, incluyendo la contraseña. En entornos reales de producción se usa SSH. Esta guía es válida para laboratorios y práctica inicial.

---

## Requisitos previos

- Acceso al modo de configuración global del equipo (`configure terminal`)
- El equipo debe tener al menos una interfaz con dirección IP activa
- Conectividad IP entre tu PC y el equipo

---

## Los 4 comandos clave

### Paso 1 — Entrar a la línea VTY

```
Router(config)# line vty 0 4
```

Accede a la configuración de las líneas de terminal virtual. El rango `0 4` habilita hasta **5 sesiones simultáneas** (0, 1, 2, 3 y 4). Puedes usar `0 15` en equipos que lo soporten para hasta 16 sesiones.

---

### Paso 2 — Establecer la contraseña

```
Router(config-line)# password cisco
```

Define la contraseña que se pedirá al usuario cuando intente conectarse por Telnet. En este ejemplo se usa `cisco`, pero en un entorno real debes elegir una contraseña segura.

---

### Paso 3 — Habilitar el login

```
Router(config-line)# login
```

Activa la autenticación por contraseña en la línea VTY. **Sin este comando, la contraseña definida en el paso anterior no se pedirá**, y cualquiera podría conectarse sin autenticarse.

---

### Paso 4 — Permitir el transporte Telnet

```
Router(config-line)# transport input telnet
```

Especifica qué protocolos están permitidos para conectarse a estas líneas. Con `telnet` solo se permite ese protocolo. También puedes usar `transport input ssh telnet` para permitir ambos, o `transport input all` para no restringir.

---

## Configuración completa (resumen)

```
Router> enable
Router# configure terminal
Router(config)# line vty 0 4
Router(config-line)# password cisco
Router(config-line)# login
Router(config-line)# transport input telnet
Router(config-line)# end
Router# write memory
```

> 💡 El comando `write memory` (o `copy running-config startup-config`) guarda la configuración para que persista tras un reinicio.

---

## Verificación

Para comprobar que todo funciona, desde otro equipo con conectividad:

```
C:\> telnet 192.168.1.1
```

El router debe pedir contraseña. Si ingresas `cisco`, deberías obtener acceso al modo EXEC de usuario (`Router>`).

---

## Diferencia entre `login` y `login local`

| Comando | Autenticación |
|---|---|
| `login` | Usa la contraseña definida con `password` en la línea VTY |
| `login local` | Usa usuarios creados con `username` + `secret` en la config global |

Para entornos más controlados, `login local` es preferible porque permite definir usuarios individuales con distintos privilegios.

---

## Próximo paso recomendado

Una vez dominada esta configuración, el siguiente paso natural es configurar **SSH**, que cifra la comunicación y es el estándar en redes reales:

```
Router(config)# ip domain-name lab.local
Router(config)# crypto key generate rsa modulus 1024
Router(config)# line vty 0 4
Router(config-line)# transport input ssh
Router(config-line)# login local
```
