# Quick Start Guide

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Obtener Token de Telegram
1. Abre Telegram y busca [@BotFather](https://t.me/botfather)
2. Envía `/newbot`
3. Sigue las instrucciones y copia el token que te da

### Paso 2: Configurar Google API
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo
3. Habilita estas APIs:
   - Gmail API
   - Google Calendar API
4. Crea credenciales OAuth 2.0 (Aplicación de escritorio)
5. Descarga `credentials.json` y ponlo en la raíz del proyecto

### Paso 3: Configurar el proyecto

**En Windows:**
```powershell
# Copiar .env y editarlo
copy .env.example .env
notepad .env

# Pegar tu token de Telegram y email en .env
```

**En Linux/Mac:**
```bash
# Copiar .env y editarlo
cp .env.example .env
nano .env

# Pegar tu token de Telegram y email en .env
```

### Paso 4: Primera ejecución (autenticación Google)

**Opción A - Con Python:**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar (se abrirá el navegador para autorizar)
python run.py
```

**Opción B - Con script de setup:**

Windows:
```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

### Paso 5: Levantar con Docker

```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Verificar que está corriendo
curl http://localhost:5000/health
```

### Paso 6: ¡Probar el bot!

1. Abre Telegram
2. Busca tu bot (el nombre que le diste en BotFather)
3. Envía `/start`
4. Prueba un comando: `111` (enviar email)

## 📋 Comandos Rápidos

| Comando | Qué hace |
|---------|----------|
| `111` | Envía un email de prueba |
| `112` | Borra emails antiguos |
| `113` | Muestra emails de hoy |
| `211` | Lista eventos del mes |
| `212` | Crea un evento de cumpleaños |
| `213` | Borra eventos de hoy |

## 🐛 Problemas Comunes

### "No module named 'app'"
```bash
# Asegúrate de estar en la raíz del proyecto
cd Proyecto-automatizacion
python run.py
```

### "TELEGRAM_BOT_TOKEN is not set"
```bash
# Verifica que .env existe y tiene el token
cat .env  # Linux/Mac
type .env  # Windows
```

### Docker no encuentra credentials.json
```bash
# Verifica que el archivo existe
ls credentials.json  # Linux/Mac
dir credentials.json  # Windows

# Debe estar en la raíz del proyecto, al mismo nivel que docker-compose.yml
```

### El bot no responde
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar el contenedor
docker-compose restart
```

## 🎯 Siguiente Nivel

- Configura webhook con ngrok para producción
- Personaliza los mensajes en `app/controllers/`
- Agrega más comandos según tus necesidades
- Implementa base de datos para historial

## 📞 ¿Necesitas Ayuda?

Revisa el `README.md` principal para documentación completa.
