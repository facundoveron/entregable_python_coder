
from blog.datos import estados_post


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
