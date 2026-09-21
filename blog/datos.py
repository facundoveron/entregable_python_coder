import os
import json

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

# Posts iniciales de demostración en formato diccionario
posts_iniciales = [
    {
        "id": 1,
        "titulo": "Primeros pasos con Python",
        "contenido": "Aprende los conceptos básicos de sintaxis, variables y estructuras de control.",
        "autor": perfil_autor,
        "tags": ["Python", "Principiantes"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Qué es Django y cómo empezar",
        "contenido": "Una introducción al framework web más popular para Python.",
        "autor": perfil_autor,
        "tags": ["Python", "Django", "Web"],
        "estado": "publicado"
    },
    {
        "id": 3,
        "titulo": "Organizando datos con listas",
        "contenido": "Guía práctica sobre el uso de listas, métodos comunes y mejores prácticas.",
        "autor": perfil_autor,
        "tags": ["Python", "Listas"],
        "estado": "borrador"
    }
]

# Lista expuesta para compatibilidad
posts = list(posts_iniciales)


def verificar_si_existe_el_archivo(ruta="posts.json"):
    """Comprueba si un archivo existe en el sistema de archivos."""
    return os.path.exists(ruta)


def convertir_dict_en_autor(autor_dict):
    """Convierte un diccionario en una instancia de la clase Autor."""
    from blog.modelos import Autor
    if isinstance(autor_dict, Autor):
        return autor_dict
    if not isinstance(autor_dict, dict):
        return Autor(nombre=str(autor_dict) if autor_dict else "Desconocido")

    return Autor(
        nombre=autor_dict.get("nombre", "Desconocido"),
        bio=autor_dict.get("bio", ""),
        especialidad=autor_dict.get("especialidad", ""),
        redes_sociales=autor_dict.get("redes_sociales", [])
    )


def convertir_dict_en_post(post_dict):
    """Convierte un diccionario en una instancia de la clase Post."""
    from blog.modelos import Post, Autor
    if isinstance(post_dict, Post):
        return post_dict
    if not isinstance(post_dict, dict):
        raise ValueError("El post debe ser un diccionario para poder convertirse a objeto Post")

    autor_data = post_dict.get("autor")
    if isinstance(autor_data, Autor):
        autor = autor_data
    elif isinstance(autor_data, dict):
        autor = convertir_dict_en_autor(autor_data)
    else:
        autor = Autor(nombre=str(autor_data) if autor_data else "Desconocido")

    return Post(
        id=post_dict.get("id"),
        titulo=post_dict.get("titulo", "Sin título"),
        contenido=post_dict.get("contenido", ""),
        autor=autor,
        tags=post_dict.get("tags", []),
        estado=post_dict.get("estado", "borrador")
    )


def convertir_autor_en_dict(autor):
    """Convierte un objeto Autor en un diccionario compatible con JSON."""
    from blog.modelos import Autor
    if isinstance(autor, dict):
        return autor
    if isinstance(autor, Autor):
        return autor.to_dict()
    return {
        "nombre": str(autor) if autor else "Desconocido",
        "bio": "",
        "especialidad": "",
        "redes_sociales": []
    }


def convertir_post_en_dict(post, autor_dict=None):
    """Convierte un objeto Post en un diccionario compatible con JSON."""
    from blog.modelos import Post, Autor
    if isinstance(post, dict):
        return post
    if isinstance(post, Post):
        return post.to_dict()

    autor_final = autor_dict if autor_dict is not None else {}
    return {
        "id": getattr(post, "id", None),
        "titulo": getattr(post, "titulo", "Sin título"),
        "contenido": getattr(post, "contenido", ""),
        "autor": autor_final,
        "tags": getattr(post, "tags", []),
        "estado": getattr(post, "estado", "borrador")
    }


def cargar_en_memoria_post(ruta="posts.json"):
    """
    Carga los posts desde el archivo JSON especificado.
    Maneja de forma segura si el archivo no existe, está vacío o contiene JSON inválido.
    Retorna una lista de objetos Post.
    """
    posts_objetos = []
    if not verificar_si_existe_el_archivo(ruta):
        print(f"Información: El archivo '{ruta}' no existe. Se inicializará con lista vacía.")
        return posts_objetos

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                print(f"Información: El archivo '{ruta}' está vacío.")
                return posts_objetos

            datos = json.loads(contenido)
            if not isinstance(datos, list):
                print(f"Advertencia: El contenido de '{ruta}' no es una lista válida.")
                return posts_objetos

            for item in datos:
                try:
                    if isinstance(item, dict):
                        post_obj = convertir_dict_en_post(item)
                        posts_objetos.append(post_obj)
                except Exception as error_item:
                    print(f"Error al procesar un post del archivo: {error_item}")

    except json.JSONDecodeError:
        print(f"Error: El archivo '{ruta}' contiene datos con formato JSON inválido.")
    except Exception as e:
        print(f"Error inesperado al leer '{ruta}': {e}")

    return posts_objetos


def guardar_todos_los_posts(lista_posts, ruta="posts.json"):
    """
    Guarda una lista de objetos Post o diccionarios en el archivo JSON especificado.
    Retorna True si se guardó correctamente o False en caso de error.
    """
    try:
        lista_dicts = []
        for p in lista_posts:
            if hasattr(p, "to_dict"):
                lista_dicts.append(p.to_dict())
            elif isinstance(p, dict):
                lista_dicts.append(p)
            else:
                lista_dicts.append(convertir_post_en_dict(p))

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(lista_dicts, archivo, indent=4, ensure_ascii=False)

        print(f"Se guardaron exitosamente {len(lista_dicts)} posts en '{ruta}'.")
        return True
    except Exception as e:
        print(f"Error al guardar los posts en '{ruta}': {e}")
        return False


def guardar_post(post, ruta="posts.json"):
    """
    Guarda o anexa un post en el archivo JSON.
    """
    post_dict = post.to_dict() if hasattr(post, "to_dict") else convertir_post_en_dict(post)

    lista_posts = []
    if verificar_si_existe_el_archivo(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                if contenido:
                    datos = json.loads(contenido)
                    if isinstance(datos, list):
                        lista_posts = datos
        except Exception:
            lista_posts = []

    lista_posts.append(post_dict)

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(lista_posts, archivo, indent=4, ensure_ascii=False)
        print("Post guardado exitosamente.")
        return True
    except Exception as e:
        print(f"Error al guardar el post: {e}")
        return False