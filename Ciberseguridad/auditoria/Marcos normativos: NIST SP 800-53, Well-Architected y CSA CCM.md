# 14 — Marcos normativos: NIST SP 800-53, Well-Architected y CSA CCM

> Configurar un control no basta: hay que poder decir **qué norma cumple y por qué**. Esta guía entrega los marcos de referencia y cómo usarlos para justificar configuraciones, auditar y proponer mejoras.

---

## NIST SP 800-53 Rev. 5

> **Qué es:** Catálogo de controles de seguridad y privacidad del National Institute of Standards and Technology (EE. UU.). Los controles se agrupan en familias identificadas por dos letras (AC = control de acceso, AU = auditoría, etc.).
>
> **Para qué sirve:** Es la referencia más usada para justificar un control técnico y evaluar cumplimiento. Cada configuración del servidor se puede asociar a un control específico.

### Familias relevantes

| Familia | Nombre | Tema |
|---|---|---|
| AC | Access Control | Quién accede y qué puede hacer |
| AU | Audit and Accountability | Registro y revisión de eventos |
| IA | Identification and Authentication | Cómo se comprueba la identidad |
| SC | System and Communications Protection | Red y cifrado |
| CM | Configuration Management | Configuración segura y mínima |

### Controles aplicables a un servidor Linux en la nube

| Control | Nombre | Implementación técnica |
|---|---|---|
| AC-2 | Account Management | Usuarios y grupos creados por función (`useradd`, `groupadd`) |
| AC-3 | Access Enforcement | Permisos de archivos y reglas sudoers |
| AC-5 | Separation of Duties | `sysops` administra, `auditores` solo revisa |
| AC-6 | Least Privilege | sudoers con comandos exactos, root deshabilitado |
| AC-7 | Unsuccessful Logon Attempts | `MaxAuthTries`, fail2ban |
| AC-12 | Session Termination | `TMOUT`, `LoginGraceTime` |
| AC-17 | Remote Access | SSH con llave, `AllowGroups`, `AllowUsers` por IP |
| AU-2 | Event Logging | Eventos registrados en `auth.log` y CloudTrail |
| AU-3 | Content of Audit Records | Fecha, usuario, IP, resultado en cada evento |
| AU-6 | Audit Record Review, Analysis, and Reporting | Revisión y análisis de `auth.log`, `last`, `lastb`, CloudTrail |
| AU-9 | Protection of Audit Information | Auditor sin permiso para borrar logs |
| IA-2 | Identification and Authentication | Usuario único por persona, llave SSH |
| IA-2(1) | Multi-Factor Authentication to Privileged Accounts | MFA TOTP en SSH |
| IA-5 | Authenticator Management | Llaves ED25519, permisos `600`/`400`, contraseñas para sudo |
| SC-7 | Boundary Protection | Security Group con SSH solo desde `/32` |
| SC-8 | Transmission Confidentiality and Integrity | SSH cifra la sesión |
| SC-28 | Protection of Information at Rest | Cifrado EBS o LUKS |
| CM-7 | Least Functionality | Solo los servicios y puertos necesarios |

Referencia: [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

---

## Microsoft Azure Well-Architected Framework — Pilar de seguridad

> **Qué es:** Guía de buenas prácticas de Microsoft para diseñar cargas de trabajo en la nube. Tiene cinco pilares; el de **seguridad** se basa en Zero Trust.
>
> **Para qué sirve:** Sus principios son independientes del proveedor: aplican igual en AWS o en un servidor propio. AWS tiene su equivalente, el *AWS Well-Architected Framework*, con un pilar de seguridad análogo.

### Principios Zero Trust

| Principio | Significado | Aplicación en el servidor |
|---|---|---|
| Verificar explícitamente | Autenticar y autorizar cada acceso | Llave SSH + MFA |
| Mínimo privilegio | Solo el acceso necesario, por el tiempo necesario | sudoers por rol, `AllowGroups` |
| Asumir la brecha | Diseñar pensando que un control puede fallar | Registro, auditoría, cifrado, segmentación |

### Recomendaciones del pilar de seguridad aplicables

| Área | Aplicación |
|---|---|
| Gestión de identidades y accesos | Usuarios individuales, roles por grupo, MFA |
| Controles de red | Security Group restrictivo, firewall del SO |
| Cifrado | Datos en reposo (EBS/LUKS) y en tránsito (SSH) |
| Hardening | Root deshabilitado, sin contraseñas, servicios mínimos |
| Monitoreo y detección | Revisión de `auth.log` y CloudTrail |

Referencia: [Azure Well-Architected Framework — Security](https://learn.microsoft.com/es-es/azure/well-architected/security/)

---

## CSA Cloud Controls Matrix (CCM)

> **Qué es:** Marco de controles específico para la nube publicado por la Cloud Security Alliance. Organiza los controles en dominios y los relaciona con otras normas (ISO 27001, NIST, PCI DSS).
>
> **Para qué sirve:** Evaluar la seguridad de un servicio cloud con controles pensados para la nube, incluyendo qué le toca al proveedor y qué al cliente.

| Dominio | Nombre | Aplicación |
|---|---|---|
| IAM | Identity & Access Management | Usuarios, grupos, sudoers, MFA, separación de funciones |
| LOG | Logging and Monitoring | `auth.log`, CloudTrail, revisión de sesiones |
| CEK | Cryptography, Encryption & Key Management | Cifrado EBS/LUKS, llaves SSH |
| IVS | Infrastructure & Virtualization Security | Security Group, hardening de la instancia |
| TVM | Threat & Vulnerability Management | Actualizaciones de seguridad, Lynis |

Referencia: [CSA Cloud Controls Matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix)

---

## Cómo justificar un control

> **Qué es:** Relacionar cada configuración con el riesgo que reduce y la norma que cumple.
>
> **Para qué sirve:** Transformar un comando en evidencia de cumplimiento.

Estructura: **configuración → qué riesgo mitiga → control(es) que cumple**.

**Ejemplo**
> Se configuró `PasswordAuthentication no` en SSH. Esto elimina los ataques de fuerza bruta contra contraseñas, ya que solo se aceptan llaves criptográficas. Cumple NIST IA-2 e IA-5, el principio *verificar explícitamente* del Well-Architected y el dominio IAM de CSA CCM.

---

## Tabla de cumplimiento

> **Qué es:** Cuadro que contrasta cada control normativo con la evidencia encontrada y su estado.
>
> **Para qué sirve:** Mostrar de un vistazo qué se cumple, qué no y dónde están las brechas.

| Control | Evidencia | Estado | Observación |
|---|---|---|---|
| AC-6 Least Privilege | `sudo -l -U usr_auditor` muestra solo comandos de lectura | Cumple | — |
| IA-2(1) MFA | SSH pide `Verification code` | Cumple | — |
| AU-6 Audit Review | `auth.log` revisado; CloudTrail sin acceso | Parcial | Cuenta sin permisos sobre CloudTrail |
| AU-9 Protection of Audit Info | Logs solo locales | Parcial | Sin copia central (rsyslog) |
| SC-28 Data at Rest | Volumen EBS `Encrypted` | Cumple | — |

Estados: **Cumple** / **Parcial** / **No cumple**. Todo *Parcial* o *No cumple* debe dar origen a una recomendación.

---

## Cómo redactar una recomendación de mejora

> **Qué es:** Propuesta técnica que corrige una brecha detectada en la auditoría.
>
> **Para qué sirve:** Cerrar el ciclo de mejora continua: detectar → evaluar → proponer.

Estructura: **hallazgo → riesgo → recomendación → control**.

**Ejemplo**
> **Hallazgo:** los logs se guardan solo en el servidor.
> **Riesgo:** un atacante con privilegios puede borrarlos y eliminar la evidencia.
> **Recomendación:** enviar los logs a un servidor central con rsyslog o a CloudWatch Logs.
> **Control:** NIST AU-9, dominio LOG de CSA CCM.
