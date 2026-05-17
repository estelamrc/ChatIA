from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Conversacion, Mensaje, PerfilUsuario


# Create your tests here.


class ChatIATests(TestCase):

    # Configuración
    def setUp(self):         # para crear datos de prueba
        #simula un navegador
        self.client = Client()

        #crea un usuario normal en la base de datos de test
        self.user = User.objects.create_user(
            username="usuario_prueba",
            password="1234"
        )

        #su configuración
        self.perfil = PerfilUsuario.objects.create(
            user=self.user,
            alias="Tester",
            temperatura=0.7
        )

        #crea una conversación de prueba
        self.conversacion = Conversacion.objects.create(
            user=self.user,
            titulo="Conversación de prueba"
        )

        #crear un mensaje de prueba
        self.mensaje = Mensaje.objects.create(
            conversacion=self.conversacion,
            rol="usuario",
            contenido="Hola"
        )

    # comprueba si un usuario YA EXISTENTE puede iniciar sesión
    def test_login_usuario_correcto(self):
        # hace POST a reverse("login") y espera 302 (redirección)
        response = self.client.post(reverse("login"), {
            "username": "usuario_prueba",
            "password": "1234"
        })

        self.assertEqual(response.status_code, 302)

    # test para el registro: coinciden contraseñas-> espera 302 (redirección)
    def test_registro_usuario(self):
        response = self.client.post(reverse("registro"), {
            "username": "nuevo_usuario",
            "password1": "1234",
            "password2": "1234"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="nuevo_usuario").exists())

    # test registro pero distintas contraseñas -> espera 200 (formulario con error)
    def test_registro_passwords_distintas(self):
        response = self.client.post(reverse("registro"), {
            "username": "usuario_error",
            "password1": "1234",
            "password2": "abcd"
        })

        # assert para verificar que el usuario no se creó
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="usuario_error").exists())

    # comprueba que una conver no se ve sin iniciar sesión
    # GET A /chat/id sin login-> espera 302 (redirección)
    def test_acceso_chat_sin_login_redirige(self):
        response = self.client.get(
            reverse("ver_conversacion", args=[self.conversacion.id])
        )

        self.assertEqual(response.status_code, 302)

    # inicia sesión, entra a la conversación-> espera 200 (página de chat)
    def test_ver_conversacion_con_login(self):
        self.client.login(username="usuario_prueba", password="1234")

        response = self.client.get(
            reverse("ver_conversacion", args=[self.conversacion.id])
        )

        self.assertEqual(response.status_code, 200)
        #comprueba que aparece el titulo
        self.assertContains(response, "Conversación de prueba")

    # inicia sesion y llama a reverse("nueva_conversacion")
    # espera 302 (redirección)
    def test_crear_nueva_conversacion(self):
        self.client.login(username="usuario_prueba", password="1234")

        response = self.client.get(reverse("nueva_conversacion"))
        self.assertEqual(response.status_code, 302)
        # comprueba que ahora tiene 2 conversaciones
        self.assertEqual(Conversacion.objects.filter(user=self.user).count(), 2)


    #inicia sesion y hace POST a editar conversacion
    # espera 302 (redirección)
    def test_editar_conversacion(self):
        self.client.login(username="usuario_prueba", password="1234")

        response = self.client.post(
            reverse("editar_conversacion", args=[self.conversacion.id]),
            {
                "titulo": "Nombre cambiado"
            }
        )

        self.assertEqual(response.status_code, 302)
        #comprueba que el titulo se cambió
        self.conversacion.refresh_from_db()
        self.assertEqual(self.conversacion.titulo, "Nombre cambiado")


    #inicia sesion y llama a la URL de favorita
    def test_marcar_conversacion_favorita(self):
        self.client.login(username="usuario_prueba", password="1234")

        response = self.client.get(
            reverse("marcar_favorita", args=[self.conversacion.id])
        )

        # espera 302 (redirección)
        # recarga desde base de datos y comprueba que es favorita
        self.assertEqual(response.status_code, 302)

        self.conversacion.refresh_from_db()
        self.assertTrue(self.conversacion.favorita)


    #inicia sesion y llama a la URL de eliminar
    def test_eliminar_conversacion(self):
        self.client.login(username="usuario_prueba", password="1234")

        response = self.client.get(
            reverse("eliminar_conversacion", args=[self.conversacion.id])
        )

        self.assertEqual(response.status_code, 302)
        # comprueba que la conversación no existe (FALSE)
        self.assertFalse(
            Conversacion.objects.filter(id=self.conversacion.id).exists()
        )

    # entra en el recurso /chat/id/json
    def test_json_conversacion(self):
        self.client.login(username="usuario_prueba", password="1234")

        response = self.client.get(
            reverse("conversacion_json", args=[self.conversacion.id])
        )

        # espera 200 (página de chat)
        self.assertEqual(response.status_code, 200)
        # comprueba que el contenido sea JSON
        self.assertEqual(response["Content-Type"], "application/json")

        # comprueba wl titulo y que tiene 1 mensaje
        data = response.json()
        self.assertEqual(data["titulo"], "Conversación de prueba")
        self.assertEqual(len(data["mensajes"]), 1)

    # envia cambios a configuración
    def test_configuracion_usuario(self):
        self.client.login(username="usuario_prueba", password="1234")

        response = self.client.post(reverse("configuracion_usuario"), {
            "alias": "NuevoAlias",
            "modelo": "google/gemma-2-2b-it",
            "temperatura": 0.5,
            "tamano_fuente": "grande"
        })

        # espera 302 (redirección)
        self.assertEqual(response.status_code, 302)

        # recarga perfil desde base de datos y comprueba cambios
        self.perfil.refresh_from_db()
        self.assertEqual(self.perfil.alias, "NuevoAlias")
        self.assertEqual(self.perfil.tamano_fuente, "grande")


class TestFuncionalidadesOpcionales(TestCase):

    def setUp(self):
        #usuario de prueba
        self.user = User.objects.create_user(username="testuser", password="12345")

    # este test comprueba que se genera un hash publico
    def test_generar_hash_publico(self):
        # Creamos una conversación sin hash
        conv = Conversacion.objects.create(user=self.user, titulo="Prueba Hash")
        self.assertIsNone(conv.hash_publico)

        # Generamos hash
        conv.generar_hash_publico()
        self.assertIsNotNone(conv.hash_publico)
        self.assertEqual(len(conv.hash_publico), 32)  # Debe ser un hex de 16 bytes = 32 caracteres

    # este test comprueba que se marca una conversación como favorita
    def test_favorita(self):
        # Crear conversación
        conv = Conversacion.objects.create(user=self.user, titulo="Prueba Favorita")
        conv.favorita = False
        conv.save()

        # Marcar como favorita
        conv.favorita = True
        conv.save()

        # Comprobar que se actualiza
        conv.refresh_from_db()
        self.assertTrue(conv.favorita)

    # este test comprueba que se configura el alias del usuario
    def test_configuracion_usuario_alias(self):
        # Si tienes un modelo PerfilUsuario relacionado con el user
        from .models import PerfilUsuario

        perfil = PerfilUsuario.objects.create(user=self.user, alias="MiAlias", temperatura=0.2, tamano_fuente="normal")

        self.assertEqual(perfil.alias, "MiAlias")
        self.assertEqual(perfil.temperatura, 0.2)
        self.assertEqual(perfil.tamano_fuente, "normal")