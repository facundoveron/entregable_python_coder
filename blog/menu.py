# --- Funciones de Menú e Interacción ---

def mostrar_menu():
    """
    Muestra las opciones del menú y retorna la opción ingresada por el usuario.
    """
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")

    try:
        entrada = input("Ingresa tu opcion: ")
        opcion = int(entrada)
        return opcion
    except ValueError:
        print("Opción inválida, intenta de nuevo (debes ingresar un número).")
        return None
