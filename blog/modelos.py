from blog.validaciones import (
    validar_input_texto,
    validar_input_estado,
    validar_input_etiquetas,
    validar_post
)
from blog.datos import (
    estados_post,
    etiquetas_blog,
    guardar_post,
    guardar_todos_los_posts,
    cargar_en_memoria_post
)


class Autor:
    """Modela y encapsula la información de un autor de publicaciones."""

    def __init__(self, nombre, bio="", especialidad="", redes_sociales=None):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        self.redes_sociales = list(redes_sociales) if redes_sociales is not None else []

    def to_dict(self):
        """Convierte la instancia de Autor a un diccionario compatible con JSON."""
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": list(self.redes_sociales)
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruye una instancia de Autor a partir de un diccionario."""
        if not isinstance(data, dict):
            raise ValueError("Los datos para Autor deben ser un diccionario.")
        return cls(
            nombre=data.get("nombre", "Desconocido"),
            bio=data.get("bio", ""),
            especialidad=data.get("especialidad", ""),
            redes_sociales=data.get("redes_sociales", [])
        )

    def __repr__(self):
        return f"Autor(nombre='{self.nombre}')"


class Post:
    """Representa una publicación del blog vinculada a un Autor."""

    def __init__(self, id, titulo, contenido, autor, tags=None, estado="borrador"):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido

        if isinstance(autor, Autor):
            self.autor = autor
        elif isinstance(autor, dict):
            self.autor = Autor.from_dict(autor)
        elif isinstance(autor, str):
            self.autor = Autor(nombre=autor)
        else:
            self.autor = Autor(nombre=str(autor) if autor else "Desconocido")

        self.tags = list(tags) if tags is not None else []
        self.estado = estado

    def to_dict(self):
        """Convierte la instancia de Post a un diccionario compatible con JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.to_dict() if isinstance(self.autor, Autor) else {"nombre": str(self.autor)},
            "tags": list(self.tags),
            "estado": self.estado
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruye una instancia de Post a partir de un diccionario."""
        if not isinstance(data, dict):
            raise ValueError("Los datos para Post deben ser un diccionario.")
        return cls(
            id=data.get("id"),
            titulo=data.get("titulo", "Sin título"),
            contenido=data.get("contenido", ""),
            autor=data.get("autor"),
            tags=data.get("tags", []),
            estado=data.get("estado", "borrador")
        )

    def __repr__(self):
        nombre_autor = self.autor.nombre if isinstance(self.autor, Autor) else str(self.autor)
        return f"Post(id={self.id}, titulo='{self.titulo}', autor='{nombre_autor}', estado='{self.estado}')"


class Blog:
    """Centraliza la lógica principal y la colección de publicaciones del sistema."""

    def __init__(self, posts=None, tags=None, ruta_archivo="posts.json"):
        self.ruta_archivo = ruta_archivo
        self.tags = set(tags) if tags is not None else set(etiquetas_blog)

        if posts is None:
            self.posts = cargar_en_memoria_post(self.ruta_archivo)
        else:
            self.posts = []
            for p in posts:
                if isinstance(p, Post):
                    self.posts.append(p)
                elif isinstance(p, dict):
                    self.posts.append(Post.from_dict(p))

    def listar_posts(self):
        """
        Muestra un resumen de cada post de la lista en consola.
        Muestra como mínimo: Título, Autor y Estado.
        Retorna la lista de cadenas formateadas para cada post mostrado.
        """
        if not self.posts:
            print("No hay posts disponibles para mostrar.")
            return []

        resumen = []
        for post in self.posts:
            titulo = post.titulo if (isinstance(post, Post) and post.titulo) else "Sin título"
            if isinstance(post, Post) and isinstance(post.autor, Autor):
                nombre_autor = post.autor.nombre
            elif isinstance(post, dict):
                autor_val = post.get("autor")
                nombre_autor = autor_val.get("nombre", "Desconocido") if isinstance(autor_val, dict) else str(autor_val)
            else:
                nombre_autor = "Desconocido"

            estado = post.estado if isinstance(post, Post) else (post.get("estado", "Desconocido") if isinstance(post, dict) else "Desconocido")
            linea = f"- {titulo} | Autor: {nombre_autor} | Estado: {estado}"
            print(linea)
            resumen.append(linea)
        return resumen

    def buscar_por_titulo(self, termino):
        """
        Busca posts cuyo título contenga el término especificado (insensible a mayúsculas).
        Retorna una lista con las instancias de Post que coincidan.
        """
        if not isinstance(termino, str) or not termino.strip():
            return []

        termino_busqueda = termino.strip().lower()
        resultados = []
        for post in self.posts:
            if isinstance(post, Post) and post.titulo:
                if termino_busqueda in post.titulo.lower():
                    resultados.append(post)
            elif isinstance(post, dict):
                titulo = post.get("titulo", "")
                if isinstance(titulo, str) and termino_busqueda in titulo.lower():
                    resultados.append(post)
        return resultados

    def filtrar_por_tag(self, tag):
        """
        Filtra posts que contengan el tag especificado (insensible a mayúsculas).
        Retorna una lista con las instancias de Post coincidentes.
        """
        if not isinstance(tag, str) or not tag.strip():
            return []

        tag_busqueda = tag.strip().lower()
        resultados = []
        for post in self.posts:
            tags_lista = post.tags if isinstance(post, Post) else (post.get("tags") if isinstance(post, dict) else None)
            if isinstance(tags_lista, list):
                if any(isinstance(t, str) and t.strip().lower() == tag_busqueda for t in tags_lista):
                    resultados.append(post)
        return resultados

    def agregar_post(self, post):
        """Agrega un post a la colección si es válido."""
        if isinstance(post, Post):
            if validar_post(post):
                self.posts.append(post)
                return True
        elif isinstance(post, dict):
            if validar_post(post):
                self.posts.append(Post.from_dict(post))
                return True
        return False

    def crear_post(self):
        """
        Permite crear un nuevo post desde consola solicitando datos interactivos al usuario.
        Crea la instancia de Post y la agrega a la lista de posts del blog.
        """
        id_post = validar_input_texto("Ingrese el ID: ")
        titulo = validar_input_texto("Ingrese el titulo: ")
        contenido = validar_input_texto("Ingrese el contenido: ")
        nombre_autor = validar_input_texto("Ingrese el nombre del autor: ")
        autor = Autor(nombre=nombre_autor)
        tags = validar_input_etiquetas("Ingrese un tag: ")
        estado = validar_input_estado("Ingrese el estado (borrador/publicado/archivado): ")

        nuevo_post = Post(
            id=id_post,
            titulo=titulo,
            contenido=contenido,
            autor=autor,
            tags=tags,
            estado=estado
        )

        if validar_post(nuevo_post):
            self.posts.append(nuevo_post)
            print(f"\n¡Post '{nuevo_post.titulo}' creado exitosamente en memoria!")
            return nuevo_post
        else:
            print("\nError: No se pudo crear el post debido a datos inválidos.")
            return None

    def validar_posts(self):
        """
        Valida que todos los posts cargados en el blog cumplan con las reglas requeridas.
        Retorna True si todos son válidos o False si alguno falla o no hay posts.
        """
        if not self.posts:
            print("No hay posts para validar en el blog.")
            return False

        todos_validos = True
        for post in self.posts:
            titulo = post.titulo if isinstance(post, Post) else (post.get("titulo", "Sin título") if isinstance(post, dict) else "Desconocido")
            if validar_post(post):
                print(f"Post '{titulo}' es válido.")
            else:
                print(f"Error: El post '{titulo}' no cumple con los requisitos de validación.")
                todos_validos = False
        return todos_validos

    def guardar_en_json(self, ruta=None):
        """Guarda los posts actuales de la instancia en el archivo JSON."""
        destino = ruta or self.ruta_archivo
        return guardar_todos_los_posts(self.posts, destino)

    def cargar_desde_json(self, ruta=None):
        """Carga o recarga los posts desde el archivo JSON."""
        origen = ruta or self.ruta_archivo
        self.posts = cargar_en_memoria_post(origen)
        return self.posts

    def obtener_posts(self):
        """Retorna la lista de posts del blog."""
        return self.posts

    def to_dict_list(self):
        """Convierte la lista de posts en una lista de diccionarios."""
        resultado = []
        for p in self.posts:
            if hasattr(p, "to_dict"):
                resultado.append(p.to_dict())
            elif isinstance(p, dict):
                resultado.append(p)
        return resultado