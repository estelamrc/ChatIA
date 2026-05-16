from django import forms
from .models import PerfilUsuario
from django.contrib.auth.models import User



class MensajeForm(forms.Form):
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 1,
            "placeholder": "Escribe tu mensaje..."
        })
    )

class ConversacionForm(forms.Form):
    titulo = forms.CharField(
        label="Nombre de la conversación",
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nuevo nombre"
        })
    )

class ConfiguracionUsuarioForm(forms.ModelForm):

# INTENCIÓN DE AÑADIR MÁS Y QUE FUNCIONE CLARO
    MODELOS = [
        ("google/gemma-2-2b-it", "Gemma 2B"),
    ]
    modelo = forms.ChoiceField(
        choices=MODELOS,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    TAMANOS = [
        ("pequena", "Pequeña"),
        ("normal", "Normal"),
        ("grande", "Grande"),
    ]
    tamano_fuente = forms.ChoiceField(
        label="Tamaño de letra",
        choices=TAMANOS,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    class Meta:
        model = PerfilUsuario
        fields = ["alias", "modelo", "temperatura", "tamano_fuente"]

        widgets = {
            "alias": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Tu alias"
            }),

            "temperatura": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.1",
                "min": "0.1",
                "max": "1"
            }),
        }

class RegistroUsuarioForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password2 = forms.CharField(
        label="Repite la contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ese nombre de usuario ya existe.")

        return cleaned_data


class LoginUsuarioForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )