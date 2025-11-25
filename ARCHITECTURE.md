# Telegram Automation Bot - Arquitectura del Proyecto

## 📁 Estructura del Proyecto

```
Proyecto-automatizacion/
│
├── app/                          # Aplicación principal
│   ├── __init__.py              # Inicialización de Flask
│   │
│   ├── config/                  # ⚙️ CONFIGURACIÓN
│   │   ├── __init__.py
│   │   └── settings.py          # Variables de entorno y configuración
│   │
│   ├── models/                  # 📊 MODELOS (Futuro - Base de datos)
│   │   └── __init__.py
│   │
│   ├── views/                   # 🌐 VISTAS (Rutas/Endpoints)
│   │   ├── __init__.py
│   │   └── webhook_view.py      # Webhook de Telegram
│   │
│   ├── controllers/             # 🎮 CONTROLADORES (Lógica de negocio)
│   │   ├── __init__.py
│   │   ├── email_controller.py  # Lógica de comandos de email
│   │   └── calendar_controller.py  # Lógica de comandos de calendario
│   │
│   └── services/                # 🔧 SERVICIOS (APIs externas)
│       ├── __init__.py
│       ├── google_service.py    # Gmail + Google Calendar API
│       └── telegram_service.py  # Telegram Bot API
│
├── bot_Webhooks/                # 📦 Código legacy (FastAPI)
├── telegram-bot/                # 📦 Código legacy (Polling)
├── tools/                       # 📦 Código legacy (Herramientas)
│
├── .env                         # 🔐 Variables de entorno (NO commitear)
├── .env.example                 # 📝 Plantilla de variables
├── .env.development             # 🛠️ Configuración de desarrollo
├── .gitignore                   # 🚫 Archivos ignorados por git
├── .dockerignore                # 🐳 Archivos ignorados por Docker
│
├── Dockerfile                   # 🐳 Imagen Docker
├── docker-compose.yml           # 🐳 Orquestación Docker
│
├── requirements.txt             # 📦 Dependencias Python
├── run.py                       # 🚀 Punto de entrada (desarrollo)
├── wsgi.py                      # 🚀 Punto de entrada (producción)
│
├── setup.sh                     # 🔧 Script de setup (Linux/Mac)
├── setup.ps1                    # 🔧 Script de setup (Windows)
│
├── README.md                    # 📖 Documentación principal
├── QUICKSTART.md                # 🚀 Guía de inicio rápido
└── ARCHITECTURE.md              # 📐 Este archivo
```

## 🏗️ Arquitectura MVC

### Modelo (Models)
- **Ubicación**: `app/models/`
- **Propósito**: Definir estructuras de datos y interacciones con base de datos
- **Estado**: Preparado para futuras extensiones
- **Uso futuro**: Modelos SQLAlchemy, Pydantic schemas, etc.

### Vista (Views)
- **Ubicación**: `app/views/`
- **Propósito**: Definir rutas y endpoints HTTP
- **Componentes**:
  - `webhook_view.py`: Maneja peticiones POST de Telegram
  - Endpoints: `/webhook`, `/health`, `/`

### Controlador (Controllers)
- **Ubicación**: `app/controllers/`
- **Propósito**: Implementar lógica de negocio
- **Componentes**:
  - `email_controller.py`: Gestión de comandos de email (111, 112, 113)
  - `calendar_controller.py`: Gestión de comandos de calendario (211, 212, 213)

### Servicios (Services)
- **Ubicación**: `app/services/`
- **Propósito**: Abstraer comunicación con APIs externas
- **Componentes**:
  - `google_service.py`: Gmail y Calendar API
  - `telegram_service.py`: Telegram Bot API

### Configuración (Config)
- **Ubicación**: `app/config/`
- **Propósito**: Centralizar configuración
- **Componentes**:
  - `settings.py`: Carga variables de entorno y valida configuración

## 🔄 Flujo de Datos

```
1. Usuario envía mensaje en Telegram
        ↓
2. Telegram envía POST a /webhook
        ↓
3. webhook_view.py recibe y parsea el mensaje
        ↓
4. Enruta al controlador apropiado (email o calendar)
        ↓
5. Controlador ejecuta lógica de negocio
        ↓
6. Controlador llama a servicios (Google, Telegram)
        ↓
7. Servicios interactúan con APIs externas
        ↓
8. Respuesta se envía de vuelta al usuario
```

## 🔌 Integraciones Externas

### Google APIs
- **Gmail API**: Enviar, leer y eliminar emails
- **Calendar API**: Crear, listar y eliminar eventos
- **Autenticación**: OAuth 2.0 con refresh token

### Telegram Bot API
- **Webhook**: Recibe mensajes en tiempo real
- **Polling**: Alternativa para desarrollo local
- **Formato**: JSON con estructura estándar de Telegram

## 🐳 Arquitectura Docker

```
┌─────────────────────────────────────┐
│     Docker Container                │
│  ┌───────────────────────────────┐  │
│  │   Gunicorn (WSGI Server)      │  │
│  │   ├─ Worker 1                 │  │
│  │   └─ Worker 2                 │  │
│  └───────────────────────────────┘  │
│              ↕                       │
│  ┌───────────────────────────────┐  │
│  │   Flask Application           │  │
│  │   (app/)                      │  │
│  └───────────────────────────────┘  │
│              ↕                       │
│  ┌───────────────────────────────┐  │
│  │   Volumes                     │  │
│  │   ├─ credentials.json (RO)   │  │
│  │   └─ token.json              │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
           ↕
    Port 5000 → Host
```

## 🛡️ Seguridad

### Variables de Entorno
- Todas las credenciales en `.env`
- `.env` excluido del control de versiones
- Validación al inicio de la aplicación

### Google OAuth 2.0
- Credenciales separadas (`credentials.json`)
- Token de refresh persistente (`token.json`)
- Scopes mínimos necesarios

### Docker
- Usuario no-root (puede mejorarse)
- Secretos via variables de entorno
- Volúmenes de solo lectura para credenciales

## 📊 Patrones de Diseño

### Singleton
- Servicios (GoogleService, TelegramService)
- Controladores (EmailController, CalendarController)
- Configuración (Config)

### Factory
- `create_app()`: Crea instancia de Flask configurada

### Dependency Injection
- Controladores reciben servicios al inicializarse

### Blueprint (Flask)
- Rutas organizadas en blueprints para modularidad

## 🚀 Despliegue

### Desarrollo
```bash
python run.py
```
- Flask development server
- Hot reload activado
- Debug mode

### Producción
```bash
docker-compose up -d
```
- Gunicorn WSGI server
- 2 workers
- Health checks
- Auto-restart

## 🔮 Futuras Mejoras

### Corto Plazo
- [ ] Tests unitarios y de integración
- [ ] Manejo de comandos con parámetros dinámicos
- [ ] Interfaz web para configuración

### Medio Plazo
- [ ] Base de datos (PostgreSQL/SQLite)
- [ ] Sistema de usuarios y permisos
- [ ] Programación de tareas (Celery)
- [ ] Métricas y monitoreo (Prometheus)

### Largo Plazo
- [ ] Soporte multi-idioma
- [ ] Integración con más servicios (Notion, Trello, etc.)
- [ ] Dashboard web con React/Vue
- [ ] API REST completa

## 📚 Stack Tecnológico

### Backend
- **Flask**: Framework web minimalista
- **Gunicorn**: WSGI server para producción
- **Python 3.11**: Lenguaje de programación

### APIs
- **Google Calendar API**: Gestión de calendario
- **Gmail API**: Gestión de correo
- **Telegram Bot API**: Chatbot

### Infraestructura
- **Docker**: Containerización
- **Docker Compose**: Orquestación
- **Linux**: SO base del contenedor

### Herramientas
- **python-dotenv**: Variables de entorno
- **requests**: Cliente HTTP
- **google-api-python-client**: Cliente Google APIs

## 🧪 Testing (Propuesto)

```
tests/
├── unit/
│   ├── test_email_controller.py
│   ├── test_calendar_controller.py
│   ├── test_google_service.py
│   └── test_telegram_service.py
├── integration/
│   ├── test_webhook_flow.py
│   └── test_google_integration.py
└── conftest.py
```

## 📝 Notas de Desarrollo

### Convenciones de Código
- PEP 8 para estilo Python
- Docstrings en formato Google
- Type hints en funciones públicas
- Nombres descriptivos en inglés

### Git Workflow
- `main`: Producción estable
- `develop`: Desarrollo activo
- `feature/*`: Nuevas características
- `hotfix/*`: Correcciones urgentes

### Logging
- INFO: Operaciones normales
- WARNING: Situaciones inesperadas no críticas
- ERROR: Errores que afectan funcionalidad
- DEBUG: Información detallada para desarrollo

---

**Última actualización**: Noviembre 2025
