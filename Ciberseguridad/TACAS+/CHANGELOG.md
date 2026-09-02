# Changelog

Todos los cambios notables en este proyecto están documentados en este archivo.

## [1.0.0] - 2026-01-02

### ✅ Agregado
- Guía completa de TACACS+ en Docker + GNS3
- Dockerfile que compila TACACS+ desde fuente oficial (Shrubbery Networks)
- Script Python automatizado para generar imagen Docker
- Soporte para IP fija y DHCP
- Configuración de ejemplo con usuarios diego (admin) y seba (limitado)
- Documentación exhaustiva en README.md

### 🔧 Corregido
- Dockerfile ahora usa compilación desde fuente (sin depender de repositorios)
- entrypoint.sh mantiene consola bash abierta en GNS3
- Soporte universal para cualquier distribución Linux
- Rutas correctas de binario TACACS+ (/usr/local/sbin/tac_plus)

### 🗑️ Eliminado
- Dependencia de paquete apt `tacacs+` (descontinuado)
- Arquitectura que cerraba consola inmediatamente

### 📚 Documentación
- README.md completamente reescrito
- Guía paso a paso para Linux y Windows
- Troubleshooting incluido
- Checklist de verificación

---

## Estado Actual

✅ **Testeado en GNS3**
- Compilación exitosa en Ubuntu
- Consola mantenida abierta
- TACACS+ corriendo en background
- Conectividad verificada

**Versión:** 1.0.0
**Estado:** Producción-ready para laboratorios educativos
