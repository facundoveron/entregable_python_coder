from blog.datos import estados_post, etiquetas_blog


def validar_input_texto(mensaje):
    """
    Solicita una entrada de texto no vacía al usuario y valida que no esté en blanco.
    """
    while True:
        valor = input(mensaje)
        if valor and isinstance(valor, str) and valor.strip():
            return valor.strip()
        else:
            print("Error: El texto no puede estar vacío. Por favor ingrese un valor válido.")


def validar_input_estado(mensaje):
    """
    Solicita un estado al usuario y valida que pertenezca a la tupla estados_post.
    """
    while True:
        valor = input(mensaje).strip().lower()
        if valor in estados_post:
            return valor
        else:
            print(f"Error: Estado no válido. Debe ser uno de los siguientes: {', '.join(estados_post)}")


def validar_input_etiquetas(mensaje):
    """
    Solicita una o más etiquetas al usuario y valida que no estén vacías.
    """
    etiquetas = []
    while True:
        valor = input(mensaje).strip()
        if valor:
            if valor not in etiquetas:
                etiquetas.append(valor)
            if validar_agregar_mas_etiquetas():
                continue
            else:
                return etiquetas
        else:
            print("Error: La etiqueta no puede estar vacía.")


def validar_agregar_mas_etiquetas():
    """
    Pregunta al usuario si desea continuar agregando etiquetas ('s' o 'n').
    """
    while True:
        decision = input("¿Deseas agregar más etiquetas? (s/n): ").strip().lower()
        if decision in ("s", "n"):
            return decision == "s"
        else:
            print("Error: Por favor ingresa únicamente 's' (sí) o 'n' (no).")


def validar_post(post):
    """
    Verifica que el post cumpla con todas las reglas requeridas:
    1. Que el post sea un diccionario o una instancia de Post.
    2. Que existan todas las claves/atributos obligatorios: id, titulo, contenido, autor, tags, estado.
    3. Que titulo no esté vacío.
    4. Que contenido no esté vacío.
    5. Que autor sea un diccionario o instancia de Autor con nombre no vacío.
    6. Que tags sea una lista.
    7. Que estado sea uno de los valores válidos en estados_post.
    Retorna True si es válido o False si encuentra algún error.
    """
    if post is None:
        return False

    # Si es una instancia de clase Post
    if hasattr(post, "to_dict"):
        post = post.to_dict()

    if not isinstance(post, dict):
        return False

    # 1. Comprobación de claves obligatorias
    claves_obligatorias = ["id", "titulo", "contenido", "autor", "tags", "estado"]
    for clave in claves_obligatorias:
        if clave not in post:
            return False

    # 2. Validar título no vacío
    titulo = post.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip():
        return False

    # 3. Validar contenido no vacío
    contenido = post.get("contenido")
    if not isinstance(contenido, str) or not contenido.strip():
        return False

    # 4. Validar que autor sea un diccionario con nombre no vacío
    autor = post.get("autor")
    if isinstance(autor, dict):
        nombre_autor = autor.get("nombre")
        if not isinstance(nombre_autor, str) or not nombre_autor.strip():
            return False
    elif hasattr(autor, "nombre"):
        if not isinstance(autor.nombre, str) or not autor.nombre.strip():
            return False
    else:
        return False

    # 5. Validar que tags sea una lista
    tags = post.get("tags")
    if not isinstance(tags, list):
        return False

    # 6. Validar que estado sea uno de los definidos en estados_post
    estado = post.get("estado")
    if estado not in estados_post:
        return False

    return True