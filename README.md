# 🤖 Bot de Telegram - Automatización Email y Calendar

Bot de Telegram simple con Flask que automatiza tareas de Gmail y Google Calendar.

## 📋 Requisitos

- Python 3.11+
- Cuenta de Telegram
- Cuenta de Google (para Gmail y Calendar)

## 🚀 Instalación Rápida

### 1. Clonar o descargar el proyecto

```bash
cd Proyecto-automatizacion
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Copia el archivo de ejemplo:
```bash
copy .env.example .env
```

Edita `.env` y configura:
- `TELEGRAM_BOT_TOKEN` - Tu token de @BotFather
- `DEFAULT_EMAIL_RECIPIENT` - Email por defecto
- Otras configuraciones opcionales

### 6. Configurar Google APIs (Opcional)

Para usar funciones de Gmail y Calendar:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo
3. Habilita **Gmail API** y **Google Calendar API**
4. Crea credenciales OAuth 2.0 (Aplicación de escritorio)
5. Descarga el archivo JSON y renómbralo a `credentials.json`
6. Colócalo en la carpeta raíz del proyecto

### 7. Ejecutar el bot

```bash
python app.py
```

La primera vez se abrirá tu navegador para autorizar Google APIs.

## 📱 Comandos Disponibles

### Email (Gmail)
- **111** - Enviar email de prueba
- **112** - Eliminar emails antiguos (configurable en `.env`)
- **113** - Leer emails de hoy

### Calendar (Google Calendar)
- **211** - Ver eventos del mes actual
- **212** - Crear evento (cumpleaños por defecto, hoy a las 10:00)
- **213** - Eliminar eventos de hoy

### Ayuda
- **/start** o **/help** - Ver lista de comandos

## ⚙️ Configuración Avanzada

### Parámetros personalizables en `.env`:

```bash
# Días hacia atrás para eliminar emails (comando 112)
EMAIL_DELETE_DAYS_AGO=7

# Zona horaria para eventos del calendario
CALENDAR_TIMEZONE=America/Lima

# Puerto del servidor
APP_PORT=5000
```

### Personalizar funciones en el código

Todas las funciones en `app.py` son parametrizables:

```python
# Ejemplo: Cambiar días para eliminar emails
handle_email_command_112(chat_id, days_ago=14)  # 14 días en lugar de 7

# Ejemplo: Crear evento personalizado
handle_calendar_command_212(
    chat_id, 
    title="Reunión",
    date="2024-12-25",
    start_time="15:00",
    end_time="16:00"
)

# Ejemplo: Eliminar eventos de fecha específica
handle_calendar_command_213(chat_id, date="2024-12-20")
```

## 🔧 Estructura del Proyecto

```
Proyecto-automatizacion/
├── app.py              # ⭐ Archivo principal con toda la lógica
├── .env                # Configuración (no subir a Git)
├── .env.example        # Plantilla de configuración
├── requirements.txt    # Dependencias de Python
├── credentials.json    # Credenciales de Google (no subir a Git)
├── token.json          # Token de autenticación Google (generado automáticamente)
├── venv/               # Entorno virtual (no subir a Git)
└── README.md           # Este archivo
```

## 🐛 Solución de Problemas

### El bot no responde
1. Verifica que el servidor esté corriendo (`python app.py`)
2. Revisa que `TELEGRAM_BOT_TOKEN` esté correcto en `.env`
3. Verifica los logs en la consola

### "Google not authenticated"
1. Asegúrate de tener `credentials.json` en la carpeta raíz
2. Ejecuta `python app.py` y autoriza cuando se abra el navegador
3. Se creará automáticamente `token.json`

### Puerto 5000 en uso
Cambia el puerto en `.env`:
```bash
APP_PORT=8000
```

O detén el proceso que usa el puerto:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <número> /F
```

## 📚 Endpoints de la API

- `GET /` - Información del servicio
- `GET /health` - Health check del servidor
- `POST /webhook` - Webhook de Telegram (recibe mensajes)

## 🔐 Seguridad

- **NO SUBAS** a Git los archivos:
  - `.env`
  - `credentials.json`
  - `token.json`
  
- Crea un archivo `.gitignore`:
```
venv/
.env
credentials.json
token.json
__pycache__/
*.pyc
```

## 📝 Notas

- Todos los comandos son parametrizables desde el código
- Las fechas por defecto son configurables
- El bot funciona en modo webhook (no polling)
- Para producción, usa un servidor WSGI como Gunicorn

## 🛠️ Desarrollo

Para modificar el bot, edita directamente `app.py`. Todo está en un solo archivo para facilitar el mantenimiento.

Las funciones principales:
- `handle_email_command_111/112/113` - Comandos de email
- `handle_calendar_command_211/212/213` - Comandos de calendar
- `GoogleService` - Clase para interactuar con Google APIs
- `send_telegram_message` - Enviar mensajes a Telegram

## 📄 Licencia

Este proyecto es de código abierto. Úsalo y modifícalo libremente.

---

**¿Necesitas ayuda?** Revisa los logs en la consola donde ejecutas `python app.py`
