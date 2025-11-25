# ✅ Checklist de Configuración - Telegram Automation Bot

## 📋 Pre-requisitos

- [ ] Python 3.11 o superior instalado
- [ ] Docker y Docker Compose instalados (opcional pero recomendado)
- [ ] Git instalado
- [ ] Editor de texto (VS Code, Notepad++, etc.)

## 🔑 Credenciales Necesarias

### 1. Token de Telegram Bot
- [ ] Ir a Telegram y buscar [@BotFather](https://t.me/botfather)
- [ ] Enviar comando `/newbot`
- [ ] Seguir instrucciones y elegir nombre
- [ ] Copiar el token que te proporciona (formato: `123456789:ABCdefGHI...`)
- [ ] Guardar el token en un lugar seguro

### 2. Google Cloud Credentials
- [ ] Ir a [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Crear un proyecto nuevo o usar uno existente
- [ ] Habilitar **Gmail API**
- [ ] Habilitar **Google Calendar API**
- [ ] Crear credenciales OAuth 2.0:
  - Tipo: Aplicación de escritorio
  - Descargar el archivo JSON
- [ ] Renombrar el archivo a `credentials.json`
- [ ] Colocar `credentials.json` en la raíz del proyecto

## 🛠️ Configuración Inicial

### 1. Clonar/Descargar Proyecto
- [ ] Proyecto descargado en tu máquina
- [ ] Navegar a la carpeta del proyecto

### 2. Configurar Variables de Entorno
- [ ] Copiar `.env.example` a `.env`
  ```bash
  # Windows
  copy .env.example .env
  
  # Linux/Mac
  cp .env.example .env
  ```
- [ ] Abrir `.env` con un editor de texto
- [ ] Completar las siguientes variables:
  - [ ] `TELEGRAM_BOT_TOKEN=` (tu token de Telegram)
  - [ ] `DEFAULT_EMAIL_RECIPIENT=` (tu email para pruebas)
  - [ ] `SECRET_KEY=` (cualquier string aleatorio largo)

### 3. Verificar Archivos
- [ ] Verificar que `credentials.json` existe en la raíz
- [ ] Verificar que `.env` existe y tiene valores

## 🚀 Primera Ejecución

### Opción A: Setup Automático (Recomendado)

**Windows:**
```powershell
# Ejecutar el script de setup
powershell -ExecutionPolicy Bypass -File setup.ps1

# O hacer doble click en:
quickstart.bat
```

**Linux/Mac:**
```bash
# Hacer ejecutable y correr
chmod +x setup.sh
./setup.sh
```

Checklist del script:
- [ ] Script ejecutado sin errores
- [ ] Virtual environment creado
- [ ] Dependencias instaladas
- [ ] Navegador abierto para autorizar Google
- [ ] Autorización completada
- [ ] Archivo `token.json` creado

### Opción B: Setup Manual

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Primera ejecución (autenticación Google)
python run.py
```

Checklist manual:
- [ ] Entorno virtual creado
- [ ] Entorno virtual activado
- [ ] Todas las dependencias instaladas sin errores
- [ ] Aplicación iniciada
- [ ] Navegador abierto automáticamente
- [ ] Cuenta de Google seleccionada
- [ ] Permisos aceptados:
  - [ ] Ver y administrar Gmail
  - [ ] Ver y administrar Calendar
- [ ] Archivo `token.json` creado en la raíz
- [ ] Servidor Flask ejecutándose en `http://localhost:5000`

## 🐳 Levantar con Docker

### Pre-requisitos Docker
- [ ] Docker Desktop instalado y ejecutándose
- [ ] `credentials.json` en la raíz del proyecto
- [ ] `token.json` creado (requiere autenticación previa)
- [ ] `.env` configurado

### Comandos Docker
```bash
# Construir y levantar
docker-compose up -d

# Verificar que está ejecutándose
docker-compose ps

# Ver logs
docker-compose logs -f
```

Checklist Docker:
- [ ] Imagen construida exitosamente
- [ ] Contenedor levantado
- [ ] Estado: "Up" (ejecutándose)
- [ ] Health check: "healthy"
- [ ] Logs sin errores críticos
- [ ] Endpoint `/health` responde: `curl http://localhost:5000/health`

## 📱 Probar el Bot

### 1. Encontrar tu Bot en Telegram
- [ ] Abrir Telegram
- [ ] Buscar tu bot por el nombre que le diste
- [ ] Iniciar conversación

### 2. Comandos de Prueba
- [ ] Enviar `/start` → Debe mostrar el menú de ayuda
- [ ] Enviar `/help` → Debe mostrar comandos disponibles
- [ ] Enviar `111` → Debe enviar email de prueba
- [ ] Verificar que llegó el email
- [ ] Enviar `211` → Debe mostrar eventos del mes
- [ ] Enviar `212` → Debe crear evento de cumpleaños
- [ ] Verificar evento en Google Calendar

### 3. Verificar Funcionalidades

**Email:**
- [ ] 111: Email enviado correctamente
- [ ] 112: Emails antiguos eliminados
- [ ] 113: Lista de emails de hoy mostrada

**Calendar:**
- [ ] 211: Eventos del mes listados
- [ ] 212: Evento creado exitosamente
- [ ] 213: Eventos eliminados

## 🔍 Verificación del Sistema

### Endpoints API
```bash
# Health check
curl http://localhost:5000/health

# Info del servicio
curl http://localhost:5000/
```

- [ ] `/health` retorna status "healthy"
- [ ] `/` retorna información del servicio

### Logs
```bash
# Sin Docker
# Los logs aparecen en la consola donde ejecutaste python run.py

# Con Docker
docker-compose logs -f telegram-bot
```

- [ ] Logs muestran "Application initialized successfully"
- [ ] No hay errores críticos en los logs
- [ ] Los comandos se procesan correctamente

## 🐛 Troubleshooting

### Si algo falla, verificar:

**Problema: Bot no responde**
- [ ] Verificar que el servicio está ejecutándose
- [ ] Verificar TOKEN de Telegram en `.env`
- [ ] Ver logs para errores

**Problema: Error de autenticación Google**
- [ ] `credentials.json` está en la raíz
- [ ] `token.json` fue creado correctamente
- [ ] Las APIs están habilitadas en Google Cloud

**Problema: Docker no inicia**
- [ ] Docker Desktop está ejecutándose
- [ ] `credentials.json` y `token.json` existen
- [ ] `.env` está configurado
- [ ] Puerto 5000 no está en uso

**Problema: "No module named 'app'"**
- [ ] Estás en la raíz del proyecto
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas

## ✅ Checklist Final

- [ ] ✅ Proyecto configurado
- [ ] ✅ Credenciales de Google obtenidas
- [ ] ✅ Token de Telegram obtenido
- [ ] ✅ `.env` configurado
- [ ] ✅ Autenticación de Google completada
- [ ] ✅ Servicio ejecutándose (Python o Docker)
- [ ] ✅ Bot responde en Telegram
- [ ] ✅ Comandos de email funcionan
- [ ] ✅ Comandos de calendar funcionan
- [ ] ✅ Health check responde OK

## 🎉 ¡Listo!

Si todos los checks están completos, tu bot está funcionando correctamente.

### Próximos Pasos
- [ ] Personalizar mensajes en `app/controllers/`
- [ ] Agregar más comandos según necesidad
- [ ] Configurar webhook con ngrok/servidor público
- [ ] Implementar base de datos para historial
- [ ] Agregar tests automatizados

---

**¿Necesitas ayuda?** Revisa `README.md`, `QUICKSTART.md` o `DEV_NOTES.md`
