# Sistema de Gestión de Blog por Consola

Este proyecto es una aplicación interactiva por consola desarrollada en Python que implementa los principios de la **Programación Orientada a Objetos (POO)** y la **persistencia de datos en archivos JSON** para la gestión completa de publicaciones (posts) y autores de un blog.

---

## 1. ¿Qué hace el sistema?

El sistema proporciona un entorno interactivo en consola para administrar el ciclo de vida de publicaciones en un blog. Permite:
- **Listar publicaciones:** Visualizar todas las publicaciones registradas con su título, autor y estado actual.
- **Buscar publicaciones por título:** Realizar búsquedas por coincidencia de texto (sin distinción entre mayúsculas y minúsculas).
- **Filtrar publicaciones por etiqueta (*tag*):** Consultar publicaciones asociadas a una temática específica.
- **Validar publicaciones:** Verificar la integridad estructural y las reglas de negocio de los posts cargados en el sistema.
- **Crear nuevas publicaciones:** Formulario interactivo guiado con validaciones estrictas para registrar nuevos posts y persistirlos en disco.
- **Persistencia continua:** Cargar y guardar información de forma automática en un archivo `posts.json`.

---

## 2. ¿Cómo ejecutar el programa?

### Requisitos previos
- **Python 3.8** o superior instalado en el sistema.

### Pasos para la ejecución
1. Abrir una terminal o consola de comandos.
2. Navegar al directorio raíz del proyecto:
   ```bash
   cd "ruta/al/proyecto"
   ```
3. Ejecutar el archivo principal:
   ```bash
   python main.py
   ```

El punto de entrada del programa es [main.py](file:///c:/Users/Facundo/Documents/Python%20Coder/main.py).

---

## 3. Clases Principales y Responsabilidades

El sistema adopta el paradigma de Programación Orientada a Objetos ubicado en el módulo [blog/modelos.py](file:///c:/Users/Facundo/Documents/Python%20Coder/blog/modelos.py):

| Clase | Responsabilidad Principal | Atributos / Métodos Clave |
| :--- | :--- | :--- |
| **`Autor`** | Modela y encapsula los datos del autor de una publicación. | **Atributos:** `nombre`, `bio`, `especialidad`, `redes_sociales`.<br>**Métodos:** `to_dict()`, `from_dict(data)`. |
| **`Post`** | Representa una publicación individual del blog, vinculando su contenido con una instancia de `Autor` y sus metadatos. | **Atributos:** `id`, `titulo`, `contenido`, `autor` (objeto `Autor`), `tags` (lista de etiquetas), `estado` (`"borrador"`, `"publicado"`, `"archivado"`).<br>**Métodos:** `to_dict()`, `from_dict(data)`. |
| **`Blog`** | Entidad controladora y administradora del blog en memoria. Gestiona la colección de publicaciones y centraliza la lógica de negocio. | **Atributos:** `posts` (lista de objetos `Post`), `tags`, `ruta_archivo`.<br>**Métodos:** `listar_posts()`, `buscar_por_titulo(termino)`, `filtrar_por_tag(tag)`, `agregar_post(post)`, `crear_post()`, `validar_posts()`, `guardar_en_json(ruta)`, `cargar_desde_json(ruta)`, `obtener_posts()`, `to_dict_list()`. |

---

## 4. Interacción con el archivo `posts.json`

La comunicación entre los objetos en memoria (`Blog`, `Post`, `Autor`) y el archivo de almacenamiento [posts.json](file:///c:/Users/Facundo/Documents/Python%20Coder/posts.json) se realiza a través de una capa de serialización y deserialización definida en [blog/datos.py](file:///c:/Users/Facundo/Documents/Python%20Coder/blog/datos.py):

```
       [ posts.json ]  (Almacenamiento en disco)
             │
             ▲  (json.load / json.dump)
             ▼
   [ blog/datos.py ]  (Capa de Persistencia & Transformación)
             │
     ┌───────┴────────────────────────┐
     ▼ Deserialización                ▼ Serialización
 (dict -> Objetos)                (Objetos -> dict)
     │                                │
     ▼                                ▲
[ Instancias Post & Autor ] ◄───► [ Clase Blog ]
```

1. **Lectura y Deserialización:** `posts.json` almacena diccionarios en formato JSON. `blog/datos.py` los transforma en instancias vivas de `Autor` y `Post` para que la clase `Blog` opere con objetos tipados.
2. **Escritura y Serialización:** Cuando se guardan los posts, los objetos `Post` y `Autor` son transformados nuevamente en estructuras de diccionarios compatibles con JSON para escribirse de forma estructurada e indentada en `posts.json`.

---

## 5. ¿Cómo se guarda y carga la información?

### Carga de información (`cargar_en_memoria_post`)
1. **Verificación de archivo:** Se comprueba si `posts.json` existe en la ruta de trabajo mediante `verificar_si_existe_el_archivo()`. Si no existe, se notifica y se inicializa la colección vacía sin fallar.
2. **Lectura segura:** Se abre el archivo en modo lectura (`"r"`, `utf-8`) y se procesa. Si el archivo está vacío (0 bytes) o tiene formato corrupto, se captura la excepción `json.JSONDecodeError` evitando que el programa se detenga.
3. **Conversión a objetos:** Cada diccionario de la lista se convierte mediante:
   - `convertir_dict_en_autor(autor_dict)` / `Autor.from_dict()`: Instancia un objeto `Autor`.
   - `convertir_dict_en_post(post_dict)` / `Post.from_dict()`: Instancia un objeto `Post` asociando el objeto `Autor` generado.
4. **Inicialización:** La lista resultante de objetos `Post` se asigna a `self.posts` al instanciar `Blog()`.

### Guardado de información (`guardar_todos_los_posts` y `guardar_post`)
1. **Conversión a diccionarios:**
   - `Post.to_dict()` y `Autor.to_dict()`: Extraen los datos estructurados a diccionarios puros de Python.
2. **Actualización del archivo:**
   - Se serializa la lista completa de diccionarios en `posts.json` utilizando `json.dump(..., indent=4, ensure_ascii=False)`.

---

## 6. Estructura del Proyecto

```text
blog_consola/
│
├── main.py               # Orquestador del programa y ciclo del menú
├── README.md             # Documentación técnica general
├── posts.json            # Base de datos persistente en formato JSON
│
├── blog/                 # Paquete principal del blog
│   ├── __init__.py       # Inicializador del paquete Python
│   ├── modelos.py        # Clases principales: Autor, Post y Blog
│   ├── datos.py          # Lógica de persistencia, carga y guardado en JSON
│   ├── menu.py           # Interfaz de usuario por terminal (7 opciones)
│   ├── validaciones.py   # Funciones de validación para entradas del usuario y posts
│   └── operaciones.py    # Módulo auxiliar para utilidades y compatibilidad
│
└── tests/                # Pruebas automatizadas del sistema
    ├── __init__.py
    └── test_sistema_blog.py
```

---

## 7. ¿Qué cambió respecto al checkpoint anterior?

En este checkpoint se implementó una evolución arquitectónica significativa respecto a la versión anterior:

| Aspecto | Checkpoint Anterior (Entregable 5) | Checkpoint Actual (Entregable 6 / POO & JSON) |
| :--- | :--- | :--- |
| **Paradigma** | Programación estructurada / procedural basada en diccionarios. | **Programación Orientada a Objetos (POO)** con clases (`Autor`, `Post`, `Blog`). |
| **Almacenamiento** | Datos estáticos en memoria definidos en `datos.py` (se reiniciaban al cerrar). | **Persistencia real en disco** mediante el archivo `posts.json`. |
| **Manejo de Datos** | Diccionarios anidados directos. | **Modelos tipados y métodos de conversión** (`to_dict` / `from_dict`). |
| **Creación de Posts** | No permitía agregar nuevos posts desde el menú. | **Nueva opción interactiva (Crear Post)** con validación en tiempo real de campos, estado y etiquetas permitidas. |
| **Lógica de Negocio** | Funciones sueltas en `operaciones.py`. | **Métodos encapsulados** dentro de la clase `Blog`. |
| **Opciones de Menú** | 6 opciones simples. | **7 opciones integradas con persistencia manual/automática en JSON**. |
