from django.db import models
from django.contrib.auth.models import User
import secrets

# Create your models here.

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, default="google/gemma-2-2b-it")
    temperatura = models.FloatField(default=0.7)
    tamano_fuente = models.CharField(max_length=20, default="normal")
    # para controlar usuarios:
    #   - alias: un nombre alternativo para mostrar en lugar del nombre de usuario real.
    #   - modelo: el modelo de lenguaje que el usuario prefiere usar para las conversaciones.
    #   - temperatura: valor que controla la creatividad de las respuestas generadas por el modelo de lenguaje.
    #   + temperatura = + creatividad
    def __str__(self):
        return self.user.username


class Conversacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    favorita = models.BooleanField(default=False)

    nombre_personalizado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    # Añadimos campo para el enlace público
    hash_publico = models.CharField(max_length=32, blank=True, null=True)

    def generar_hash_publico(self):
        """Genera un hash aleatorio para compartir la conversación públicamente"""
        self.hash_publico = secrets.token_hex(16)
        self.save()

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)