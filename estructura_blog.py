perfil_autor = {
    "nombre": "Facundo Veron",
    "bio": "Desarrollador web y creador de contenido sobre programación.",
    "especialidad": "Python y Django",
    "redes_sociales": ["@FacundoVeron", "@facu", "@facupedia"]
}

estados_post = (
    "borrador",
    "publicado",
    "archivado"
)

etiquetas_blog = {
    "Python",
    "Django",
    "Desarrollo Web",
    "Data Science",
    "Data Science", 
}

posts = [
    {
        "id": 1,
        "titulo": "Primeros pasos con Python",
        "autor": perfil_autor,
        "tags": ["Python", "Principiantes"],
        "estado": estados_post[1]
    },
    {
        "id": 2,
        "titulo": "Qué es Django",
        "autor": perfil_autor,
        "tags": ["Python", "Django", "Web"],
        "estado": estados_post[0]
    },
    {
        "id": 3,
        "titulo": "Organizando datos con diccionarios",
        "autor": perfil_autor,
        "tags": ["Python", "Diccionarios"],
        "estado": estados_post[1]
    },
    {
        "id": 4,
        "titulo": "Data Science",
        "autor": perfil_autor,
        "tags": ["Python", "Data Science"],
        "estado": estados_post[0]
    }
]


print(f"El nombre del autor del segundo post es: {posts[1]['autor']['nombre']}")
print("\nLista completa de posts:")
print(posts)

