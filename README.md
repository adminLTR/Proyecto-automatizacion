# 🤖 Telegram Automation Bot

Bot de automatización para Telegram que permite gestionar Gmail y Google Calendar mediante comandos simples. Construido con Flask usando arquitectura MVC, Docker y buenas prácticas de seguridad.

## 📋 Características

### 📧 Gestión de Email (Gmail)
- **111**: Enviar email de prueba a un destinatario predeterminado
- **112**: Eliminar emails antiguos (configurable, por defecto 7 días)
- **113**: Leer y listar emails de hoy

### 📅 Gestión de Calendario (Google Calendar)
- **211**: Ver eventos del mes actual
- **212**: Crear evento nuevo (por defecto: cumpleaños de hoy)
- **213**: Eliminar todos los eventos de hoy (fecha parametrizable)

## 🏗️ Arquitectura

El proyecto sigue una arquitectura **Modelo-Vista-Controlador (MVC)** profesional:

```
Proyecto-automatizacion/
├── app/
│   ├── config/           # Configuración y variables de entorno
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── controllers/      # Lógica de negocio para cada dominio
│   │   ├── __init__.py
│   │   ├── email_controller.py
│   │   └── calendar_controller.py
│   ├── models/           # Modelos de datos (futuro)
│   │   └── __init__.py
│   ├── services/         # Servicios externos (Google, Telegram)
│   │   ├── __init__.py
│   │   ├── google_service.py
│   │   └── telegram_service.py
│   ├── views/            # Rutas y endpoints Flask
│   │   ├── __init__.py
│   │   └── webhook_view.py
│   └── __init__.py       # Inicialización de la app Flask
├── bot_Webhooks/         # Código legacy (referencia)
├── telegram-bot/         # Código legacy (referencia)
├── tools/                # Código legacy (referencia)
├── .env.example          # Plantilla de variables de entorno
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py                # Punto de entrada de la aplicación
└── README.md
```

## 🚀 Instalación y Configuración

### Prerrequisitos

1. **Python 3.11+**
2. **Docker y Docker Compose** (para despliegue containerizado)
3. **Cuenta de Google** con acceso a Gmail y Calendar
4. **Bot de Telegram** (obtener token de [@BotFather](https://t.me/botfather))

### Paso 1: Clonar el repositorio

```bash
git clone <tu-repositorio>
cd Proyecto-automatizacion
```

### Paso 2: Configurar Google API

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las APIs:
   - Gmail API
   - Google Calendar API
4. Crea credenciales OAuth 2.0:
   - Tipo: Aplicación de escritorio
   - Descarga el archivo JSON
5. Renombra el archivo a `credentials.json` y colócalo en la raíz del proyecto

### Paso 3: Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
```

Configuración mínima requerida en `.env`:

```env
# Telegram Bot Token (obtener de @BotFather)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Email por defecto para pruebas
DEFAULT_EMAIL_RECIPIENT=tu-email@ejemplo.com

# Clave secreta (generar una aleatoria)
SECRET_KEY=tu-clave-secreta-muy-segura-aqui

# Opcional: Configurar webhook (si usas ngrok o servidor público)
USE_WEBHOOK=False
WEBHOOK_URL=https://tu-dominio.com/webhook
```

### Paso 4: Primera autenticación con Google

**Importante**: Debes autenticar la aplicación con Google antes de usar Docker.

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la app localmente por primera vez
python run.py
```

Esto abrirá un navegador para autorizar la aplicación. Una vez autorizado, se generará el archivo `token.json`.

## 🐳 Despliegue con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir y levantar el contenedor
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el contenedor
docker-compose down
```

### Opción 2: Docker manual

```bash
# Construir la imagen
docker build -t telegram-automation-bot .

# Ejecutar el contenedor
docker run -d \
  --name telegram-bot \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  -v $(pwd)/token.json:/app/token.json \
  telegram-automation-bot
```

## 🔧 Ejecución sin Docker

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📱 Configurar Webhook de Telegram (Opcional)

Si quieres usar webhooks en lugar de polling:

1. Configura una URL pública (usando ngrok o un servidor):
   ```bash
   ngrok http 5000
   ```

2. Actualiza `.env`:
   ```env
   USE_WEBHOOK=True
   WEBHOOK_URL=https://tu-url-de-ngrok.ngrok.io/webhook
   ```

3. El webhook se configurará automáticamente al iniciar la aplicación.

## 🎯 Uso

1. **Inicia una conversación con tu bot en Telegram**
2. **Envía** `/start` para ver los comandos disponibles
3. **Envía un código de comando** para ejecutar una acción:

### Ejemplos:

```
Usuario: /start
Bot: [Muestra menú con todos los comandos]

Usuario: 111
Bot: ✅ Email enviado exitosamente
     📧 Destinatario: tu-email@ejemplo.com
     ...

Usuario: 211
Bot: 📅 Eventos de Noviembre 2025 (5)
     1. Reunión de equipo
        📅 25/11/2025 14:00
     ...

Usuario: 212
Bot: ✅ Evento creado exitosamente
     📋 Título: Cumpleaños
     📅 Fecha: 2025-11-25
     ...
```

## 🔐 Seguridad y Buenas Prácticas

✅ **Variables de entorno** para datos sensibles  
✅ **Archivo `.gitignore`** para evitar commits de credenciales  
✅ **Docker multi-stage** (puede optimizarse más)  
✅ **Health checks** en Docker  
✅ **Logging estructurado**  
✅ **Validación de configuración** al inicio  
✅ **Manejo de errores** robusto  
✅ **Separación de responsabilidades** (MVC)

## 🛠️ Desarrollo

### Estructura del Código

- **`app/config/`**: Gestión de configuración centralizada
- **`app/controllers/`**: Lógica de negocio para cada dominio (email, calendar)
- **`app/services/`**: Comunicación con APIs externas (Google, Telegram)
- **`app/views/`**: Endpoints y rutas Flask
- **`app/models/`**: Modelos de datos (preparado para futuras extensiones)

### Extender Funcionalidad

Para agregar un nuevo comando:

1. Agregar el handler en el controlador correspondiente
2. Registrar la ruta en `webhook_view.py`
3. Actualizar la documentación

## 📊 Endpoints API

- `GET /` - Información del servicio
- `GET /health` - Health check para monitoreo
- `POST /webhook` - Webhook para recibir mensajes de Telegram

## 🧪 Testing (Futuro)

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/
```

## 📝 Comandos Disponibles

| Código | Categoría | Acción | Parámetros |
|--------|-----------|--------|------------|
| `111` | Email | Enviar email de prueba | Por defecto |
| `112` | Email | Eliminar emails antiguos | 7 días (configurable) |
| `113` | Email | Leer emails de hoy | - |
| `211` | Calendar | Ver eventos del mes | - |
| `212` | Calendar | Crear evento | Fecha: hoy, Título: "Cumpleaños" |
| `213` | Calendar | Eliminar eventos de hoy | Fecha: hoy (parametrizable) |

## 🐛 Troubleshooting

### Error: "TELEGRAM_BOT_TOKEN is not set"
- Verifica que `.env` existe y contiene `TELEGRAM_BOT_TOKEN`
- Asegúrate de que Docker está cargando el archivo `.env`

### Error: "Google credentials file not found"
- Verifica que `credentials.json` está en la raíz del proyecto
- Asegúrate de haber descargado las credenciales de Google Cloud Console

### Error: "Invalid grant" al autenticar con Google
- Elimina `token.json` y vuelve a autenticar
- Verifica que las APIs están habilitadas en Google Cloud

### El bot no responde
- Verifica que el servicio está ejecutándose: `docker-compose ps`
- Revisa los logs: `docker-compose logs -f`
- Verifica que el webhook está configurado correctamente (si aplica)

## 📄 Licencia

Este proyecto es de código abierto. Siéntete libre de usar, modificar y distribuir.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando Flask, Docker y Google APIs**
