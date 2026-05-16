import os
import requests


def pedir_respuesta_nvidia(mensajes, temperatura=0.7):
    api_key = os.getenv("NVIDIA_API_KEY")
    modelo = os.getenv("NVIDIA_MODEL", "google/gemma-2-2b-it")

    if not api_key:
        return "Error: no se ha encontrado NVIDIA_API_KEY en el archivo .env"

    url = "https://integrate.api.nvidia.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": modelo,
        "messages": mensajes,
        "temperature": temperatura,
        "top_p": 1,
        "max_tokens": 300,
        "stream": False,
    }

    try:
        respuesta = requests.post(url, headers=headers, json=data, timeout=60)
        respuesta.raise_for_status()
        resultado = respuesta.json()
        return resultado["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as error:
        return f"Error al conectar con NVIDIA: {error}"

    except KeyError:
        return "Error: NVIDIA ha devuelto una respuesta inesperada"