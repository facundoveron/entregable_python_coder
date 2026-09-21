
from blog.operaciones import listar_posts, buscar_por_titulo, filtrar_por_tag
from blog.validaciones import validar_post
from blog.menu import mostrar_menu
from blog.datos import posts


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


if __name__ == "__main__":
    menu()