# 🔐 Cisco Port Security Commands Cheat Sheet

## 📌 Introducción

Port Security permite controlar qué dispositivos pueden conectarse a un puerto de un switch Cisco mediante restricciones de direcciones MAC.

Se utiliza para:

- Restringir acceso no autorizado.
- Limitar dispositivos conectados.
- Mitigar ataques MAC Flooding.
- Generar alertas de seguridad.

---

# ⚙️ Habilitar Modo Privilegiado

```bash
enable
```

---

# ⚙️ Entrar al Modo de Configuración Global

```bash
configure terminal
```

---

# ⚙️ Seleccionar Interfaz

```bash
interface FastEthernet0/1
```

---

# ⚙️ Configurar Puerto en Modo Access

```bash
switchport mode access
```

✅ Requisito obligatorio para Port Security.

---

# 🔐 Habilitar Port Security

```bash
switchport port-security
```

---

# 🔢 Limitar Cantidad de Direcciones MAC

## Permitir máximo 2 dispositivos

```bash
switchport port-security maximum 2
```

---

# 📌 Sticky MAC

## Aprender MAC automáticamente

```bash
switchport port-security mac-address sticky
```

✅ El switch aprende automáticamente las MAC conectadas.

---

# 🧾 Configurar MAC Manualmente

```bash
switchport port-security mac-address 0011.2233.4455
```

✅ Solo esa MAC podrá usar el puerto.

---

# 🚨 Modos de Violación

---

## 🔹 Protect

```bash
switchport port-security violation protect
```

### Características

- Bloquea tráfico no autorizado.
- No genera logs.
- No apaga el puerto.

---

## 🔹 Restrict

```bash
switchport port-security violation restrict
```

### Características

- Bloquea tráfico no autorizado.
- Genera Syslog.
- Incrementa contador de violaciones.
- Mantiene el puerto activo.

---

## 🔹 Shutdown

```bash
switchport port-security violation shutdown
```

### Características

- Puerto entra en estado `err-disabled`.
- Apaga el puerto automáticamente.
- Genera logs Syslog.

---

# 🔄 Reactivar Puerto Bloqueado

```bash
interface FastEthernet0/1
shutdown
no shutdown
```

---

# 💾 Guardar Configuración

```bash
copy running-config startup-config
```

---

# 🔍 Verificar Configuración

---

## Mostrar Estado General

```bash
show port-security
```

---

## Ver Configuración de una Interfaz

```bash
show port-security interface FastEthernet0/1
```

---

## Ver Direcciones MAC Aprendidas

```bash
show port-security address
```

---

# 🧪 Configuración Completa de Ejemplo

```bash
enable

configure terminal

interface FastEthernet0/1

switchport mode access

switchport port-security

switchport port-security maximum 2

switchport port-security mac-address sticky

switchport port-security violation restrict

end

copy running-config startup-config
```

---

# ⚔️ Protección Contra MAC Flooding

Port Security ayuda a mitigar ataques donde un atacante intenta llenar la tabla CAM del switch con múltiples direcciones MAC falsas.

## Beneficios

- Limita MAC por puerto.
- Bloquea dispositivos no autorizados.
- Reduce riesgos de sniffing.
- Mejora seguridad LAN.

---

# 📚 Comandos Útiles Adicionales

---

## Ver Tabla MAC

```bash
show mac address-table
```

---

## Ver Interfaces

```bash
show interfaces status
```

---

## Ver Logs

```bash
show logging
```

---

## Restaurar Configuración del Puerto

```bash
default interface FastEthernet0/1
```

---

# 🛠 Tecnologías Relacionadas

- Cisco IOS
- Switching
- VLANs
- DHCP Snooping
- Dynamic ARP Inspection
- STP Security
- Network Access Control

---

# 📖 Recomendaciones

✅ Usar Port Security en puertos de usuarios finales.  
✅ No utilizar en enlaces trunk.  
✅ Combinar con VLAN Security.  
✅ Revisar logs periódicamente.  
✅ Configurar límites de MAC apropiados.

---

# 👨‍💻 Uso Educativo

Repositorio orientado a:

- Estudiantes de redes.
- Laboratorios Cisco.
- CCNA.
- Seguridad en Switching.
- Hardening de infraestructura LAN.

---
