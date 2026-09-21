import os
import sys
import unittest
from unittest.mock import patch

# Asegura que el directorio raíz del proyecto esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sistema_blog import (
    perfil_autor,
    estados_post,
    etiquetas_blog,
    posts,
    validar_post,
    listar_posts,
    listar_post,
    buscar_por_titulo,
    filtrar_por_tag,
    mostrar_menu
)


class TestValidarPost(unittest.TestCase):
    """Pruebas unitarias para la función validar_post."""

    def setUp(self):
        self.post_valido = {
            "id": 1,
            "titulo": "Primeros pasos con Python",
            "contenido": "Aprende los conceptos básicos de Python.",
            "autor": {
                "nombre": "Ana López",
                "bio": "Desarrolladora web",
                "especialidad": "Python y Django",
                "redes_sociales": ["@ana_dev"]
            },
            "tags": ["Python", "Principiantes"],
            "estado": "publicado"
        }

    def test_post_valido(self):
        """Verifica que un post completo y con datos correctos retorne True."""
        self.assertTrue(validar_post(self.post_valido))

    def test_post_no_es_diccionario(self):
        """Verifica que si el post no es un diccionario retorne False."""
        self.assertFalse(validar_post("cadena de texto"))
        self.assertFalse(validar_post([1, 2, 3]))
        self.assertFalse(validar_post(None))
        self.assertFalse(validar_post(123))

    def test_claves_obligatorias_faltantes(self):
        """Verifica que falte cualquiera de las claves obligatorias retorne False."""
        claves = ["id", "titulo", "contenido", "autor", "tags", "estado"]
        for clave in claves:
            with self.subTest(clave_faltante=clave):
                post_incompleto = self.post_valido.copy()
                del post_incompleto[clave]
                self.assertFalse(validar_post(post_incompleto))

    def test_titulo_vacio_o_invalido(self):
        """Verifica que si titulo está vacío, solo con espacios o no es string retorne False."""
        casos = ["", "   ", None, 12345]
        for caso in casos:
            with self.subTest(titulo=caso):
                post = self.post_valido.copy()
                post["titulo"] = caso
                self.assertFalse(validar_post(post))

    def test_contenido_vacio_o_invalido(self):
        """Verifica que si contenido está vacío, solo con espacios o no es string retorne False."""
        casos = ["", "   ", None, 12345]
        for caso in casos:
            with self.subTest(contenido=caso):
                post = self.post_valido.copy()
                post["contenido"] = caso
                self.assertFalse(validar_post(post))

    def test_autor_no_es_diccionario(self):
        """Verifica que si autor es un string, int o lista retorne False."""
        casos = ["Ana López", 123, ["Ana López"], None]
        for caso in casos:
            with self.subTest(autor=caso):
                post = self.post_valido.copy()
                post["autor"] = caso
                self.assertFalse(validar_post(post))

    def test_autor_sin_nombre_o_nombre_vacio(self):
        """Verifica que si autor no tiene la clave 'nombre' o está vacía retorne False."""
        post_sin_nombre = self.post_valido.copy()
        post_sin_nombre["autor"] = {"bio": "Sin nombre"}
        self.assertFalse(validar_post(post_sin_nombre))

        post_nombre_vacio = self.post_valido.copy()
        post_nombre_vacio["autor"] = {"nombre": "   "}
        self.assertFalse(validar_post(post_nombre_vacio))

    def test_tags_no_es_lista(self):
        """Verifica que si tags no es una lista retorne False."""
        casos = ["Python", ("Python", "Django"), {"Python"}, None, 123]
        for caso in casos:
            with self.subTest(tags=caso):
                post = self.post_valido.copy()
                post["tags"] = caso
                self.assertFalse(validar_post(post))

    def test_estados_validos_e_invalidos(self):
        """Verifica que todos los estados en estados_post sean válidos y otros retornen False."""
        for estado in estados_post:
            with self.subTest(estado_valido=estado):
                post = self.post_valido.copy()
                post["estado"] = estado
                self.assertTrue(validar_post(post))

        estados_invalidos = ["eliminado", "revision", "PUBLICADO", "", None, 123]
        for estado in estados_invalidos:
            with self.subTest(estado_invalido=estado):
                post = self.post_valido.copy()
                post["estado"] = estado
                self.assertFalse(validar_post(post))


class TestBuscarPorTitulo(unittest.TestCase):
    """Pruebas unitarias para buscar_por_titulo."""

    def setUp(self):
        self.lista_posts = [
            {"id": 1, "titulo": "Primeros pasos con Python", "tags": ["Python"]},
            {"id": 2, "titulo": "Qué es Django", "tags": ["Django"]},
            {"id": 3, "titulo": "Organizando datos con listas", "tags": ["Listas"]}
        ]

    def test_busqueda_exacta_y_parcial(self):
        """Verifica coincidencias exactas y parciales en el título."""
        res_django = buscar_por_titulo(self.lista_posts, "Django")
        self.assertEqual(len(res_django), 1)
        self.assertEqual(res_django[0]["id"], 2)

        res_python = buscar_por_titulo(self.lista_posts, "python")
        self.assertEqual(len(res_python), 1)
        self.assertEqual(res_python[0]["id"], 1)

    def test_busqueda_insensible_a_mayusculas(self):
        """Verifica que la búsqueda use .lower() y no distinga mayúsculas/minúsculas."""
        res1 = buscar_por_titulo(self.lista_posts, "DJANGO")
        res2 = buscar_por_titulo(self.lista_posts, "django")
        res3 = buscar_por_titulo(self.lista_posts, "DjAnGo")
        self.assertEqual(res1, res2)
        self.assertEqual(res2, res3)
        self.assertEqual(len(res1), 1)

    def test_busqueda_sin_coincidencias(self):
        """Verifica que si no hay coincidencias retorne una lista vacía."""
        res = buscar_por_titulo(self.lista_posts, "JavaScript")
        self.assertEqual(res, [])

    def test_busqueda_parametros_invalidos(self):
        """Verifica el comportamiento seguro con parámetros no válidos."""
        self.assertEqual(buscar_por_titulo(self.lista_posts, ""), [])
        self.assertEqual(buscar_por_titulo(self.lista_posts, None), [])
        self.assertEqual(buscar_por_titulo([], "Python"), [])


class TestFiltrarPorTag(unittest.TestCase):
    """Pruebas unitarias para filtrar_por_tag."""

    def setUp(self):
        self.lista_posts = [
            {"id": 1, "titulo": "Python 1", "tags": ["Python", "Principiantes"]},
            {"id": 2, "titulo": "Django 1", "tags": ["Python", "Django", "Web"]},
            {"id": 3, "titulo": "Listas 1", "tags": ["Listas"]}
        ]

    def test_filtrado_exitoso(self):
        """Verifica que retorne todos los posts que tengan el tag solicitado."""
        res_python = filtrar_por_tag(self.lista_posts, "Python")
        self.assertEqual(len(res_python), 2)
        ids = [p["id"] for p in res_python]
        self.assertIn(1, ids)
        self.assertIn(2, ids)

    def test_filtrado_insensible_a_mayusculas(self):
        """Verifica que el filtrado por tag use .lower() y sea case-insensitive."""
        res_web = filtrar_por_tag(self.lista_posts, "wEb")
        self.assertEqual(len(res_web), 1)
        self.assertEqual(res_web[0]["id"], 2)

    def test_tag_sin_coincidencias(self):
        """Verifica que retorne lista vacía si el tag no existe en los posts."""
        res = filtrar_por_tag(self.lista_posts, "React")
        self.assertEqual(res, [])

    def test_parametros_invalidos_o_posts_incompletos(self):
        """Verifica que no falle si la lista o el tag no son válidos."""
        self.assertEqual(filtrar_por_tag(self.lista_posts, ""), [])
        self.assertEqual(filtrar_por_tag(self.lista_posts, None), [])
        self.assertEqual(filtrar_por_tag([], "Python"), [])
        # Post con tags no lista o ausente
        posts_danados = [{"id": 4, "titulo": "Sin tags"}, {"id": 5, "tags": "no-es-lista"}]
        self.assertEqual(filtrar_por_tag(posts_danados, "Python"), [])


class TestListarPosts(unittest.TestCase):
    """Pruebas unitarias para listar_posts y su alias listar_post."""

    def test_listar_posts_valido(self):
        """Verifica que liste correctamente posts y retorne las líneas formateadas."""
        lista_prueba = [
            {
                "titulo": "Post de prueba",
                "autor": {"nombre": "Ana López"}
            }
        ]
        resumen = listar_posts(lista_prueba)
        self.assertEqual(len(resumen), 1)
        self.assertIn("Post de prueba", resumen[0])
        self.assertIn("Ana López", resumen[0])

    def test_listar_posts_incompletos_seguro(self):
        """Verifica que no lance excepciones KeyError ante posts incompletos."""
        lista_incompleta = [
            {"id": 4},
            {"titulo": "Solo titulo"},
            {"titulo": "Con autor string", "autor": "Nombre String"}
        ]
        resumen = listar_posts(lista_incompleta)
        self.assertEqual(len(resumen), 3)

    def test_listar_posts_vacio(self):
        """Verifica el manejo de una lista vacía."""
        self.assertEqual(listar_posts([]), [])

    def test_alias_listar_post(self):
        """Verifica que el alias listar_post apunte a la misma función."""
        self.assertIs(listar_post, listar_posts)


class TestMostrarMenu(unittest.TestCase):
    """Pruebas unitarias para mostrar_menu."""

    @patch('builtins.input', return_value='1')
    def test_mostrar_menu_opcion_valida(self, mock_input):
        """Verifica que retorna el entero de la opción ingresada."""
        opcion = mostrar_menu()
        self.assertEqual(opcion, 1)

    @patch('builtins.input', return_value='abc')
    def test_mostrar_menu_opcion_invalida_retorna_none(self, mock_input):
        """Verifica que retorna None y maneja el error ValueError con try-except."""
        opcion = mostrar_menu()
        self.assertIsNone(opcion)


class TestEstructurasBlog(unittest.TestCase):
    """Pruebas para verificar que las estructuras principales requeridas existen y tienen los tipos correctos."""

    def test_perfil_autor_estructura(self):
        """Verifica el tipo y las claves del diccionario perfil_autor."""
        self.assertIsInstance(perfil_autor, dict)
        self.assertIn("nombre", perfil_autor)
        self.assertIn("bio", perfil_autor)
        self.assertIn("especialidad", perfil_autor)
        self.assertIn("redes_sociales", perfil_autor)

    def test_estados_post_estructura(self):
        """Verifica que estados_post sea una tupla con los 3 estados requeridos."""
        self.assertIsInstance(estados_post, tuple)
        self.assertIn("borrador", estados_post)
        self.assertIn("publicado", estados_post)
        self.assertIn("archivado", estados_post)

    def test_etiquetas_blog_estructura(self):
        """Verifica que etiquetas_blog sea un set."""
        self.assertIsInstance(etiquetas_blog, set)

    def test_posts_estructura(self):
        """Verifica que posts sea una lista con al menos 3 elementos."""
        self.assertIsInstance(posts, list)
        self.assertGreaterEqual(len(posts), 3)


if __name__ == '__main__':
    unittest.main()
