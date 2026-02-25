# Structured Query Language (SQL) y Gestión de RDBMS

### Definición y Funcionamiento
**SQL (Structured Query Language)** es el lenguaje estándar de dominio específico diseñado para administrar y manipular sistemas de gestión de bases de datos relacionales (RDBMS). Funciona mediante consultas declarativas que permiten al motor de la base de datos determinar la ruta de ejecución más eficiente para recuperar, insertar o modificar registros.

### Jerarquía de Objetos en RDBMS
La organización de los datos sigue una estructura arbórea y lógica:
* **Instancia/Servidor:** El proceso de software que gestiona el acceso a los datos.
* **Base de Datos (Database):** Contenedor lógico independiente que agrupa esquemas y objetos.
* **Esquema (Schema):** Espacio de nombres que agrupa objetos (Tablas, Vistas, Procedimientos).
* **Tabla (Table):** Estructura bidimensional compuesta por filas (registros) y columnas (campos).
* **Campo (Column):** Atributo específico definido por un tipo de dato (INTEGER, VARCHAR, etc.).

# Lenguaje de Manipulación y Definición de Datos (DML y DDL)

En el ecosistema de SQL, los comandos se clasifican según su propósito técnico dentro de la base de datos. Las dos categorías principales son **DDL** y **DML**.

---

### 1. DDL (Data Definition Language)
El **Lenguaje de Definición de Datos** se utiliza para definir, modificar o eliminar la **estructura** de los objetos de la base de datos (tablas, índices, usuarios, etc.). Estos comandos afectan al "contenedor" y no al contenido.

* **CREATE:** Crea objetos (bases de datos, tablas, vistas).
* **ALTER:** Modifica la estructura de un objeto existente (añadir una columna).
* **DROP:** Elimina objetos de forma permanente.
* **TRUNCATE:** Vacía el contenido de una tabla pero mantiene su estructura.



---

### 2. DML (Data Manipulation Language)
El **Lenguaje de Manipulación de Datos** se utiliza para gestionar los **datos** que residen dentro de los objetos definidos por el DDL. Permite a los usuarios consultar y modificar la información.

* **SELECT:** Recupera datos de la base de datos (a veces clasificado como DQL).
* **INSERT:** Añade nuevos registros a una tabla.
* **UPDATE:** Modifica registros existentes.
* **DELETE:** Elimina registros específicos de una tabla.



---

### Cuadro Comparativo Técnico

| Característica | DDL (Definición) | DML (Manipulación) |
| :--- | :--- | :--- |
| **Objetivo** | Estructura / Esquema | Datos / Registros |
| **Efecto** | Cambia el diseño de la DB | Cambia el contenido de las filas |
| **Ejemplo real** | Crear una carpeta (Tabla) | Escribir en un archivo (Registro) |
| **Persistencia** | Los cambios suelen ser automáticos | Pueden revertirse (Rollback) si no hay Commit |

---

### Operaciones Fundamentales (DML y DDL)

#### 1. Acceso y Enumeración de Estructuras
Comandos iniciales para identificar el entorno de trabajo:

| Acción | MySQL / MariaDB | PostgreSQL |
| :--- | :--- | :--- |
| **Listar Bases de Datos** | `SHOW DATABASES;` | `\l` o `SELECT datname FROM pg_database;` |
| **Seleccionar Base de Datos** | `USE nombre_db;` | `\c nombre_db` |
| **Listar Tablas** | `SHOW TABLES;` | `\dt` o `SELECT tablename FROM pg_catalog.pg_tables;` |
| **Ver Estructura de Tabla** | `DESCRIBE nombre_tabla;` | `\d nombre_tabla` |

#### 2. Consultas y Extracción de Información (DQL)
Para obtener y filtrar datos específicos:
* **Selección global:** `SELECT * FROM nombre_tabla;`
* **Selección por columnas:** `SELECT columna1, columna2 FROM nombre_tabla;`
* **Filtrado de resultados:** `SELECT * FROM nombre_tabla WHERE columna = 'valor';`
* **Ordenamiento:** `SELECT * FROM nombre_tabla ORDER BY columna DESC;`

#### 3. Inserción y Manipulación de Datos (DML)
Comandos para poblar y actualizar la información:
* **Insertar datos:** `INSERT INTO nombre_tabla (columna1, columna2) VALUES ('dato1', 'dato2');`
* **Actualizar registros:** `UPDATE nombre_tabla SET columna = 'nuevo_valor' WHERE id = 1;`
* **Eliminar registros:** `DELETE FROM nombre_tabla WHERE id = 1;`

---

### Enumeración Avanzada de Metadatos
En entornos donde se desconocen los nombres de los objetos, se consulta el **Information Schema** (estándar ANSI):

* **Listar todas las tablas del sistema:**
    `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';`
* **Listar todas las columnas de una tabla específica:**
    `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'usuarios';`
* **Obtener versión del motor:**
    * **MySQL:** `SELECT @@version;`
    * **PostgreSQL:** `SELECT version();`

 
