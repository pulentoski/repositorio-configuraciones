# 📖 Manual Técnico: Fundamentos y Operación de Ansible



### ¿Qué es la Automatización Declarativa?
Ansible es un motor de automatización que permite gestionar servidores sin intervención manual. A diferencia de los scripts tradicionales (imperativos), Ansible es **declarativo**: el ingeniero define el "estado final deseado" y la herramienta resuelve los pasos técnicos para alcanzarlo.

### Conceptos Clave para Ingeniería
- **Arquitectura Agentless:** No requiere software residente en los nodos remotos. Utiliza **SSH** y **Python**, lo que minimiza el consumo de recursos y la superficie de ataque en la red.
- **Idempotencia:** Es la capacidad de ejecutar la misma operación múltiples veces sin cambiar el resultado tras la primera aplicación exitosa. Esto garantiza la estabilidad y evita inconsistencias en los servidores.
- **Nodo de Control vs. Nodo Administrado:** El *Control Node* es la estación de trabajo donde reside Ansible (tu máquina local); los *Managed Nodes* son los servidores finales (instancias en AWS).

---

## 2. Protocolo de Instalación (Nodo de Control)

Para preparar el entorno de gestión en un sistema basado en Debian o Ubuntu, se deben ejecutar los siguientes comandos en la terminal del nodo de control:

```bash
# 1. Actualización de los índices de repositorios locales
sudo apt update

# 2. Instalación de dependencias para gestionar repositorios PPA
sudo apt install software-properties-common -y

# 3. Incorporación del repositorio oficial de los desarrolladores de Ansible
sudo add-apt-repository --yes --update ppa:ansible/ansible

# 4. Instalación del motor de ejecución de Ansible
sudo apt install ansible -y
```

### Verificación de la instalación correcta
```bash
ansible --version
```

---

## 3. El "Ensamble" Técnico: Estructura de Archivos

Para que un proceso de automatización sea exitoso, Ansible requiere una estructura jerárquica de archivos:

### A. El Inventario (hosts.ini)
Es la base de datos lógica que define el alcance de la red y las direcciones de los nodos.

```ini
[servidores_iptv]
13.217.54.87 ansible_user=ubuntu ansible_ssh_private_key_file=~/mis-llaves/clave.pem
```

### B. El Playbook (deploy.yml)
Es el manual de estrategia escrito en formato YAML. Sus secciones principales son:

- `hosts`: Indica el grupo de servidores destino definido en el inventario.  
- `become: yes`: Indica que las tareas requieren escalada de privilegios (sudo).  
- `tasks`: Lista de acciones secuenciales que invocan módulos de Ansible.  

---

## 4. Guía de Comandos y Ejemplos de Uso

### 1. Ejecución de Playbooks (Configuraciones Complejas)
Este comando procesa el archivo YAML y aplica todas las tareas definidas de forma secuencial.

```bash
ansible-playbook -i hosts.ini deploy.yml
```

### 2. Comandos Ad-Hoc (Gestión y Auditoría en Tiempo Real)
Se utilizan para tareas de diagnóstico rápido sin necesidad de escribir un archivo de script completo.

#### Verificar conectividad (Módulo Ping)
```bash
ansible servidores_iptv -i hosts.ini -m ping
```

#### Auditoría de Memoria RAM (Módulo Shell)
```bash
ansible servidores_iptv -i hosts.ini -a "free -m"
```

#### Gestión de Estados de Servicio (Módulo Service)
```bash
ansible servidores_iptv -i hosts.ini -m service -a "name=tvheadend state=restarted" --become
```

---

## 5. Matriz de Módulos Críticos en Telecomunicaciones

| Módulo   | Función Técnica                         | Aplicación en el Sistema                              |
|----------|----------------------------------------|-------------------------------------------------------|
| apt      | Gestión de paquetes `.deb`             | Instalación de dependencias base de Linux             |
| snap     | Gestión de paquetes autocontenidos     | Instalación aislada de TVHeadend                      |
| get_url  | Cliente de transferencia HTTP/HTTPS    | Descarga de listas M3U o archivos remotos             |
| template | Procesamiento de archivos Jinja2       | Despliegue de archivos de configuración dinámicos     |
| ufw      | Gestión de Firewall (Netfilter)        | Apertura de puertos de streaming (9981, 9982)         |

---

## 6. Ejemplo de Diseño de Tareas (YAML)

Un diseño profesional debe ser legible y registrar sus resultados para auditorías:

```yaml
- name: Instalación de TVHeadend mediante SNAP (Método Robusto)
  snap:
    name: tvheadend
    state: present
  register: resultado_log  # Almacena el resultado para verificar errores
```

---

## Resumen Didáctico

Ansible transforma la gestión de infraestructuras en código fuente. El objetivo es que el alumno comprenda que la infraestructura debe ser tratada como software: **versionable, auditable y automatizable**.
