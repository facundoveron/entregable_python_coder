# Diccionario con el perfil del autor
perfil_autor = {
    "nombre": "Ana López",
    "bio": "Desarrolladora web y creadora de contenido sobre programación.",
    "especialidad": "Python y Django",
    "redes_sociales": ["@ana_dev", "@ana_python"]
}

# Tupla con los estados posibles de una publicación
estados_post = ("borrador", "publicado", "archivado")

# Set con los tags o etiquetas disponibles en el blog
etiquetas_blog = {"Python", "Django", "Web", "Backend", "Python"}

# Lista de diccionarios, donde cada uno representa un post del blog
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
    }
]

# Bucle principal que mantiene el menú activo
while True:
    # Mostrar opciones del menú
    print("---MENU DEL BLOG---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Salir")

    # Capturar la opción elegida por el usuario
    opcion = input("Ingresa tu opcion:")

    # Opción 1: Muestra los títulos de todos los posts y el autor
    if opcion == "1":
        print("Posts disponibles:")
        for post in posts:
            print(f"- {post['titulo']} | Autor: {post['autor']['nombre']}")

    # Opción 2: Busca un post por coincidencia en su título (sin distinguir mayúsculas/minúsculas)
    elif opcion == "2":
        titulo_buscar = input("Buscar por titulo: ").lower()
        for post in posts:
            if titulo_buscar in post['titulo'].lower():
                print(f"- {post['titulo']}")

    # Opción 3: Filtra los posts que contengan un tag específico
    elif opcion == "3":
        tag_buscar = input("Ingresa un tag: ")
        print(f"Posts con el tag {tag_buscar}:")
        for post in posts:
            if tag_buscar.lower() in [tag.lower() for tag in post['tags']]:
                print(f"- {post['titulo']}")

    # Opción 4: Se despide y rompe el bucle para finalizar el programa
    elif opcion == "4":
        print("Gracias por usar el sistema del blog. ¡Hasta luego!")
        break

    # Manejo de opciones que no están en el menú
    else:
        print("Opción inválida, intenta de nuevo")