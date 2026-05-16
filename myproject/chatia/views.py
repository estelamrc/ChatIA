from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Conversacion, Mensaje, PerfilUsuario
from .forms import MensajeForm, ConversacionForm, ConfiguracionUsuarioForm
from .forms import RegistroUsuarioForm, LoginUsuarioForm
from .llm import pedir_respuesta_nvidia
from django.http import JsonResponse


import markdown

# Create your views here.
def generar_titulo_automatico(texto):
    palabras_vacias = [
        "explicame", "explícame", "que","qué", "cual", "cuál", "dime",
        "cuentame", "cuéntame", "dame",
        "hazme", "quiero", "necesito", "puedes", "podrias", "podrías",
        "por", "favor", "sobre", "acerca", "del", "de", "la", "el",
        "los", "las", "un", "una", "unos", "unas", "que", "qué",
        "es", "son", "como", "cómo", "en", "a", "y", "o", "para"
    ]

    texto = texto.lower().strip()
    texto = texto.replace("¿", "").replace("?", "")
    texto = texto.replace("¡", "").replace("!", "")
    texto = texto.replace(",", "").replace(".", "")

    palabras = texto.split()

    palabras_clave = []

    for palabra in palabras:
        if palabra not in palabras_vacias:
            palabras_clave.append(palabra)

    if len(palabras_clave) == 0:
        return "Nueva conversación"

    titulo = " ".join(palabras_clave[:4])
    titulo = titulo.capitalize()

    if len(titulo) > 45:
        titulo = titulo[:45] + "..."

    return titulo


def index(request):
    # Si el usuario ya está logueado, redirigirlo al chat principal
    #esto lo he cambiado para que no redirija (pa pinchar el ChatIA)
    return render(request, "index.html")

@login_required
def chat_principal(request):
    conversacion = Conversacion.objects.filter(
        user=request.user
    ).order_by("-favorita", "-fecha_creacion").first()

    if conversacion is None:
        conversacion = Conversacion.objects.create(
            user=request.user,
            titulo="Conversación 1"
        )

    return redirect("ver_conversacion", conversacion_id=conversacion.id)


@login_required
def nueva_conversacion(request):
    total = Conversacion.objects.filter(user=request.user).count()

    conversacion = Conversacion.objects.create(
        user=request.user,
        titulo=f"Conversación {total + 1}"
    )

    return redirect("ver_conversacion", conversacion_id=conversacion.id)


@login_required
def ver_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(
        Conversacion,
        id=conversacion_id,
        user=request.user
    )

    if request.method == "POST":
        form = MensajeForm(request.POST)

        if form.is_valid():
            texto_usuario = form.cleaned_data["mensaje"]

            if not conversacion.nombre_personalizado and conversacion.titulo.startswith("Conversación"):
                conversacion.titulo = generar_titulo_automatico(texto_usuario)
                conversacion.save()

            Mensaje.objects.create(
                conversacion=conversacion,
                rol="usuario",
                contenido=texto_usuario
            )

            perfil, creado = PerfilUsuario.objects.get_or_create(
                user=request.user
            )

            mensajes_historial = Mensaje.objects.filter(
                conversacion=conversacion
            ).order_by("fecha")

            mensajes_para_ia = []

            for mensaje in mensajes_historial:

                if mensaje.rol == "usuario":
                    rol_api = "user"
                else:
                    rol_api = "assistant"

                mensajes_para_ia.append({
                    "role": rol_api,
                    "content": mensaje.contenido
                })

            respuesta_ia = pedir_respuesta_nvidia(
                mensajes_para_ia,
                temperatura=perfil.temperatura
            )

            respuesta_ia_html = markdown.markdown(respuesta_ia)

            Mensaje.objects.create(
                conversacion=conversacion,
                rol="ChatIA",
                contenido=respuesta_ia_html
            )

            mensajes = Mensaje.objects.filter(
                conversacion=conversacion
            ).order_by("fecha")

            if request.headers.get("HX-Request"):
                return render(request, "partials/mensajes.html", {
                    "mensajes": mensajes,
                })

            return redirect("ver_conversacion", conversacion_id=conversacion.id)
    else:
        form = MensajeForm()

    mensajes = Mensaje.objects.filter(
        conversacion=conversacion
    ).order_by("fecha")

    conversaciones = Conversacion.objects.filter(
        user=request.user
    ).order_by("-favorita", "-fecha_creacion")

    total_conversaciones = conversaciones.count()

    total_mensajes = Mensaje.objects.filter(
        conversacion__user=request.user
    ).count()

    perfil, creado = PerfilUsuario.objects.get_or_create(user=request.user)

    return render(request, "chat.html", {
        "form": form,
        "mensajes": mensajes,
        "conversacion": conversacion,
        "conversaciones": conversaciones,
        "total_conversaciones": total_conversaciones,
        "total_mensajes": total_mensajes,
        "perfil": perfil,
    })


@login_required
def eliminar_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(
        Conversacion,
        id=conversacion_id,
        user=request.user
    )

    conversacion.delete()

    return redirect("chat_principal")


@login_required
def editar_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(
        Conversacion,
        id=conversacion_id,
        user=request.user
    )

    if request.method == "POST":
        form = ConversacionForm(request.POST)

        if form.is_valid():
            conversacion.titulo = form.cleaned_data["titulo"]
            conversacion.nombre_personalizado = True
            conversacion.save()
            return redirect("ver_conversacion", conversacion_id=conversacion.id)

    else:
        form = ConversacionForm(initial={
            "titulo": conversacion.titulo
        })

    conversaciones = Conversacion.objects.filter(
        user=request.user
    ).order_by("-favorita", "-fecha_creacion")

    total_mensajes = Mensaje.objects.filter(
        conversacion__user=request.user
    ).count()

    perfil, creado = PerfilUsuario.objects.get_or_create(user=request.user)
    return render(request, "editar_conversacion.html", {
        "form": form,
        "conversacion": conversacion,
        "conversaciones": conversaciones,
        "total_conversaciones": conversaciones.count(),
        "total_mensajes": total_mensajes,
        "perfil": perfil,
    })

@login_required
def marcar_favorita(request, conversacion_id):
    conversacion = get_object_or_404(
        Conversacion,
        id=conversacion_id,
        user=request.user
    )

    conversacion.favorita = not conversacion.favorita
    conversacion.save()

    return redirect("ver_conversacion", conversacion_id=conversacion.id)

@login_required
def configuracion_usuario(request):
    perfil, creado = PerfilUsuario.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ConfiguracionUsuarioForm(request.POST, instance=perfil)

        if form.is_valid():
            form.save()
            return redirect("configuracion_usuario")

    else:
        form = ConfiguracionUsuarioForm(instance=perfil)

    conversaciones = Conversacion.objects.filter(
        user=request.user
    ).order_by("-favorita", "-fecha_creacion")

    total_mensajes = Mensaje.objects.filter(
        conversacion__user=request.user
    ).count()

    perfil, creado = PerfilUsuario.objects.get_or_create(user=request.user)
    return render(request, "configuracion_usuario.html", {
        "form": form,
        "perfil": perfil,
        "conversaciones": conversaciones,
        "total_conversaciones": conversaciones.count(),
        "total_mensajes": total_mensajes,
        "created": creado,
    })

def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = User.objects.create_user(
                username=username,
                password=password
            )

            PerfilUsuario.objects.create(user=user)

            login(request, user)

            return redirect("chat_principal")

    else:
        form = RegistroUsuarioForm()

    return render(request, "registro.html", {
        "form": form
    })


def login_usuario(request):
    if request.method == "POST":
        form = LoginUsuarioForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("chat_principal")
            else:
                form.add_error(None, "Usuario o contraseña incorrectos.")

    else:
        form = LoginUsuarioForm()

    return render(request, "login.html", {
        "form": form
    })


def logout_usuario(request):
    logout(request)
    return redirect("login")

# PARA EL JSON
@login_required
def conversacion_json(request, conversacion_id):
    conversacion = get_object_or_404(
        Conversacion,
        id=conversacion_id,
        user=request.user
    )

    mensajes = Mensaje.objects.filter(
        conversacion=conversacion
    ).order_by("fecha")

    datos = {
        "id": conversacion.id,
        "titulo": conversacion.titulo,
        "favorita": conversacion.favorita,
        "usuario": request.user.username,
        "mensajes": []
    }

    for mensaje in mensajes:
        datos["mensajes"].append({
            "rol": mensaje.rol,
            "contenido": mensaje.contenido,
            "fecha": mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse(datos)

# PARA LA AYUDA
@login_required
def ayuda(request):
    conversaciones = Conversacion.objects.filter(
        user=request.user
    ).order_by("-favorita", "-fecha_creacion")

    total_mensajes = Mensaje.objects.filter(
        conversacion__user=request.user
    ).count()

    perfil, creado = PerfilUsuario.objects.get_or_create(
        user=request.user
    )

    return render(request, "ayuda.html", {
        "conversaciones": conversaciones,
        "total_conversaciones": conversaciones.count(),
        "total_mensajes": total_mensajes,
        "perfil": perfil,
    })

#PARA EL HTMX DE LOS NOMBRES DE CONVER
@login_required
def sidebar_partial(request):
    conversaciones = Conversacion.objects.filter(
        user=request.user
    ).order_by("-favorita", "-fecha_creacion")

    return render(request, "partials/sidebar.html", {
        "conversaciones": conversaciones,
        "total_conversaciones": conversaciones.count(),
    })

#para el enlace y compartir conversacion

def ver_conversacion_publica(request, hash_publico):
    conversacion = get_object_or_404(Conversacion, hash_publico=hash_publico)
    mensajes = conversacion.mensaje_set.order_by("fecha")

    return render(request, "chat_publica.html", {
        "conversacion": conversacion,
        "mensajes": mensajes,
    })

@login_required
def compartir_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id, user=request.user)

    if not conversacion.hash_publico:
        conversacion.generar_hash_publico()

    # redirige de nuevo a la conversación
    return redirect("ver_conversacion", conversacion_id=conversacion.id)