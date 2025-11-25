# 🎨 Diagramas y Flujos - Telegram Automation Bot

## 📊 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                           TELEGRAM USER                              │
│                    (Envía comandos al bot)                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TELEGRAM BOT API                                │
│                   (Recibe y procesa mensajes)                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP POST
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FLASK APPLICATION                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    WEBHOOK ENDPOINT                           │  │
│  │                 POST /webhook (views/)                        │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │                                       │
│                              ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                     COMMAND ROUTER                            │  │
│  │         (Determina tipo de comando: 1XX o 2XX)                │  │
│  └──────────────┬───────────────────────────┬────────────────────┘  │
│                 │                           │                        │
│      ┌──────────▼──────────┐     ┌─────────▼──────────┐            │
│      │  Email Controller   │     │ Calendar Controller │            │
│      │   (controllers/)    │     │   (controllers/)    │            │
│      │                     │     │                     │            │
│      │ • 111: Send Email   │     │ • 211: List Events │            │
│      │ • 112: Delete Old   │     │ • 212: Create Event│            │
│      │ • 113: Read Today   │     │ • 213: Delete Today│            │
│      └──────────┬──────────┘     └─────────┬──────────┘            │
│                 │                           │                        │
│                 └──────────┬────────────────┘                        │
│                            │                                         │
│                            ▼                                         │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                      SERVICES LAYER                           │  │
│  │  ┌────────────────────┐        ┌────────────────────┐        │  │
│  │  │  Google Service    │        │ Telegram Service   │        │  │
│  │  │   (services/)      │        │   (services/)      │        │  │
│  │  │                    │        │                    │        │  │
│  │  │ • Gmail API        │        │ • Send Message     │        │  │
│  │  │ • Calendar API     │        │ • Send Keyboard    │        │  │
│  │  │ • OAuth 2.0        │        │ • Webhook Mgmt     │        │  │
│  │  └─────────┬──────────┘        └─────────┬──────────┘        │  │
│  └────────────┼───────────────────────────────┼──────────────────┘  │
└───────────────┼───────────────────────────────┼─────────────────────┘
                │                               │
                ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│    GOOGLE APIs           │    │   TELEGRAM BOT API       │
│                          │    │                          │
│ • Gmail API              │    │ • sendMessage            │
│ • Calendar API           │    │ • sendKeyboard           │
│ • OAuth 2.0 Auth         │    │ • Webhook                │
└──────────────────────────┘    └──────────────────────────┘
```

## 🔄 Flujo de Ejecución de Comando

### Ejemplo: Comando "111" (Enviar Email)

```
1. Usuario                    2. Telegram API              3. Webhook View
   │                             │                            │
   │  Envía "111"               │                            │
   ├──────────────────────────>│                            │
   │                            │  POST /webhook             │
   │                            ├──────────────────────────>│
   │                            │  {message: {text: "111"}}  │
   │                            │                            │
   │                            │                            │

4. Command Router              5. Email Controller         6. Google Service
   │                              │                           │
   │  Detecta comando "111"       │                           │
   ├─────────────────────────────>│                           │
   │                              │  handle_command("111")    │
   │                              ├──────────────────────────>│
   │                              │                           │
   │                              │  send_email(...)          │
   │                              │<──────────────────────────┤
   │                              │  {success: true}          │

7. Telegram Service            8. Telegram API             9. Usuario
   │                              │                           │
   │  send_message(chat_id, ✅)   │                           │
   ├─────────────────────────────>│                           │
   │                              │  Mensaje enviado          │
   │                              ├──────────────────────────>│
   │                              │  "✅ Email enviado..."     │
```

## 🏗️ Modelo MVC Implementado

```
┌─────────────────────────────────────────────────────────────┐
│                         MODEL (M)                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  app/models/                                        │    │
│  │  • Preparado para base de datos futura             │    │
│  │  • Estructuras de datos                             │    │
│  │  • Lógica de persistencia                           │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                             ▲
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                         VIEW (V)           │                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  app/views/                            │             │   │
│  │  • webhook_view.py                     │             │   │
│  │  • Flask Blueprints                    │             │   │
│  │  • Rutas HTTP                          ▼             │   │
│  │  • Request handling          ┌──────────────────┐    │   │
│  └──────────────────────────────│  CONTROLLER (C)  │────┘   │
│                                 │                  │        │
│                                 │  app/controllers/ │        │
│                                 │  • email_ctrl    │        │
│                                 │  • calendar_ctrl │        │
│                                 │  • Lógica negocio│        │
│                                 └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 🔌 Integración con APIs Externas

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROLLERS LAYER                         │
│  (Lógica de negocio - No conoce detalles de APIs)          │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ Llama a servicios abstractos
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVICES LAYER                            │
│  (Abstracción de APIs - Maneja detalles de comunicación)   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  GoogleService                                      │   │
│  │  • _authenticate()                                  │   │
│  │  • send_email()                                     │   │
│  │  • list_emails()                                    │   │
│  │  • delete_old_emails()                              │   │
│  │  • list_events()                                    │   │
│  │  • create_event()                                   │   │
│  │  • delete_events_by_date()                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  TelegramService                                    │   │
│  │  • send_message()                                   │   │
│  │  • send_keyboard()                                  │   │
│  │  • set_webhook()                                    │   │
│  │  • delete_webhook()                                 │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTP/HTTPS Requests
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL APIs                             │
│  • Google Gmail API                                         │
│  • Google Calendar API                                      │
│  • Telegram Bot API                                         │
└─────────────────────────────────────────────────────────────┘
```

## 🐳 Docker Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     HOST MACHINE                             │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               DOCKER CONTAINER                        │  │
│  │  ┌────────────────────────────────────────────────┐   │  │
│  │  │         Gunicorn (WSGI Server)                 │   │  │
│  │  │         Port: 5000                             │   │  │
│  │  │  ┌──────────┐        ┌──────────┐             │   │  │
│  │  │  │ Worker 1 │        │ Worker 2 │             │   │  │
│  │  │  └─────┬────┘        └────┬─────┘             │   │  │
│  │  │        │                  │                    │   │  │
│  │  │        └──────────┬───────┘                    │   │  │
│  │  │                   ▼                            │   │  │
│  │  │        ┌──────────────────────┐               │   │  │
│  │  │        │  Flask Application   │               │   │  │
│  │  │        │       (app/)         │               │   │  │
│  │  │        └──────────────────────┘               │   │  │
│  │  └────────────────────────────────────────────────┘   │  │
│  │                                                        │  │
│  │  VOLUMES (Mounted):                                   │  │
│  │  • credentials.json (Read-Only)                       │  │
│  │  • token.json (Read-Write)                            │  │
│  │  • logs/ (Read-Write)                                 │  │
│  │                                                        │  │
│  │  ENV VARS:                                             │  │
│  │  • TELEGRAM_BOT_TOKEN                                 │  │
│  │  • GOOGLE_CREDENTIALS_PATH                            │  │
│  │  • DEFAULT_EMAIL_RECIPIENT                            │  │
│  │  • etc.                                                │  │
│  └────────────────────────────┬───────────────────────────┘  │
│                               │                              │
│                               │ Port Mapping 5000:5000       │
└───────────────────────────────┼──────────────────────────────┘
                                │
                                ▼
                        External Access
                      http://localhost:5000
```

## 📱 Flujo de Comandos Completo

```
┌──────────────────────────────────────────────────────────────┐
│                    TELEGRAM USER                              │
└────────────┬─────────────────────────────────────────────────┘
             │
             │ Envía comando
             ▼
┌──────────────────────────────────────────────────────────────┐
│  COMMAND    │  CONTROLLER        │  SERVICE      │  ACTION   │
├──────────────────────────────────────────────────────────────┤
│  /start     │  webhook_view      │  telegram     │  Help msg │
│  /help      │  webhook_view      │  telegram     │  Help msg │
├──────────────────────────────────────────────────────────────┤
│  111        │  email_controller  │  google       │  Send     │
│  112        │  email_controller  │  google       │  Delete   │
│  113        │  email_controller  │  google       │  List     │
├──────────────────────────────────────────────────────────────┤
│  211        │  calendar_ctrl     │  google       │  List     │
│  212        │  calendar_ctrl     │  google       │  Create   │
│  213        │  calendar_ctrl     │  google       │  Delete   │
└──────────────────────────────────────────────────────────────┘
             │
             │ Respuesta al usuario
             ▼
┌──────────────────────────────────────────────────────────────┐
│                    TELEGRAM USER                              │
│              (Recibe respuesta del bot)                       │
└──────────────────────────────────────────────────────────────┘
```

## 🔐 Flujo de Autenticación OAuth 2.0

```
1. Primera Ejecución
   │
   ├─> ¿Existe token.json?
   │   │
   │   NO
   │   │
   │   ▼
   ├─> Leer credentials.json
   │   │
   │   ▼
   ├─> Iniciar OAuth Flow
   │   │
   │   ▼
   ├─> Abrir navegador
   │   │
   │   ▼
   ├─> Usuario autoriza
   │   │
   │   ▼
   ├─> Google devuelve tokens
   │   │
   │   ▼
   ├─> Guardar en token.json
   │   │
   │   ▼
   └─> ✅ Autenticado


2. Ejecuciones Siguientes
   │
   ├─> ¿Existe token.json?
   │   │
   │   SÍ
   │   │
   │   ▼
   ├─> Cargar token
   │   │
   │   ▼
   ├─> ¿Token válido?
   │   │
   │   SÍ────────────────────> ✅ Autenticado
   │   │
   │   NO (Expirado)
   │   │
   │   ▼
   ├─> ¿Tiene refresh_token?
   │   │
   │   SÍ
   │   │
   │   ▼
   ├─> Refrescar token
   │   │
   │   ▼
   ├─> Guardar nuevo token
   │   │
   │   ▼
   └─> ✅ Autenticado
```

## 📊 Estructura de Datos

### Mensaje de Telegram (Entrada)
```json
{
  "update_id": 123456789,
  "message": {
    "message_id": 1,
    "from": {
      "id": 12345,
      "first_name": "Juan",
      "username": "juan123"
    },
    "chat": {
      "id": 12345,
      "type": "private"
    },
    "text": "111"
  }
}
```

### Respuesta del Servicio (Interna)
```python
{
    'success': True,
    'message': 'Email sent successfully',
    'message_id': 'abc123xyz'
}
```

### Mensaje al Usuario (Salida)
```markdown
✅ **Email enviado exitosamente**

📧 Destinatario: `user@example.com`
📋 Asunto: Mensaje automático
🆔 ID: `abc123xyz`
```

---

**Este archivo proporciona una vista visual completa de cómo funciona el sistema**
