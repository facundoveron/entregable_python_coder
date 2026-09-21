from blog.menu import mostrar_menu
from blog.modelos import Blog


def menu(blog):
    """Mantiene el menú interactivo activo y despacha a los métodos correspondientes de Blog."""
    while True:
        opcion = mostrar_menu()

        if opcion is None:
            continue

        if opcion == 1:
            print("\nPosts disponibles:")
            blog.listar_posts()

        elif opcion == 2:
            termino = input("Buscar por titulo: ")
            resultados = blog.buscar_por_titulo(termino)
            if resultados:
                print(f"\nResultados encontrados ({len(resultados)}):")
                for post in resultados:
                    nombre_autor = post.autor.nombre if hasattr(post.autor, "nombre") else str(post.autor)
                    print(f"- {post.titulo} (Autor: {nombre_autor})")
            else:
                print(f"No se encontraron posts que contengan '{termino}'.")

        elif opcion == 3:
            tag = input("Ingresa un tag: ")
            resultados = blog.filtrar_por_tag(tag)
            if resultados:
                print(f"\nPosts con el tag '{tag}' ({len(resultados)}):")
                for post in resultados:
                    print(f"- {post.titulo} [Tags: {', '.join(post.tags)}]")
            else:
                print(f"No se encontraron posts con el tag '{tag}'.")

        elif opcion == 4:
            print("\n--- CREAR NUEVO POST ---")
            blog.crear_post()

        elif opcion == 5:
            print("\n--- VALIDACIÓN DE POSTS ---")
            blog.validar_posts()

        elif opcion == 6:
            print("\n--- GUARDAR POSTS EN JSON ---")
            blog.guardar_en_json()

        elif opcion == 7:
            print("\nGracias por usar el sistema del blog. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intenta de nuevo.")


if __name__ == "__main__":
    blog = Blog()
    menu(blog)