# 🔐 AAA en Cisco
AAA es un sistema de seguridad que controla el acceso a dispositivos de red mediante 3 funciones:

## 📌 Componentes:
    Autenticación → Verifica identidad (¿Quién eres?)
    
    Autorización → Define permisos (¿Qué puedes hacer?)
    
    Contabilización → Registra actividades (¿Qué hiciste?)


## Comandos de Configuración Completos

HABILITAR EL SISTEMA AAA (OBLIGATORIO) ---
      
    aaa new-model

## CREAR USUARIOS CON NIVELES DE PRIVILEGIO ASIGNADOS ---

    username USER privilege 1 secret cisco1       ! Usuario básico (nivel 1)
    username SUPPORT privilege 5 secret cisco5    ! Soporte técnico (nivel 5)
    username JR-ADMIN privilege 10 secret cisco10 ! Administrador junior (nivel 10)
    username ADMIN privilege 15 secret cisco123   ! Administrador total (nivel 15)

# PERSONALIZAR PRIVILEGIOS DE COMANDOS POR NIVEL 
    privilege exec level 5 ping   ! Solo nivel 5+ puede usar PING
    privilege exec level 10 reload ! Solo nivel 10+ puede usar RELOAD

# CONTRASEÑAS PARA CAMBIO ENTRE NIVELES DE PRIVILEGIO 

    enable secret level 5 cisco5    ! Contraseña para entrar a nivel 5
    enable secret level 10 cisco10  ! Contraseña para entrar a nivel 10
    enable secret cisco15           ! Contraseña para nivel 15 (máximo)

# POLÍTICAS AAA PARA AUTENTICACIÓN, AUTORIZACIÓN Y CONTABILIZACIÓN 

    aaa authentication login default local    ! Autentica con base local de usuarios
    aaa authorization exec default local      ! Autoriza nivel de acceso según usuario
    aaa accounting exec default start-stop group local  ! Registra inicio/fin de sesiones

# CONFIGURACIÓN DE LÍNEA DE CONSOLA (acceso físico) 
    line con 0
     logging synchronous           ! Evita interrupciones de mensajes en consola
     login authentication default  ! Obliga autenticación AAA en consola

# CONFIGURACIÓN DE LÍNEAS VIRTUALES (acceso remoto por Telnet) 
    line vty 0 15
     transport input telnet         ! Habilita acceso por Telnet (solo laboratorio)
     login authentication default   ! Obliga autenticación AAA para conexiones
     authorization exec default     ! Aplica autorización de nivel de privilegio

🔍 Comandos de Verificación Recomendados

    show running-config | section aaa    ! Ver configuración AAA
    show privilege                      ! Ver nivel actual de privilegio
    show aaa sessions                   ! Ver sesiones AAA activas
    show users                          ! Ver usuarios conectados
