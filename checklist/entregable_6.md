# Clase Blog
~~La clase Blog debe centralizar la lógica principal del sistema.~~
~~Debe tener un atributo que sea una lista de objetos Post.~~
~~Esa clase puede incluir métodos para:~~ 

~~Listar posts.~~
~~Buscar posts por título.~~
~~Filtrar posts por tag.~~
~~Crear un nuevo post.~~
~~Validar posts.~~
~~Obtener todos los posts cargados.~~

La idea es que la clase Blog sea el punto principal desde donde se maneja la colección de publicaciones.

# Conversión entre objetos y diccionarios
Como JSON no puede guardar objetos personalizados directamente, vas a necesitar convertir los objetos a estructuras compatibles.

Para guardar datos en JSON, los objetos deben convertirse a diccionarios.

Por ejemplo:

Un objeto Autor debe poder representarse como diccionario.
Un objeto Post debe poder representarse como diccionario.
La lista de posts del blog debe poder convertirse en una lista de diccionarios.
También debe existir alguna forma de reconstruir objetos a partir de los diccionarios cargados desde JSON.

No hace falta que uses un nombre obligatorio, pero pueden ser métodos o funciones con responsabilidades como:

Convertir un autor a diccionario.
Convertir un post a diccionario.
Crear un autor desde un diccionario.
Crear un post desde un diccionario.

# Persistencia con JSON en blog/datos.py
El archivo blog/datos.py debe encargarse de la carga y guardado de datos.

Debés modificarlo o ampliarlo para trabajar con un archivo llamado:



posts.json
Al iniciar el programa, se deben cargar los posts desde ese archivo.

Si el archivo no existe, está vacío o tiene datos inválidos, el programa debe manejar la situación sin cerrarse inesperadamente.

También debe existir una función para guardar los posts actuales en posts.json.

# Crear nuevos posts
El menú debe permitir crear un nuevo post desde consola.

Al crear un nuevo post:

Se deben pedir los datos necesarios al usuario.
Se debe crear una instancia de Post.
Esa instancia debe agregarse al objeto Blog.
El post debe poder convertirse a diccionario para guardarse en posts.json.
Esto permite verificar que la persistencia JSON realmente funcione con objetos nuevos creados durante la ejecución.

6. Integración del menú
El sistema debe seguir funcionando desde consola.

En main.py, se debe instanciar la clase Blog.

El menú debe interactuar con esa instancia de Blog, llamando a sus métodos para listar, buscar, filtrar, crear y validar posts.

El menú sugerido es:



--- MENU DEL BLOG ---
1. Ver todos los posts
2. Buscar por titulo
3. Filtrar por tag
4. Crear nuevo post
5. Validar posts
6. Guardar posts en JSON
7. Salir
No es obligatorio que el menú sea exactamente igual, pero debe permitir probar las funcionalidades principales del checkpoint.

7. Integración en main.py
El archivo main.py debe ser el punto de entrada del programa.

Debe encargarse de:

Importar las clases y funciones necesarias.
Cargar los datos desde posts.json.
Crear una instancia de Blog.
Mostrar el menú.
Llamar a los métodos correspondientes según la opción elegida.
Guardar los datos cuando corresponda.
Proteger la ejecución principal con if __name__ == "__main__":.
La lógica principal del sistema no debería quedar toda escrita en main.py.

8. Actualización del README
El archivo README.md debe actualizarse.

Debe explicar:

Qué hace el sistema.
Cómo ejecutar el programa.
Qué clases principales existen.
Qué responsabilidad tiene cada clase.
Cómo interactúan las clases con el archivo posts.json.
Cómo se guarda y carga la información.
Qué cambió respecto al checkpoint anterior.


Funcionalidades requeridas
Opción 1: Ver todos los posts
El programa debe mostrar los posts cargados actualmente en el blog.

Debe mostrar, como mínimo:

Título.
Autor.
Estado.
Esta funcionalidad debe usar la instancia de la clase Blog.

Opción 2: Buscar por título
El programa debe permitir buscar publicaciones por título.

La búsqueda debe ignorar mayúsculas y minúsculas.

Esta funcionalidad debe resolverse mediante un método de la clase Blog.

Opción 3: Filtrar por tag
El programa debe permitir filtrar publicaciones según una etiqueta.

El filtrado debe ignorar mayúsculas y minúsculas.

Esta funcionalidad debe resolverse mediante un método de la clase Blog.

Opción 4: Crear nuevo post
El programa debe permitir crear un nuevo post desde consola.

El nuevo post debe crearse como una instancia de la clase Post.

Luego debe agregarse a la lista de posts del objeto Blog.

Opción 5: Validar posts
El programa debe poder validar que los posts tengan datos correctos.

Puede hacerlo mediante métodos de la clase Blog, funciones del módulo validaciones.py o una combinación de ambos.

Lo importante es que la validación siga existiendo y funcione con la nueva estructura orientada a objetos.

Opción 6: Guardar posts en JSON
El programa debe guardar los posts actuales en el archivo posts.json.

Para eso, los objetos deben convertirse a diccionarios compatibles con JSON.

Opción 7: Salir
El programa debe mostrar un mensaje de despedida y finalizar correctamente.

Podés decidir si el programa guarda automáticamente antes de salir o si el guardado queda como opción manual del menú.

Manejo de errores
El programa debe evitar cerrarse inesperadamente.

Debe manejar, como mínimo:

El archivo posts.json no existe.
El archivo posts.json está vacío.
El archivo posts.json tiene contenido inválido.
El usuario ingresa una opción incorrecta en el menú.
El usuario deja campos vacíos al crear un post.
Se intenta guardar un objeto sin convertirlo antes a diccionario.
Se intenta reconstruir un objeto desde un diccionario incompleto.
Los mensajes de error deben ser claros y ayudar a entender qué ocurrió.



Criterios de aceptación
Para considerar este checkpoint como completado, tu proyecto debe cumplir con los siguientes puntos:

Continuar sobre el repositorio de GitHub del módulo anterior.
Mantener una estructura modular.
Incluir el archivo blog/modelos.py.
Definir la clase Autor.
Definir la clase Post.
Definir la clase Blog.
La clase Post debe recibir una instancia de Autor.
La clase Blog debe tener una lista de objetos Post.
La clase Blog debe centralizar la lógica principal del sistema.
El programa debe cargar datos desde posts.json al iniciar.
El programa debe poder guardar datos en posts.json.
Los objetos deben convertirse a diccionarios antes de guardarse en JSON.
Los diccionarios cargados desde JSON deben convertirse nuevamente en objetos.
El menú debe usar una instancia de Blog.
El programa debe permitir listar posts.
El programa debe permitir buscar posts por título.
El programa debe permitir filtrar posts por tag.
El programa debe permitir crear un nuevo post.
El programa debe permitir guardar posts en JSON.
La búsqueda y el filtrado deben ignorar mayúsculas y minúsculas.
El programa debe manejar errores de archivo con claridad.
main.py debe usar if __name__ == "__main__":.
El README.md debe estar actualizado.
Los cambios deben subirse al repositorio de GitHub.