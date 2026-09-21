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
