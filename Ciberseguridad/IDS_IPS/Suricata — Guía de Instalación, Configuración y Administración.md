# Suricata — Guía de Instalación, Configuración y Administración 🛡️

## ¿Qué es Suricata? 📖

Sistema de detección y prevención de intrusiones (IDS/IPS) de código abierto. Monitorea tráfico de red en tiempo real, analiza patrones sospechosos y puede bloquear actividades maliciosas.

---

## Funcionamiento de Suricata 🔄

| Etapa | Descripción |
|-------|------------|
| **Captura** | "Escucha" tráfico en interfaz específica |
| **Decodificación** | Descompone paquetes en elementos comprensibles (IPs, puertos, protocolos) |
| **DPI** | Inspección profunda de paquetes — analiza contenido malicioso |
| **Comparación** | Contrasta tráfico contra reglas predefinidas |
| **Alertas** | Genera alertas con detalles del evento |
| **Registro** | Guarda logs detallados para análisis posterior |
| **Prevención (IPS)** | Bloquea tráfico malicioso en tiempo real (opcional) |

---

## Instalación 📦

### Preparación del Sistema

```bash
sudo apt update
sudo apt upgrade
```

### Debian/Kali Linux

```bash
sudo apt install suricata
```

### Ubuntu

```bash
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt update
sudo apt install suricata
```

### Descargar Reglas ET Open (Emerging Threats)

```bash
sudo suricata-update
```

---

## Configuración Principal ⚙️

Editar archivo base:

```bash
sudo nano /etc/suricata/suricata.yaml
```

| Parámetro | Qué cambiar | Ejemplo |
|-----------|------------|---------|
| `HOME_NET` | Red local a proteger | `HOME_NET: "[192.168.0.0/24]"` |
| `af-packet` interface | Interfaz de captura | `interface: ens2` |
| `pcap` interface | Interfaz alternativa PCAP | `interface: ens2` |
| `community-id` | Activar identificación única de eventos | `community-id: true` |
| `rule-files` | Ubicación de reglas personalizadas | `/etc/suricata/rules/custom.rules` |

---

## Validación y Prueba ✅

| Comando | Función |
|---------|---------|
| `suricata -T -c /etc/suricata/suricata.yaml` | Valida sintaxis de configuración |
| `suricata -t` | Ejecuta en modo prueba (análisis de capturas) |
| `suricata -c /etc/suricata/suricata.yaml -i ens2` | Inicia en modo IDS interfaz ens2 |
| `suricata -c config -s rules -i ens2` | Inicia con reglas personalizadas |

Verificar logs en tiempo real:

```bash
tail -f /var/log/suricata/fast.log
```

---

## Administración de Servicios 🔧

| Comando | Acción |
|---------|--------|
| `sudo systemctl start suricata` | Inicia el servicio |
| `sudo systemctl stop suricata` | Detiene el servicio |
| `sudo systemctl restart suricata` | Reinicia el servicio |
| `sudo systemctl status suricata` | Verifica estado |
| `sudo systemctl enable suricata` | Inicio automático al arrancar |
| `sudo systemctl disable suricata` | Deshabilita inicio automático |

---

## Archivos de Logs 📊

### 1. **eve.json** — Registro exhaustivo de eventos

Contiene:
- Alertas de seguridad (intrusiones, ataques, anomalías)
- Flujos de red (IPs, puertos, protocolos, duración)
- Registros DNS (resoluciones de dominios)
- Registros HTTP/TLS (solicitudes, respuestas, encabezados, URLs)

**Uso:** Análisis forense profundo, reconstrucción de actividad.

---

### 2. **fast.log** — Resumen ejecutivo de alertas

Contiene por línea:
- Marca de tiempo
- Dirección IP y puertos (origen/destino)
- Regla activada
- Clasificación (ataque web, tráfico sospechoso)
- Prioridad/severidad

**Uso:** Revisión rápida de alertas urgentes.

---

### 3. **stats.log** — Rendimiento y métricas

Registra:
- Uso de CPU y memoria
- Paquetes procesados
- Reglas coincidentes

**Uso:** Evaluación de carga del sistema, optimización.

---

### 4. **suricata.log** — Diario de ejecución

Registra:
- Mensajes de inicio (versión, configuración)
- Errores y advertencias
- Notificaciones de eventos importantes

**Uso:** Resolución de problemas, mantenimiento.

---

## Solución: Error "fanout not supported by kernel" 🚨

### Causa 1: Kernel incompatible

```bash
# Verifica versión del kernel
uname -r

# Solución: Actualiza kernel
sudo apt upgrade linux-image-generic
```

### Causa 2: Cluster ID en uso

```bash
# Verifica procesos Suricata activos
ps aux | grep suricata

# Cambia cluster-id en suricata.yaml
# BUSCA: cluster-id: 99
# CAMBIA A: cluster-id: 100
```

### Cluster Types Disponibles

| Tipo | Descripción | Ideal para |
|------|-------------|-----------|
| `cluster_flow` ⭐ | Agrupa paquetes por flujo (IPs/puertos) | Mayoría de sistemas |
| `cluster_cpu` | Asigna secuencialmente a núcleos | Tarjetas NIC sin RSS |
| `cluster_qm` | Colas MPMC para eficiencia | Sistemas con muchos núcleos |

---

## Reglas — Fuentes de Detección 📋

### Emerging Threats Open (ET Open) — Recomendado

Fuente comunitaria gratuita, amplio catálogo de reglas de calidad.

**Descarga e instalación:**

```bash
wget https://rules.emergingthreats.net/open/suricata/emerging.rules.tar.gz
tar -xzf emerging.rules.tar.gz -C /etc/suricata/rules
nano /etc/suricata/suricata.yaml  # Descomenta líneas rule-files
sudo systemctl restart suricata
```

### Emerging Threats Pro (ET Pro)

Opción comercial: reglas adicionales, soporte prioritario, inteligencia exclusiva.

### Actualización de Reglas

**Automática (recomendado):**
```bash
sudo suricata-update
```

**Manual:**
Descargar y reemplazar periódicamente archivos de reglas.

### Reglas Personalizadas

Crea archivo `/etc/suricata/rules/custom.rules`:

```
alert http any any -> any any (msg:"Detección personalizada"; content:"patrón"; sid:1000001;)
```

Incluye en `suricata.yaml` → `rule-files:` → `- /etc/suricata/rules/custom.rules`

---

## Pruebas de Detección 🧪

| Método | Descripción |
|--------|------------|
| **Ataques simulados** | Usa Metasploit, Nmap para generar tráfico sospechoso |
| **Tráfico malicioso** | Genera contenido que coincida con reglas (⚠️ con precaución) |
| **Análisis de logs** | Examina `/var/log/suricata/` para verificar registros |

**Ejemplo: Verificar alertas en tiempo real**

Terminal 1:
```bash
sudo suricata -c /etc/suricata/suricata.yaml -i ens2
```

Terminal 2:
```bash
tail -f /var/log/suricata/fast.log
```

---

## Consideraciones de Optimización ⚡

| Aspecto | Recomendación |
|--------|--------------|
| **Rendimiento** | Evalúa impacto de reglas — desactiva si es necesario |
| **Falsos positivos** | Revisa y ajusta reglas para minimizar alertas falsas |
| **CPU/Memoria** | Monitorea stats.log para optimizar configuración |
| **Reglas personalizadas** | Crea para detectar amenazas específicas de tu entorno |

---

## Checklist de Implementación ✔️

- ✓ Sistema actualizado (`apt update && apt upgrade`)
- ✓ Suricata instalado (`apt install suricata`)
- ✓ Reglas descargadas (`suricata-update`)
- ✓ suricata.yaml configurado (HOME_NET, interfaz, community-id)
- ✓ Configuración validada (`suricata -T`)
- ✓ Logs accesibles en `/var/log/suricata/`
- ✓ Servicio habilitado (`systemctl enable suricata`)
- ✓ Monitoreo activo (`tail -f fast.log`)
- ✓ Reglas ET Open funcionando
- ✓ Pruebas de detección verificadas

---

**Última revisión:** 2025 | CML Labs 🛡️
