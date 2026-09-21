import os
import sys
import json
import tempfile
import unittest
from unittest.mock import patch

# Asegura que el directorio raíz del proyecto esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blog.datos import (
    perfil_autor,
    estados_post,
    etiquetas_blog,
    posts,
    verificar_si_existe_el_archivo,
    convertir_dict_en_autor,
    convertir_dict_en_post,
    convertir_autor_en_dict,
    convertir_post_en_dict,
    cargar_en_memoria_post,
    guardar_todos_los_posts,
    guardar_post
)
from blog.modelos import Autor, Post, Blog
from blog.validaciones import (
    validar_post,
    validar_input_texto,
    validar_input_estado,
    validar_input_etiquetas,
    validar_agregar_mas_etiquetas
)

from blog.menu import mostrar_menu


class TestClaseAutor(unittest.TestCase):
    """Pruebas unitarias para la clase Autor."""

    def test_instanciacion_autor(self):
        """Verifica la correcta creación de una instancia de Autor."""
        autor = Autor("Carlos Ruiz", "Escritor tech", "Python", ["@carlos_dev"])
        self.assertEqual(autor.nombre, "Carlos Ruiz")
        self.assertEqual(autor.bio, "Escritor tech")
        self.assertEqual(autor.especialidad, "Python")
        self.assertEqual(autor.redes_sociales, ["@carlos_dev"])

    def test_autor_to_dict(self):
        """Verifica la serialización de Autor a diccionario."""
        autor = Autor("Ana López", "Dev", "Django", ["@ana"])
        data = autor.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["nombre"], "Ana López")
        self.assertEqual(data["bio"], "Dev")
        self.assertEqual(data["especialidad"], "Django")
        self.assertEqual(data["redes_sociales"], ["@ana"])

    def test_autor_from_dict(self):
        """Verifica la deserialización de diccionario a objeto Autor."""
        data = {
            "nombre": "Ana López",
            "bio": "Desarrolladora",
            "especialidad": "Python",
            "redes_sociales": ["@ana"]
        }
        autor = Autor.from_dict(data)
        self.assertIsInstance(autor, Autor)
        self.assertEqual(autor.nombre, "Ana López")
        self.assertEqual(autor.especialidad, "Python")

    def test_autor_from_dict_invalido(self):
        """Verifica que from_dict lance ValueError si no recibe un diccionario."""
        with self.assertRaises(ValueError):
            Autor.from_dict("No es dict")


class TestClasePost(unittest.TestCase):
    """Pruebas unitarias para la clase Post."""

    def setUp(self):
        self.autor = Autor("Ana López", "Dev", "Python", ["@ana"])

    def test_instanciacion_post_con_autor_objeto(self):
        """Verifica la creación de un Post recibiendo una instancia de Autor."""
        post = Post(1, "Post Test", "Contenido", self.autor, ["Python"], "publicado")
        self.assertEqual(post.id, 1)
        self.assertEqual(post.titulo, "Post Test")
        self.assertIsInstance(post.autor, Autor)
        self.assertEqual(post.autor.nombre, "Ana López")
        self.assertEqual(post.estado, "publicado")

    def test_instanciacion_post_con_autor_dict(self):
        """Verifica que si se pasa un dict en autor, se convierta a objeto Autor."""
        autor_dict = {"nombre": "Pedro Gomez", "bio": "", "especialidad": "", "redes_sociales": []}
        post = Post(2, "Post Dict", "Contenido", autor_dict, ["Web"], "borrador")
        self.assertIsInstance(post.autor, Autor)
        self.assertEqual(post.autor.nombre, "Pedro Gomez")

    def test_post_to_dict(self):
        """Verifica la serialización de Post a diccionario compatible con JSON."""
        post = Post(1, "Mi Post", "Texto del post", self.autor, ["Python", "Django"], "publicado")
        d = post.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["id"], 1)
        self.assertEqual(d["titulo"], "Mi Post")
        self.assertIsInstance(d["autor"], dict)
        self.assertEqual(d["autor"]["nombre"], "Ana López")
        self.assertEqual(d["tags"], ["Python", "Django"])
        self.assertEqual(d["estado"], "publicado")

    def test_post_from_dict(self):
        """Verifica la reconstrucción de Post a partir de un diccionario."""
        data = {
            "id": 10,
            "titulo": "Reconstruido",
            "contenido": "Cuerpo",
            "autor": {"nombre": "Ana López", "bio": "", "especialidad": "", "redes_sociales": []},
            "tags": ["Python"],
            "estado": "publicado"
        }
        post = Post.from_dict(data)
        self.assertIsInstance(post, Post)
        self.assertEqual(post.id, 10)
        self.assertEqual(post.titulo, "Reconstruido")
        self.assertIsInstance(post.autor, Autor)
        self.assertEqual(post.autor.nombre, "Ana López")


class TestClaseBlog(unittest.TestCase):
    """Pruebas unitarias para la clase Blog y sus métodos de negocio."""

    def setUp(self):
        self.autor = Autor("Ana López", "Dev", "Python", ["@ana"])
        self.post1 = Post(1, "Introducción a Python", "Contenido 1", self.autor, ["Python", "Principiantes"], "publicado")
        self.post2 = Post(2, "Avanzado con Django", "Contenido 2", self.autor, ["Python", "Django", "Web"], "publicado")
        self.post3 = Post(3, "Manejo de Listas", "Contenido 3", self.autor, ["Python", "Listas"], "borrador")
        self.blog = Blog(posts=[self.post1, self.post2, self.post3])

    def test_posts_son_instancias_de_post(self):
        """Verifica que el atributo posts del Blog contenga objetos Post."""
        self.assertEqual(len(self.blog.posts), 3)
        for p in self.blog.posts:
            self.assertIsInstance(p, Post)
            self.assertIsInstance(p.autor, Autor)

    def test_listar_posts(self):
        """Verifica que listar_posts retorne un resumen formateado de cada post."""
        resumen = self.blog.listar_posts()
        self.assertEqual(len(resumen), 3)
        self.assertIn("Introducción a Python", resumen[0])
        self.assertIn("Ana López", resumen[0])
        self.assertIn("publicado", resumen[0])

    def test_listar_posts_vacio(self):
        """Verifica el comportamiento cuando el blog no tiene posts."""
        blog_vacio = Blog(posts=[])
        self.assertEqual(blog_vacio.listar_posts(), [])

    def test_buscar_por_titulo_case_insensitive(self):
        """Verifica la búsqueda de posts por título ignorando mayúsculas y minúsculas."""
        res_django = self.blog.buscar_por_titulo("DJANGO")
        self.assertEqual(len(res_django), 1)
        self.assertEqual(res_django[0].id, 2)

        res_python = self.blog.buscar_por_titulo("python")
        self.assertEqual(len(res_python), 1)
        self.assertEqual(res_python[0].id, 1)

        res_inexistente = self.blog.buscar_por_titulo("C++")
        self.assertEqual(res_inexistente, [])

        self.assertEqual(self.blog.buscar_por_titulo(""), [])
        self.assertEqual(self.blog.buscar_por_titulo("   "), [])

    def test_filtrar_por_tag_case_insensitive(self):
        """Verifica el filtrado de posts por tag ignorando mayúsculas y minúsculas."""
        res_python = self.blog.filtrar_por_tag("python")
        self.assertEqual(len(res_python), 3)

        res_web = self.blog.filtrar_por_tag("WEB")
        self.assertEqual(len(res_web), 1)
        self.assertEqual(res_web[0].id, 2)

        res_nada = self.blog.filtrar_por_tag("Rust")
        self.assertEqual(res_nada, [])

    def test_agregar_post_valido_e_invalido(self):
        """Verifica el método agregar_post para posts válidos e inválidos."""
        nuevo_valido = Post(4, "Nuevo Post", "Contenido", self.autor, ["Python"], "publicado")
        self.assertTrue(self.blog.agregar_post(nuevo_valido))
        self.assertEqual(len(self.blog.posts), 4)

        nuevo_invalido = Post(5, "", "", self.autor, ["Python"], "estado_falso")
        self.assertFalse(self.blog.agregar_post(nuevo_invalido))

    def test_validar_posts_blog(self):
        """Verifica la validación masiva de posts en la instancia de Blog."""
        self.assertTrue(self.blog.validar_posts())

        # Si agregamos un post con estado inválido
        post_malo = Post(6, "Titulo", "Contenido", self.autor, ["Python"], "invalido")
        self.blog.posts.append(post_malo)
        self.assertFalse(self.blog.validar_posts())

    def test_to_dict_list(self):
        """Verifica que to_dict_list convierta la colección a lista de diccionarios."""
        lista_dicts = self.blog.to_dict_list()
        self.assertEqual(len(lista_dicts), 3)
        self.assertIsInstance(lista_dicts[0], dict)
        self.assertEqual(lista_dicts[0]["titulo"], "Introducción a Python")


class TestPersistenciaJSON(unittest.TestCase):
    """Pruebas para carga, guardado y tolerancia a fallos con posts.json."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ruta_temp = os.path.join(self.temp_dir.name, "test_posts.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_guardar_y_cargar_posts_json(self):
        """Verifica el ciclo completo de guardado y carga de posts en JSON."""
        autor = Autor("Ana López", "Bio", "Especialidad", ["@ana"])
        posts_guardar = [
            Post(1, "Post 1", "Contenido 1", autor, ["Python"], "publicado"),
            Post(2, "Post 2", "Contenido 2", autor, ["Django"], "borrador")
        ]

        # Guardar en archivo temporal
        exito = guardar_todos_los_posts(posts_guardar, self.ruta_temp)
        self.assertTrue(exito)
        self.assertTrue(os.path.exists(self.ruta_temp))

        # Cargar desde archivo temporal
        posts_cargados = cargar_en_memoria_post(self.ruta_temp)
        self.assertEqual(len(posts_cargados), 2)
        self.assertEqual(posts_cargados[0].titulo, "Post 1")
        self.assertEqual(posts_cargados[0].autor.nombre, "Ana López")
        self.assertEqual(posts_cargados[1].estado, "borrador")

    def test_archivo_inexistente_no_falla(self):
        """Verifica que cargar un archivo inexistente retorne lista vacía sin arrojar excepciones."""
        ruta_falsa = os.path.join(self.temp_dir.name, "no_existe.json")
        resultado = cargar_en_memoria_post(ruta_falsa)
        self.assertEqual(resultado, [])

    def test_archivo_vacio_no_falla(self):
        """Verifica que un archivo vacío de 0 bytes se cargue sin errores como lista vacía."""
        with open(self.ruta_temp, "w", encoding="utf-8") as f:
            f.write("")

        resultado = cargar_en_memoria_post(self.ruta_temp)
        self.assertEqual(resultado, [])

    def test_archivo_json_invalido_no_falla(self):
        """Verifica que un archivo con formato JSON corrupto sea manejado de forma segura sin excepciones."""
        with open(self.ruta_temp, "w", encoding="utf-8") as f:
            f.write("{ este no es un json valido }")

        resultado = cargar_en_memoria_post(self.ruta_temp)
        self.assertEqual(resultado, [])


class TestValidaciones(unittest.TestCase):
    """Pruebas unitarias para validar_post y validadores de input."""

    def setUp(self):
        self.post_valido_dict = {
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
        autor = Autor("Ana López", "Dev", "Python", ["@ana"])
        self.post_valido_obj = Post(1, "Titulo", "Contenido", autor, ["Python"], "publicado")

    def test_validar_post_diccionario_y_objeto(self):
        """Verifica que validar_post funcione tanto con dicts como con objetos Post."""
        self.assertTrue(validar_post(self.post_valido_dict))
        self.assertTrue(validar_post(self.post_valido_obj))

    def test_post_no_valido_tipos(self):
        """Verifica que objetos no válidos retornen False."""
        self.assertFalse(validar_post(None))
        self.assertFalse(validar_post("cadena"))
        self.assertFalse(validar_post(123))

    def test_claves_obligatorias_faltantes(self):
        """Verifica que falte cualquiera de las claves obligatorias retorne False."""
        claves = ["id", "titulo", "contenido", "autor", "tags", "estado"]
        for clave in claves:
            with self.subTest(clave_faltante=clave):
                post_inc = self.post_valido_dict.copy()
                del post_inc[clave]
                self.assertFalse(validar_post(post_inc))

    def test_estados_validos_e_invalidos(self):
        """Verifica que solo los estados permitidos retornen True."""
        for est in estados_post:
            with self.subTest(estado=est):
                p = self.post_valido_dict.copy()
                p["estado"] = est
                self.assertTrue(validar_post(p))

        p_malo = self.post_valido_dict.copy()
        p_malo["estado"] = "estado_inexistente"
        self.assertFalse(validar_post(p_malo))


class TestMenu(unittest.TestCase):
    """Pruebas unitarias para el menú interactivo."""

    @patch('builtins.input', return_value='1')
    def test_mostrar_menu_opcion_valida(self, mock_input):
        """Verifica que retorna la opción 1."""
        self.assertEqual(mostrar_menu(), 1)

    @patch('builtins.input', return_value='7')
    def test_mostrar_menu_opcion_salir(self, mock_input):
        """Verifica que retorna la opción 7."""
        self.assertEqual(mostrar_menu(), 7)

    @patch('builtins.input', return_value='abc')
    def test_mostrar_menu_opcion_invalida(self, mock_input):
        """Verifica que entradas no numéricas sean capturadas y retornen None."""
        self.assertIsNone(mostrar_menu())


if __name__ == '__main__':
    unittest.main()
