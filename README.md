# Sistema de Gestión de Blog por Consola

Este proyecto es una aplicación interactiva por consola desarrollada en Python que simula la gestión y consulta de publicaciones (posts) de un blog.

---

## 1. ¿Qué hace el programa?

El sistema permite gestionar y consultar información de un blog a través de un menú interactivo. Sus funcionalidades principales incluyen:
- **Listar publicaciones:** Muestra todas las publicaciones disponibles junto con el nombre de su autor de forma segura.
- **Buscar por título:** Permite encontrar publicaciones que contengan una palabra o término específico en su título (búsqueda no sensible a mayúsculas/minúsculas).
- **Filtrar por etiqueta (*tag*):** Permite obtener todos los posts asociados a una etiqueta temática determinada.
- **Validar publicaciones:** Analiza la integridad y formato de cada post (claves obligatorias, campos no vacíos, estructura de autor y estados permitidos).

---

## 2. ¿Qué archivo se debe ejecutar?

El punto de entrada del programa es:
```bash
main.py
```

---

## 3. ¿Cómo ejecutar el sistema?

### Requisitos previos
- Tener instalado **Python 3.8** o superior.

### Pasos de ejecución
1. Abrir una terminal o consola de comandos.
2. Navegar hasta el directorio raíz del proyecto:
   ```bash
   cd "ruta/al/proyecto"
   ```
3. Ejecutar el archivo principal con Python:
   ```bash
   python main.py
   ```
---

## 4. ¿Cómo está organizada la carpeta?

La estructura del proyecto sigue un diseño modular para separar datos, lógica e interfaz:

```text
blog_consola/
│
├── main.py               # Archivo principal de ejecución y orquestación
├── README.md             # Documentación general del proyecto
│
└── blog/                 # Paquete modular del sistema
    ├── __init__.py       # Indica que la carpeta es un paquete de Python
    ├── datos.py          # Estructuras de datos base y posts de prueba
    ├── menu.py           # Menú interactivo y captura de opciones del usuario
    ├── operaciones.py    # Lógica de búsqueda, filtrado y listado de posts
    └── validaciones.py   # Reglas de validación e integridad de datos
```

---

## 5. ¿Qué responsabilidad cumple cada módulo?

- **`main.py`**:
  Es el orquestador principal del sistema. Importa las funciones y datos necesarios, controla el ciclo del menú interactivo, despacha las acciones según la opción elegida por el usuario y protege la ejecución mediante el bloque `if __name__ == "__main__":`.

- **`blog/__init__.py`**:
  Define la carpeta `blog/` como un paquete de Python, permitiendo importar sus módulos desde cualquier parte del proyecto.

- **`blog/datos.py`**:
  Centraliza y define las estructuras de datos base:
  - `perfil_autor`: Diccionario con la información del autor.
  - `estados_post`: Tupla con los estados válidos (`"borrador"`, `"publicado"`, `"archivado"`).
  - `etiquetas_blog`: Conjunto (*set*) con las etiquetas válidas del blog.
  - `posts`: Lista de diccionarios con posts de prueba (válidos e incompletos para pruebas de validación).

- **`blog/menu.py`**:
  Se encarga de la interfaz con el usuario en la terminal. Imprime el menú de opciones (`mostrar_menu()`) y procesa de forma segura la entrada con manejo de excepciones (`try-except`) ante valores no numéricos.

- **`blog/operaciones.py`**:
  Contiene las funciones principales de consulta y manipulación de datos, recibiendo parámetros para evitar acoplamiento:
  - `listar_posts(lista)`: Muestra el listado formateado de publicaciones.
  - `buscar_por_titulo(lista, termino)`: Filtra publicaciones por coincidencia de texto en el título.
  - `filtrar_por_tag(lista, tag)`: Filtra publicaciones que contengan una etiqueta específica.

- **`blog/validaciones.py`**:
  Implementa las reglas de integridad del sistema a través de `validar_post(post)`. Verifica que el post sea un diccionario, contenga todas las claves requeridas (`id`, `titulo`, `contenido`, `autor`, `tags`, `estado`), tenga tipos de datos correctos, datos no vacíos y estados válidos.
