# 📦 Información del Repositorio TACACS+ Docker + GNS3

## 🎯 Objetivo

Proporcionar una guía completa y funcional para desplegar un servidor TACACS+ en Docker dentro de GNS3, para uso en laboratorios educativos de ciberseguridad.

---

## 📁 Estructura del Repositorio

```
tacacs-gns3-lab/
├── README.md                    # Guía principal (paso a paso)
├── CHANGELOG.md                 # Historial de cambios
├── REPO_INFO.md                 # Este archivo
├── LICENSE                      # Licencia MIT
├── .gitignore                   # Archivos ignorados por Git
│
├── setup_tacacs.py              # Script Python automatizado
│
└── tacacs-gns3-lab/             # Carpeta generada por setup_tacacs.py
    ├── Dockerfile               # Receta Docker
    ├── entrypoint.sh            # Script de inicio del contenedor
    ├── tac_plus.conf            # Configuración TACACS+
    └── tacacs-server.tar        # Imagen Docker exportada (generada)
```

---

## 🚀 Flujo de Uso

### Opción A: Automática (Recomendada)

```bash
python3 setup_tacacs.py
# Genera automáticamente todo y compila la imagen
```

### Opción B: Manual

```bash
mkdir tacacs-gns3-lab
cd tacacs-gns3-lab

# Crear archivos manualmente (Dockerfile, entrypoint.sh, tac_plus.conf)
# Luego:
docker build -t tacacs-server:v1 .
docker save -o tacacs-server.tar tacacs-server:v1
```

---

## 📋 Archivos Principales

### **README.md**
- Guía paso a paso para Linux y Windows
- Configuración de red (IP fija vs DHCP)
- Troubleshooting y FAQ
- Checklist de verificación

### **setup_tacacs.py**
- Script Python 3 que automatiza todo
- Genera Dockerfile, entrypoint.sh, tac_plus.conf
- Compila imagen Docker
- Exporta tacacs-server.tar

### **Dockerfile**
- Base: Debian Bullseye Slim
- Compila TACACS+ desde fuente oficial (Shrubbery Networks)
- Instala dependencias (libwrap0-dev, libpam0g-dev, bison, flex)
- Copia configuración y entrypoint

### **entrypoint.sh**
- Verifica sintaxis de tac_plus.conf
- Inicia TACACS+ en background
- Mantiene bash abierto para consola interactiva en GNS3

### **tac_plus.conf**
- Configuración de TACACS+
- Grupos: admins (priv-lvl 15), limited (priv-lvl 1)
- Usuarios: diego (admin), seba (limited)
- Key por defecto: 12345

---

## ✅ Especificaciones Técnicas

| Aspecto | Valor |
|--------|-------|
| **Base del Contenedor** | Debian Bullseye Slim |
| **Método de Instalación** | Compilación desde fuente |
| **Versión TACACS+** | F4.0.4.28 (Shrubbery Networks) |
| **Puerto de Servicio** | TCP/49 |
| **Binario** | /usr/local/sbin/tac_plus |
| **Config** | /etc/tacacs+/tac_plus.conf |
| **Logs** | /var/log/tac_plus.acct |

---

## 🔐 Seguridad

### ⚠️ Para Laboratorio

- ✅ Users con contraseña cleartext (educativo)
- ✅ Key por defecto: 12345
- ✅ Sin encriptación TLS

### 🛡️ Para Producción

- ❌ Cambiar `key = 12345` por contraseña fuerte
- ❌ Usar contraseñas encriptadas (crypt/des)
- ❌ Implementar autorización granular
- ❌ Habilitar auditoría y logging
- ❌ Considerar TACACS+ NG con soporte moderno

---

## 🧪 Testeado En

- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Debian 11 (Bullseye)
- ✅ GNS3 2.2.x+
- ✅ Docker 20.10+
- ✅ Python 3.7+

---

## 📖 Documentación Relacionada

- [TACACS+ RFC 8907](https://tools.ietf.org/html/rfc8907)
- [Shrubbery Networks](https://www.shrubbery.net/tac_plus/)
- [GNS3 Docker Integration](https://docs.gns3.com/en/latest/using-gns3/administration/gns3-with-docker.html)
- [Cisco AAA Configuration](https://www.cisco.com/c/en/us/support/docs/security/authentication-authorization-accounting-aaa/10384-index.html)

---

## 🐛 Problemas Conocidos

### Console se cierra en GNS3
**Solución:** Actualizar a entrypoint.sh que mantiene bash abierto

### TACACS+ no inicia
**Solución:** Verificar sintaxis de tac_plus.conf

### Sin conectividad
**Solución:** Configurar IP correctamente y verificar gateway

Ver README.md > Troubleshooting para más detalles.

---

## 📝 Contribuciones

Este es un proyecto educativo. Contribuciones bienvenidas para:
- Mejorar documentación
- Agregar más ejemplos de configuración
- Optimizar Dockerfile
- Agregar soporte para TACACS+ NG

---

## 📄 Licencia

MIT License - Ver archivo LICENSE

---

## 👤 Autor

Proyecto educativo para enseñanza de AAA (Autenticación, Autorización, Auditoría) en redes Cisco.

**Última actualización:** 2026-01-02
**Versión:** 1.0.0
**Estado:** ✅ Funcional y testeado
