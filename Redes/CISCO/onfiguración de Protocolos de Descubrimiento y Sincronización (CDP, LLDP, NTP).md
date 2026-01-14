# Configuración de Protocolos de Descubrimiento y Sincronización (CDP, LLDP, NTP)

Este documento resume la definición, uso y comandos de configuración para los protocolos **CDP**, **LLDP** y **NTP** en entornos de red Cisco (IOS).

---

## 1. CDP (Cisco Discovery Protocol)

### Definición
Protocolo de capa 2 (enlace de datos) **propietario de Cisco**. Se activa por defecto en la mayoría de los equipos Cisco y se utiliza para compartir información entre dispositivos de la marca conectados directamente.

### Uso
- Detectar dispositivos vecinos de Cisco (routers, switches, telefonía IP).
- Obtener detalles como: Hostname, dirección IP, capacidades del dispositivo, plataforma (modelo) e IDs de interfaces locales y remotas.
- Facilitar la creación de diagramas de topología física cuando no hay documentación.

### Comandos de Configuración

| Acción | Comando (Modo) |
| :--- | :--- |
| Habilitar CDP globalmente | `cdp run` (config) |
| Deshabilitar CDP globalmente | `no cdp run` (config) |
| Habilitar en una interfaz específica | `cdp enable` (config-if) |
| Deshabilitar en una interfaz | `no cdp enable` (config-if) |

### Comandos de Verificación
- `show cdp neighbors`: Lista resumida de vecinos.
- `show cdp neighbors detail`: Información completa (incluye direcciones IP y versión de IOS).
- `show cdp traffic`: Contadores de paquetes enviados y recibidos.

---

## 2. LLDP (Link Layer Discovery Protocol - IEEE 802.1AB)

### Definición
Protocolo de descubrimiento de capa 2 **estándar de la industria (abierto)**. Es la alternativa neutral a CDP, permitiendo interoperabilidad entre distintos fabricantes.

### Uso
- Permite que dispositivos de diferentes marcas (Cisco, HP, Juniper, etc.) se descubran entre sí.
- Intercambio de identidades, capacidades y descripciones de puertos en redes multi-vendor.

### Comandos de Configuración

| Acción | Comando (Modo) |
| :--- | :--- |
| Habilitar LLDP globalmente | `lldp run` (config) |
| Deshabilitar LLDP globalmente | `no lldp run` (config) |
| Habilitar envío en interfaz | `lldp transmit` (config-if) |
| Habilitar recepción en interfaz | `lldp receive` (config-if) |

### Comandos de Verificación
- `show lldp neighbors`: Lista resumida de vecinos.
- `show lldp neighbors detail`: Detalles extendidos del vecino.
- `show lldp traffic`: Estadísticas de paquetes lldp.

---

## 3. NTP (Network Time Protocol)

### Definición
Protocolo diseñado para sincronizar los relojes de los dispositivos a través de redes de datos utilizando el puerto **UDP 123**.

### Uso
- **Precisión en Logs:** Crucial para que los mensajes de error (Syslog) tengan la misma estampa de tiempo en toda la red.
- **Seguridad:** Necesario para la validación de certificados digitales y protocolos de autenticación basados en tiempo.

### Concepto de Stratum (Estrato)
- **Stratum 0:** Fuentes de tiempo de alta precisión (Relojes atómicos, GPS).
- **Stratum 1:** Servidores conectados directamente a una fuente Stratum 0.
- **Stratum n:** Cada salto de red entre el servidor y el cliente aumenta el nivel de estrato (máximo 15).

### Comandos de Configuración

| Acción | Comando (Modo) |
| :--- | :--- |
| Configurar como servidor (Maestro) | `ntp master <estrato>` (config) |
| Configurar como cliente | `ntp server <IP_Servidor>` (config) |
| Actualizar reloj de hardware (Switches) | `ntp update-calendar` (config) |
| Configurar hora manualmente | `clock set hh:mm:ss <día> <mes> <año>` (Priv. EXEC) |

### Comandos de Verificación
- `show ntp status`: Indica si el reloj está sincronizado y el estrato.
- `show ntp associations`: Muestra los servidores/vecinos NTP conocidos.
- `show clock detail`: Muestra la hora actual y la fuente de sincronización (NTP o local).

---

> **Tip de administración:** Siempre guarda los cambios con `copy running-config startup-config` después de realizar cualquier ajuste.
