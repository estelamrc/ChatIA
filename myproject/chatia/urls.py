from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/", views.chat_principal, name="chat_principal"),
    path("login/", views.login_usuario, name="login"),
    path("registro/", views.registro_usuario, name="registro"),
    path("logout/", views.logout_usuario, name="logout"),
    path("ayuda/", views.ayuda, name="ayuda"),
    path("sidebar/", views.sidebar_partial, name="sidebar_partial"),
    path("configuracion/", views.configuracion_usuario, name="configuracion_usuario"),
    path("chat/nuevo/", views.nueva_conversacion, name="nueva_conversacion"),

    path("compartir/<int:conversacion_id>/", views.compartir_conversacion, name="compartir_conversacion"),
    path("share/<str:hash_publico>/", views.ver_conversacion_publica, name="ver_conversacion_publica"),

    path("chat/<int:conversacion_id>/json/", views.conversacion_json, name="conversacion_json"),
    path("chat/<int:conversacion_id>/favorito/", views.marcar_favorita, name="marcar_favorita"),    path("chat/<int:conversacion_id>/eliminar/", views.eliminar_conversacion, name="eliminar_conversacion"),
    path("chat/<int:conversacion_id>/editar/", views.editar_conversacion, name="editar_conversacion"),
    path("chat/<int:conversacion_id>/", views.ver_conversacion, name="ver_conversacion"),

]