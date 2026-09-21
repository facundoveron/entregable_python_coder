# --- Funciones de Menú e Interacción ---

def mostrar_menu():
    """
    Muestra las opciones del menú y retorna la opción ingresada por el usuario.
    Usa try-except para capturar y validar la entrada numérica.
    """
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar posts")
    print("5. Salir")

    try:
        opcion = int(input("Ingresa tu opcion: "))
        return opcion
    except ValueError:
        print("Opción inválida, intenta de nuevo (debes ingresar un número).")
        return None
