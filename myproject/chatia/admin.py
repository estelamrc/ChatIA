from django.contrib import admin
from .models import PerfilUsuario, Conversacion, Mensaje

# Register your models here.


admin.site.register(PerfilUsuario)
admin.site.register(Conversacion)
admin.site.register(Mensaje)