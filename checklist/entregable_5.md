Crear un README.md que explique cómo ejecutar el sistema y cómo está organizado el proyecto.

Estructura del proyecto

blog_consola/
│
├── main.py
├── README.md
│
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── operaciones.py
    └── validaciones.py



# main.py
Debe ser el archivo principal del programa.

Desde este archivo se debe:

Importar las funciones y datos necesarios.
Iniciar el sistema.
Coordinar el flujo del menú.
Llamar a las funciones correspondientes según la opción elegida.
Proteger la ejecución principal con if __name__ == "__main__":.
Este archivo no debería contener toda la lógica del sistema. Su responsabilidad principal es orquestar las partes.

# blog/__init__.py
Debe existir dentro de la carpeta blog/.

Este archivo permite que Python reconozca la carpeta como un paquete.

Puede estar vacío.

# blog/datos.py
~~Debe contener las estructuras de datos base del sistema, por ejemplo:~~
~~perfil_autor~~
~~estados_post~~
~~etiquetas_blog~~
~~posts~~
~~Debe conservar la continuidad de los módulos anteriores.~~
~~El autor debe seguir siendo un diccionario anidado dentro de cada post.~~


# blog/menu.py
~~Debe contener la función encargada del menú y del manejo de input().~~

~~Por ejemplo, una función que:~~

~~Muestre las opciones disponibles.~~
~~Solicite una opción al usuario.~~
~~Retorne la opción elegida.~~
~~El menú sugerido es:~~
~~--- MENU DEL BLOG ---
~~1. Ver todos los posts~~
~~2. Buscar por titulo~~
~~3. Filtrar por tag~~
~~4. Validar posts~~
~~5. Salir~~

# blog/operaciones.py
~~Debe contener las funciones principales del blog, especialmente las relacionadas con búsqueda y filtrado.~~

~~Por ejemplo:~~

~~listar_posts(lista)~~
~~buscar_por_titulo(lista, termino)~~
~~filtrar_por_tag(lista, tag)~~

~~Estas funciones deben recibir datos por parámetro y no depender completamente de variables globales.~~

# blog/validaciones.py
~~Debe contener las reglas lógicas del sistema.~~

~~Como mínimo, debe incluir una función para validar posts.~~

~~La validación puede revisar:~~

~~Que el post sea un diccionario.~~
~~Que tenga las claves necesarias.~~
~~Que el título no esté vacío.~~
~~Que el contenido no esté vacío.~~
~~Que el autor sea un diccionario.~~
~~Que el autor tenga nombre.~~
~~Que los tags estén guardados como lista.~~
~~Que el estado sea válido.~~

# README.md
Debe explicar brevemente:

Qué hace el programa.
Cómo ejecutar el sistema.
Cómo está organizada la carpeta.
Qué responsabilidad cumple cada módulo.
Qué archivo se debe ejecutar.
