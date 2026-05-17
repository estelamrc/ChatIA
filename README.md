
# ENTREGA CONVOCATORIA MAYO

# ENTREGA DE PRÁCTICA

## Datos

* Nombre: Estela Mª Rodríguez Césaro
* Titulación: Ingeniería Telemática
* Cuenta en laboratorios: estelam
* Cuenta URJC: em.rodriguez.2022@alumnos.urjc.es
* Video básico (url): https://youtu.be/ZiyHJy83zO8
* Video parte opcional (url): https://youtu.be/up_FccxIvQM 
* Despliegue (url): https://estelaok.pythonanywhere.com/
* Contraseñas: profe/0000 (usuario/contraseña)
* Cuenta Admin Site: admin/admin

## Recursos implementados y métodos disponibles para cada recurso

- `/` : Página principal / index (bienvenida) — **GET**
- `/login/` : Login de usuario — **GET, POST**
- `/registro/` : Registro de usuario — **GET, POST**
- `/logout/` : Cierre de sesión — **GET**
- `/ayuda/` : Página de ayuda — **GET**
- `/configuracion/` : Configuración del usuario (alias, tamaño fuente, temperatura) — **GET, POST**
- `/sidebar/` : Fragmento parcial de la sidebar (actualización HTMX) — **GET**
- `/chat/nuevo/` : Crear nueva conversación — **GET**
- `/compartir/<int:conversacion_id>/` : Generar enlace público para conversación — **GET**
- `/share/<str:hash_publico>/` : Ver conversación pública — **GET**
- `/chat/<int:conversacion_id>/json/` : Exportar conversación a JSON — **GET**
- `/chat/<int:conversacion_id>/favorito/` : Marcar/desmarcar conversación como favorita — **GET**
- `/chat/<int:conversacion_id>/eliminar/` : Eliminar conversación — **GET**
- `/chat/<int:conversacion_id>/editar/` : Editar nombre de conversación — **GET, POST**
- `/chat/<int:conversacion_id>/` : Ver conversación y enviar mensajes (HTMX) — **GET, POST**


## Resumen parte obligatoria
## Parte obligatoria – Resumen

- **Chat con IA**
  - Usuario autenticado puede enviar prompts y recibir respuestas.
  - Historial persistente de mensajes.

- **Gestión de conversaciones**
  - Crear, listar, recuperar, editar y eliminar conversaciones.
  - Favoritos visibles al inicio de la lista lateral.
  - Exportación JSON: botón “Ver JSON”.

- **Perfil y configuración de usuario**
  - Alias, modelo de IA, temperatura, tamaño de fuente.

- **Página de ayuda / documentación**
  - Explica uso de la app y todas las funcionalidades.

- **HTMX**
  - Actualización de mensajes y lista de conversaciones en tiempo real.
  - Indicador “ChatIA escribiendo…”.

- **Cabecera**
  - Logo → vuelve al index (`/`).
  - Alias de usuario y “(admin)” si corresponde.
  - Botones: Ayuda, Configuración, Logout.

- **Footer**
  - Estadísticas globales: nº de conversaciones, nº de mensajes, usuario activo.

- **Interfaz y estilo**
  - HTML + CSS dividido en dos archivos: uno para index, otro para el resto.
  - Bootstrap 5 en local para consistencia visual.

- **Autenticación**
  - Uso de cookies Django (`@login_required`).
  - Login incorrecto muestra mensaje de error en login (401).

- **Tests obligatorios**
  - 11 tests extremo a extremo que cubren login, chat, conversaciones, favoritos, configuración y JSON.
  
## Lista partes opcionales

- **Streaming de respuestas**
  - Indicador “ChatIA escribiendo…” en tiempo real mientras la IA genera la respuesta.

- **Favoritos en sidebar**
  - Las conversaciones favoritas se muestran primero en la barra lateral.
  - Se pueden marcar y desmarcar directamente desde la lista.

- **Copiar enlace público**
  - Botón en el título de cada conversación.
  - Copia automáticamente el enlace al portapapeles.
  - Mensaje emergente “Enlace copiado” visible durante unos segundos.

- **Preferencias visuales**
  - Cambiar tamaño de fuente en toda la aplicación (pequeña, normal, grande) desde la configuración de usuario.

- **Tests unitarios**
  - Verifican creación, eliminación, favoritos y compartición de conversaciones públicamente.

- **Responsive parcial**
  - Sidebar colapsable y chat ajustable para pantallas pequeñas (móviles y tablets).

- **Favicon personalizado**
  - Icono visible en la pestaña del navegador, coherente con los colores de la app.

- **Exportación de conversaciones**
  - Descarga de conversaciones en formato JSON mediante botón en la cabecera del chat.

- **Alias de usuario**
  - Visible en la cabecera de la app; si es admin se indica “(admin)”.

- **Enlace público en título de conversación**
  - Icono en la cabecera de cada conversación que permite generar y abrir un enlace público sin sobrecargar la barra lateral.