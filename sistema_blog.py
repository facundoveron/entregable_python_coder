# Datos del autor principal
perfil_autor = {
    "nombre": "Ana López",
    "bio": "Desarrolladora web y creadora de contenido sobre programación.",
    "especialidad": "Python y Django",
    "redes_sociales": ["@ana_dev", "@ana_python"]
}

# Estados válidos que puede tener un post
estados_post = ("borrador", "publicado", "archivado")

# Etiquetas permitidas en el blog (set para evitar duplicados)
etiquetas_blog = {"Python", "Django", "Web", "Backend", "Principiantes", "Listas"}

# Lista de posts para pruebas (incluye posts válidos e inválidos/incompletos)
posts = [
    {
        "id": 1,
        "titulo": "Primeros pasos con Python",
        "contenido": "En este post veremos cómo empezar a programar con Python.",
        "autor": perfil_autor,
        "tags": ["Python", "Principiantes"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Qué es Django",
        "contenido": "Django es un framework web creado con Python.",
        "autor": perfil_autor,
        "tags": ["Python", "Django", "Web"],
        "estado": "borrador"
    },
    {
        "id": 3,
        "titulo": "Organizando datos con listas",
        "contenido": "Las listas permiten guardar varios elementos en una sola variable.",
        "autor": perfil_autor,
        "tags": ["Python", "Listas"],
        "estado": "archivado"
    },
    {
        # Post incompleto (sin título, sin contenido y sin estado) para probar validaciones
        "id": 4,
        "autor": perfil_autor,
        "tags": ["Python", "Listas"],
    },
    {
        # Post incorrecto (autor como string y no como diccionario) para probar validaciones
        "id": 5,
        "titulo": "Publicación con autor inválido",
        "contenido": "Contenido de prueba con estructura de autor incorrecta.",
        "autor": "ana lopez",
        "tags": ["Python", "Listas"],
        "estado": "archivado"
    }
]


# --- Funciones de lógica y validación ---

def validar_post(post):
    """
    Verifica que el post cumpla con todas las reglas requeridas:
    1. Que el post sea un diccionario.
    2. Que existan todas las claves obligatorias.
    3. Que titulo no esté vacío.
    4. Que contenido no esté vacío.
    5. Que autor sea un diccionario.
    6. Que el autor tenga la clave nombre (no vacía).
    7. Que tags sea una lista.
    8. Que estado sea uno de los valores definidos en estados_post.
    Retorna True si es válido o False si encuentra algún error.
    """
    if not isinstance(post, dict):
        print("Error: El post debe ser un diccionario.")
        return False

    # 1. Comprobación de claves obligatorias
    claves_obligatorias = ["id", "titulo", "contenido", "autor", "tags", "estado"]
    for clave in claves_obligatorias:
        if clave not in post:
            print(f"Error: Al post le falta la clave obligatoria '{clave}'.")
            return False

    # 2. Validar título no vacío
    titulo = post.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip():
        print("Error: El campo 'titulo' no puede estar vacío.")
        return False

    # 3. Validar contenido no vacío
    contenido = post.get("contenido")
    if not isinstance(contenido, str) or not contenido.strip():
        print("Error: El campo 'contenido' no puede estar vacío.")
        return False

    # 4. Validar que autor sea un diccionario
    autor = post.get("autor")
    if not isinstance(autor, dict):
        print("Error: El campo 'autor' debe ser un diccionario.")
        return False

    # 5. Validar que el autor tenga la clave nombre y no esté vacía
    nombre_autor = autor.get("nombre")
    if not isinstance(nombre_autor, str) or not nombre_autor.strip():
        print("Error: El autor debe contener la clave 'nombre' y no estar vacía.")
        return False

    # 6. Validar que tags sea una lista
    tags = post.get("tags")
    if not isinstance(tags, list):
        print("Error: El campo 'tags' debe ser una lista.")
        return False

    # 7. Validar que estado sea uno de los definidos en estados_post
    estado = post.get("estado")
    if estado not in estados_post:
        print(f"Error: El estado '{estado}' no es válido. Estados permitidos: {estados_post}")
        return False

    print(f"Post '{post.get('titulo')}' es válido.")
    return True


def listar_posts(lista):
    """
    Muestra un resumen de cada post de la lista de forma segura (usando .get()).
    Retorna la lista de cadenas formateadas para cada post mostrado.
    """
    if not lista:
        print("No hay posts disponibles para mostrar.")
        return []

    resumen = []
    for post in lista:
        if not isinstance(post, dict):
            continue
        titulo = post.get("titulo", "Sin título")
        autor = post.get("autor")
        nombre_autor = autor.get("nombre", "Desconocido") if isinstance(autor, dict) else "Desconocido"
        linea = f"- {titulo} | Autor: {nombre_autor}"
        print(linea)
        resumen.append(linea)
    return resumen

# Alias para compatibilidad con singular y plural
listar_post = listar_posts


def buscar_por_titulo(lista, termino):
    """
    Busca posts cuyo título contenga el término especificado (insensible a mayúsculas).
    Retorna una lista con los posts que coincidan.
    """
    if not isinstance(termino, str) or not termino:
        return []

    termino_busqueda = termino.lower()
    resultados = []
    for post in lista:
        if isinstance(post, dict):
            titulo = post.get("titulo")
            if isinstance(titulo, str) and termino_busqueda in titulo.lower():
                resultados.append(post)
    return resultados


def filtrar_por_tag(lista, tag):
    """
    Filtra posts que contengan el tag especificado (insensible a mayúsculas).
    Retorna una lista con los posts coincidentes.
    """
    if not isinstance(tag, str) or not tag:
        return []

    tag_busqueda = tag.lower()
    resultados = []
    for post in lista:
        if isinstance(post, dict):
            tags = post.get("tags")
            if isinstance(tags, list):
                if any(isinstance(t, str) and t.lower() == tag_busqueda for t in tags):
                    resultados.append(post)
    return resultados


# --- Funciones de Menú e Interacción ---

def mostrar_menu():
    """
    Muestra las opciones del menú y retorna la opción ingresada por el usuario.
    Usa try-except para capturar y validar la entrada numérica.
    """
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar post")
    print("5. Salir")

    try:
        opcion = int(input("Ingresa tu opcion: "))
        return opcion
    except ValueError:
        print("Opción inválida, intenta de nuevo (debes ingresar un número).")
        return None


def menu():
    """Mantiene el menú interactivo activo y despacha a las funciones correspondientes."""
    while True:
        opcion = mostrar_menu()

        if opcion is None:
            continue

        if opcion == 1:
            print("\nPosts disponibles:")
            listar_posts(posts)

        elif opcion == 2:
            termino = input("Buscar por titulo: ")
            resultados = buscar_por_titulo(posts, termino)
            if resultados:
                print(f"\nResultados encontrados ({len(resultados)}):")
                for post in resultados:
                    print(f"- {post.get('titulo')}")
            else:
                print(f"No se encontraron posts que contengan '{termino}'.")

        elif opcion == 3:
            tag = input("Ingresa un tag: ")
            resultados = filtrar_por_tag(posts, tag)
            if resultados:
                print(f"\nPosts con el tag '{tag}' ({len(resultados)}):")
                for post in resultados:
                    print(f"- {post.get('titulo')}")
            else:
                print(f"No se encontraron posts con el tag '{tag}'.")

        elif opcion == 4:
            print("\n--- VALIDACIÓN DE POSTS ---")
            for post in posts:
                es_valido = validar_post(post)
                if not es_valido:
                    print(f"-> Post con errores: {post}")
                print("-" * 35)

        elif opcion == 5:
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intenta de nuevo")


# Arranca el programa si lo ejecutamos directamente
if __name__ == "__main__":
    menu()