# 🚀 Documentación de Integración: Herramientas Google (Calendar & Gmail)

Este documento detalla el proceso técnico seguido para integrar las APIs de Google Calendar y Gmail en el Asistente de Automatización vía Telegram.

---

## 1. ☁️ Configuración de Google Cloud Platform (GCP)

El primer paso fue establecer la identidad del proyecto en la nube para obtener acceso a las APIs.

1.  **Creación del Proyecto:** Se creó un nuevo proyecto en la consola de Google Cloud.
2.  **Habilitación de APIs:** Se activaron dos bibliotecas específicas:
    *   **Google Calendar API**
    *   **Gmail API**
3.  **Pantalla de Consentimiento OAuth:**
    *   Configurada como *External* (para pruebas).
    *   Se añadieron los correos de los desarrolladores como "Test Users" para permitir la autenticación sin verificación de Google.
4.  **Credenciales:**
    *   Se generó un **ID de cliente OAuth 2.0** (Aplicación de escritorio).
    *   Se descargó el archivo `credentials.json` y se colocó en la raíz del proyecto.

---

## 2. 🛠️ Desarrollo de Herramientas (`tools/`)

Se creó una capa de abstracción para interactuar con Google, separando la lógica de conexión del resto del bot.

### A. `calendar_tools.py` (El Gestor de Autenticación)
Este script actúa como el núcleo de seguridad.
*   **Función:** Maneja el flujo OAuth 2.0.
*   **Scopes Unificados:** Se definió una lista maestra de permisos para generar un único `token.json` válido para ambos servicios:
    ```python
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send'
    ]
    ```
*   **Capacidades:** Listar eventos filtrando por rangos de fecha (hoy, mañana, semana).

### B. `correo_tools.py`
*   **Función:** Utiliza las credenciales cargadas para operaciones de correo.
*   **Capacidades:**
    *   `tool_leer_correos`: Filtra mensajes con etiqueta `INBOX` y estado `unread`.
    *   `tool_enviar_correo`: Construye mensajes MIME y los envía a través de la API.

---

## 3. 🧠 Backend Unificado (`backend_calendar.py`)

Se implementó un servidor **FastAPI** (Puerto 7000) para centralizar la lógica de negocio.

*   **Inicialización (`startup_event`):** Al arrancar, el servidor conecta automáticamente con Google y mantiene las sesiones (`calendar_service`, `gmail_service`) en memoria global para no re-autenticar en cada petición.
*   **Endpoint `/consulta`:** Recibe solicitudes JSON del bot y decide qué herramienta invocar:
    *   *Consultas de Agenda:* Calcula fechas exactas (inicio/fin) y llama a `calendar_tools`.
    *   *Consultas de Correo:* Llama a `correo_tools` para leer o enviar pruebas.

---

## 4. 🤖 Interfaz del Bot (`bot_webhook.py`)

El bot de Telegram actúa como la interfaz de usuario (Frontend), corriendo en el Puerto 8001.

*   **Webhook & Ngrok:** Se configuró un túnel HTTPS con Ngrok para que Telegram pueda enviar actualizaciones al servidor local.
*   **Teclado Interactivo:** Se diseñó un menú de botones para facilitar el uso:
    *   📅 *Horario de hoy / mañana*
    *   📧 *Leer correos*
    *   📤 *Enviar Correo Prueba*
*   **Mapeo de Intenciones:** Una función traduce el texto del botón (ej: "📧 Leer correos") a un comando interno (ej: `leer_correos`) que el backend entiende.

---

## 5. 🔄 Flujo de Ejecución Final

Para que el sistema funcione, se orquestan tres servicios simultáneos:

1.  **Ngrok:** Expone el puerto 8001 a internet.
    ```bash
    ngrok http 8001
    ```
2.  **Backend (Cerebro):** Procesa lógica y conecta con Google.
    ```bash
    uvicorn backend_calendar:app --reload --port 7000
    ```
3.  **Bot (Interfaz):** Recibe mensajes de Telegram y consulta al Backend.
    ```bash
    uvicorn bot_webhook:app --reload --port 8001
    ```

---

### ✅ Resultado
El usuario puede gestionar su agenda y revisar/enviar correos directamente desde Telegram, con una arquitectura modular que permite agregar más herramientas en el futuro sin romper el código existente.
