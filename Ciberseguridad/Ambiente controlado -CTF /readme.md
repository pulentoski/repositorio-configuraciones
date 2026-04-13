# 🛡️ Ambientes Controlados y CTF

Repositorio de documentación para práctica de hacking ético. Cada sección cubre una plataforma o herramienta distinta para aprender ciberseguridad ofensiva y defensiva en entornos legales y seguros.

---

## ¿Qué es un ambiente controlado?

Un **ambiente controlado** es un entorno de laboratorio, aislado de redes de producción, donde se despliegan sistemas intencionalmente vulnerables para practicar técnicas de seguridad sin consecuencias legales ni daño real.

Se usan en:
- Diplomados y cursos de ciberseguridad
- Preparación para certificaciones (CEH, OSCP, CompTIA Security+)
- Investigación y desarrollo de exploits
- Demostraciones en clase

### Características de un buen ambiente controlado

- **Aislamiento de red:** la VM o contenedor no debe tener salida a internet durante las prácticas.
- **Snapshots:** permite restaurar el sistema a un estado limpio después de cada práctica.
- **Documentación:** cada vulnerabilidad debe estar documentada para que el alumno entienda qué está explotando y por qué funciona.

---

## ¿Qué es un CTF?

Un **CTF** (Capture The Flag) es una competencia o práctica de ciberseguridad donde el objetivo es encontrar una "bandera" (un texto oculto con formato específico, por ejemplo `FLAG{esto_es_una_bandera}`) explotando vulnerabilidades en sistemas diseñados para ese fin.

### Tipos de CTF

| Tipo | Descripción |
|---|---|
| **Jeopardy** | Retos independientes por categorías: web, forense, criptografía, reversing, etc. |
| **Attack/Defense** | Equipos defienden su servidor mientras atacan el del rival. |
| **Boot2Root** | Se parte desde acceso cero y el objetivo es obtener privilegios de root/SYSTEM. |

### Categorías comunes en CTF

- **Web:** SQL Injection, XSS, CSRF, LFI/RFI, IDOR
- **Forense:** análisis de capturas de red (.pcap), recuperación de archivos
- **Criptografía:** cifrados clásicos, RSA débil, hashing
- **Reversing:** ingeniería inversa de binarios
- **Pwn / Explotación:** buffer overflow, escalada de privilegios
- **OSINT:** recolección de información pública

---

## Plataformas documentadas

| Plataforma | Tipo | Descripción |
|---|---|---|
| [DVWA](./DVWA.md) | Ambiente controlado | App web vulnerable para práctica de ataques web |

---

## ⚠️ Aviso legal

Todo lo practicado en este repositorio debe realizarse **únicamente en entornos propios o con autorización explícita**. El uso de estas técnicas en sistemas ajenos sin permiso es ilegal.

- Usa **VirtualBox** o **VMware** con red en modo `Host-Only` o `Internal Network`.
- Toma un snapshot antes de cada práctica.
- Documenta lo que aprendes: anota el vector de ataque, el impacto y la mitigación.
