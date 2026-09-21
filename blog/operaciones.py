# --- Funciones de lógica

def listar_posts(lista):
    """
    Muestra un resumen de cada post de la lista de forma segura (usando .get()).
    Retorna la lista de cadenas formateadas para cada post mostrado.
    """
    if not lista:
        print("No hay posts disponibles para mostrar.")
        return []

    resumen = []
    for post in lista:
        if not isinstance(post, dict):
            continue
        titulo = post.get("titulo", "Sin título")
        autor = post.get("autor")
        nombre_autor = autor.get("nombre", "Desconocido") if isinstance(autor, dict) else "Desconocido"
        estado = post.get("estado", "Desconocido")
        linea = f"- {titulo} | Autor: {nombre_autor} | Estado: {estado}"
        print(linea)
        resumen.append(linea)
    return resumen

# Alias para compatibilidad con singular y plural
listar_post = listar_posts


def buscar_por_titulo(lista, termino):
    """
    Busca posts cuyo título contenga el término especificado (insensible a mayúsculas).
    Retorna una lista con los posts que coincidan.
    """
    if not isinstance(termino, str) or not termino:
        return []

    termino_busqueda = termino.lower()
    resultados = []
    for post in lista:
        if isinstance(post, dict):
            titulo = post.get("titulo")
            if isinstance(titulo, str) and termino_busqueda in titulo.lower():
                resultados.append(post)
    return resultados


def filtrar_por_tag(lista, tag):
    """
    Filtra posts que contengan el tag especificado (insensible a mayúsculas).
    Retorna una lista con los posts coincidentes.
    """
    if not isinstance(tag, str) or not tag:
        return []

    tag_busqueda = tag.lower()
    resultados = []
    for post in lista:
        if isinstance(post, dict):
            tags = post.get("tags")
            if isinstance(tags, list):
                if any(isinstance(t, str) and t.lower() == tag_busqueda for t in tags):
                    resultados.append(post)
    return resultados