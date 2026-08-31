# 📡  SNMP v2 y v3 en Routers Cisco para Integración con Zabbix

## 🎯 Objetivo

Configurar SNMP en routers Cisco para monitoreo centralizado mediante Zabbix, comparando SNMPv2c (legado) con SNMPv3 (seguro).

---

## 📊 Comparativa: SNMPv2c vs SNMPv3

| Aspecto | SNMPv2c | SNMPv3 |
|---------|---------|--------|
| **Autenticación** | Basada en comunidad (texto plano) | Usuario + contraseña |
| **Encriptación** | ❌ Ninguna | ✅ AES/DES |
| **Seguridad** | 🔓 Baja | 🔒 Alta |
| **Compatibilidad** | Amplia (heredada) | Moderna (RFC 3414) |
| **Complejidad** | Simple | Media |

---

## 📋 Requisitos Previos

✓ Acceso `enable` al router Cisco  
✓ Servidor Zabbix 5.0+  
✓ Conectividad IP (UDP 161 query, 162 traps)  
✓ Python 3.8+ (opcional, para validación)

---

## 🔧 **PARTE 1: Configuración SNMPv2c (Cisco IOS)**

### Paso 1: Modo Privilegiado
```
Router> enable
Router# configure terminal
```

### Paso 2: Comunidad SNMP (Solo Lectura)
```
Router(config)# snmp-server community inacap RO
```
⚠️ **Nota:** La comunidad es visible en la red. Usar string fuerte en producción.

### Paso 3: Metadatos del Dispositivo
```
Router(config)# snmp-server location "Data Center La Serena"
Router(config)# snmp-server contact "admin@example.com"
Router(config)# snmp-server description "Cisco 2900 Series"
```

### Paso 4: Host Destino (Zabbix)
```
Router(config)# snmp-server host 192.168.1.100 version 2c inacap
Router(config)# snmp-server enable traps
```

### Paso 5: Guardar
```
Router(config)# exit
Router# write memory
```

### Validación en Zabbix
```bash
snmpwalk -v 2c -c inacap 192.168.x.x 1.3.6.1.2.1.1.1.0
```

---

## 🔐 **PARTE 2: Configuración SNMPv3 (Recomendado)**

### Paso 1: Crear Usuario SNMP v3
```
Router(config)# snmp-server group GRUPO_ADMIN v3 auth read VISTA_RO
Router(config)# snmp-server user monitor GRUPO_ADMIN v3 auth sha Passwd123! priv aes 128 PrivPass456!
```

**Parámetros:**
- `auth sha`: Autenticación con SHA-1 (alternativa: `md5`)
- `priv aes 128`: Encriptación AES-128 (alternativas: `aes 192`, `aes 256`)

### Paso 2: Definir Vistas SNMP
```
Router(config)# snmp-server view VISTA_RO 1.3.6.1.2.1 included
Router(config)# snmp-server view VISTA_RO 1.3.6.1.4.1 included
```

### Paso 3: Configurar Traps SNMPv3
```
Router(config)# snmp-server host 192.168.1.100 version 3 auth monitor
```

### Paso 4: Aplicar Configuración
```
Router(config)# exit
Router# write memory
Router# show snmp user
Router# show snmp group
```

### Validación en CLI
```bash
snmpwalk -v 3 -u monitor -a SHA -A Passwd123! -x AES -X PrivPass456! 192.168.x.x 1.3.6.1.2.1.1.1.0
```

---

## 📐 Tabla de Comandos Críticos

| Comando | SNMPv2c | SNMPv3 | Propósito |
|---------|---------|--------|-----------|
| `snmp-server community` | ✅ | ❌ | Define comunidad |
| `snmp-server user` | ❌ | ✅ | Crea usuario autenticado |
| `snmp-server group` | Opcional | ✅ | Agrupa políticas de acceso |
| `snmp-server view` | Opcional | ✅ | Limita OIDs accesibles |
| `snmp-server host` | ✅ | ✅ | Define servidor traps |

---

## 🛡️ **Recomendaciones de Seguridad**

### SNMPv3 (Preferido)
1. Usar algoritmos fuertes: SHA-2 (si soporta), AES-256
2. Cambiar contraseñas cada 90 días
3. Limitar acceso por ACL de red:
   ```
   Router(config)# access-list 1 permit 192.168.1.100
   Router(config)# snmp-server community inacap RO 1
   ```

### SNMPv2c (Si es necesario)
1. Renombrar comunidad default (`public` → `inacap-ro`)
2. Usar VLAN aislada para SNMP
3. Implementar SNMPv3 en paralelo
4. Deshabilitar v1:
   ```
   Router(config)# no snmp-server host ... version 1
   ```

---

## 📊 Monitoreo en Zabbix

### Configurar Host Zabbix (SNMPv3)
```yaml
Host: Router-Cisco
IP: 192.168.x.x
Interfaces:
  - SNMP
    Version: SNMPv3
    Username: monitor
    Auth Protocol: SHA
    Auth Password: Passwd123!
    Priv Protocol: AES
    Priv Password: PrivPass456!
```

### OIDs Comunes a Monitorear
```
1.3.6.1.2.1.1.1.0     → sysDescr (Descripción)
1.3.6.1.2.1.1.3.0     → sysUpTime (Disponibilidad)
1.3.6.1.2.1.25.3.2.1  → hrStorageUsed (Memoria)
1.3.6.1.2.1.2.2.1.10  → ifInOctets (Tráfico entrada)
```

---

## ⚠️ Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| `Timeout` | Firewall bloquea UDP 161 | Verificar ACL: `permit udp any any eq 161` |
| `Authorization failed` | Comunidad incorrecta | Validar `snmp-server community` |
| `No auth algorithm` | SNMPv3 sin soporte | Actualizar IOS Cisco |
| Traps no llegan | Zabbix no escucha | Verificar puerto 162 en Zabbix |

---

## 🔗 Referencias Normativas

- **RFC 3411-3418**: SNMP v3 (USM, VACM)
- **RFC 1905**: SNMPv2c Protocol Operations
- **Cisco IOS SNMP**: docs.cisco.com/snmp
- **OID Database**: oid-info.com

---

## 📝 Script de Validación (Python)

```python
#!/usr/bin/env python3
import subprocess
import sys

def test_snmp(ip, version, community=None, user=None):
    if version == "2c":
        cmd = f"snmpwalk -v 2c -c {community} {ip} 1.3.6.1.2.1.1.1.0"
    else:
        cmd = f"snmpwalk -v 3 -u {user} -a SHA -x AES {ip} 1.3.6.1.2.1.1.1.0"
    
    try:
        result = subprocess.run(cmd.split(), capture_output=True, timeout=5)
        return "✅ SNMP Activo" if result.returncode == 0 else "❌ SNMP Fallido"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    print(test_snmp("192.168.x.x", "2c", community="inacap"))
```

---

## 📚 Estructura de Carpetas Recomendada

```
snmp-monitoring/
├── configs/
│   ├── cisco-snmpv2c.conf
│   └── cisco-snmpv3.conf
├── zabbix-templates/
│   └── template_cisco_snmp.xml
├── validation/
│   └── snmp_test.py
└── README.md
```

---

**Última actualización:** Agosto 2026  
**Autor:** Pulentoski 🔧  
**Licencia:** CC BY-NC-ND 4.0
