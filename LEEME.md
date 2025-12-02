# ✅ TU BOT ESTÁ LISTO

## 🚀 Inicio Rápido (3 Pasos)

### 1️⃣ Configura tu token de Telegram

1. Abre Telegram y busca `@BotFather`
2. Envía `/newbot` y sigue las instrucciones
3. **Copia el token** que te da (formato: `123456789:ABCdef...`)

4. **Edita el archivo `.env`**:
   ```bash
   notepad .env
   ```

5. **Pega tu token** en la línea `TELEGRAM_BOT_TOKEN`:
   ```
   TELEGRAM_BOT_TOKEN=TU_TOKEN_AQUI
   DEFAULT_EMAIL_RECIPIENT=tu-email@ejemplo.com
   ```

6. **Guarda y cierra** el archivo

### 2️⃣ Inicia el servidor

**Haz doble click en:**
```
START_SERVER.bat
```

O ejecuta en PowerShell:
```powershell
venv_new\Scripts\python.exe start.py
```

Verás:
```
✅ Application initialized successfully!
🌐 Server starting on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.114:5000
```

### 3️⃣ Habla con tu bot

1. Abre Telegram
2. Busca tu bot (el nombre que le diste)
3. Envía `/start`
4. ¡Listo! Tu bot está funcionando

---

## 📱 Comandos Disponibles

**Información (sin Google):**
- `/start` - Menú de ayuda
- `/help` - Lista de comandos

**Con Google configurado:**

### Email
- `111` - Enviar email de prueba
- `112` - Eliminar emails antiguos (7 días)
- `113` - Leer emails de hoy

### Calendar
- `211` - Ver eventos del mes
- `212` - Crear evento de cumpleaños
- `213` - Eliminar eventos de hoy

---

## ⚙️ Configuración de Google (Opcional)

Si quieres usar las funciones de Gmail y Calendar:

### Paso 1: Crear proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita las APIs:
   - Gmail API
   - Google Calendar API

### Paso 2: Crear credenciales

1. Ve a "Credenciales" → "Crear credenciales"
2. Selecciona "ID de cliente OAuth 2.0"
3. Tipo de aplicación: "Aplicación de escritorio"
4. Descarga el archivo JSON
5. **Renómbralo a `credentials.json`**
6. **Colócalo en la carpeta del proyecto** (junto a start.py)

### Paso 3: Autenticar

1. Ejecuta:
   ```bash
   venv_new\Scripts\python.exe start.py
   ```

2. Se abrirá tu navegador automáticamente
3. Inicia sesión con tu cuenta de Google
4. Autoriza las APIs
5. ¡Listo! Se creará `token.json` automáticamente

---

## 🔧 Comandos Útiles

### Verificar que el servidor funciona
```powershell
# En otra terminal PowerShell:
Invoke-WebRequest -Uri "http://localhost:5000/health"

# Deberías ver:
{"status":"healthy","service":"telegram-automation-bot"}
```

### Ver logs
Los logs aparecen directamente en la terminal donde ejecutaste el servidor.

### Detener el servidor
Presiona `CTRL+C` en la terminal donde está corriendo.

---

## 🐛 Solución de Problemas

### ❌ "No module named 'flask'"
```powershell
# Reinstalar dependencias:
venv_new\Scripts\python.exe -m pip install -r requirements.txt
```

### ❌ El bot no responde en Telegram
1. Verifica que el servidor está corriendo (deberías ver "Running on...")
2. Verifica que pusiste el token correcto en `.env`
3. Revisa los logs en la terminal

### ❌ "Google service not authenticated"
Esto es normal si no configuraste `credentials.json`. El bot funciona sin Google, solo que los comandos 111-113 y 211-213 no funcionarán.

### ❌ Puerto 5000 ya está en uso
```powershell
# Ver qué proceso usa el puerto:
netstat -ano | findstr :5000

# Anota el PID (última columna) y detenlo:
taskkill /PID <número> /F
```

### ❌ Error al crear entorno virtual
Asegúrate de tener Python 3.11 instalado:
```powershell
python --version
# Debe mostrar Python 3.11.x
```

---

## 📁 Estructura del Proyecto

```
Proyecto-automatizacion/
├── START_SERVER.bat          ← 🔥 Ejecuta esto para iniciar
├── start.py                  ← Script de inicio
├── .env                      ← Tu token de Telegram aquí
├── credentials.json          ← Credenciales de Google (opcional)
├── token.json                ← Token de Google (se crea automáticamente)
├── requirements.txt          ← Dependencias
├── venv_new/                 ← Entorno virtual (no tocar)
└── app/                      ← Código del bot
    ├── __init__.py
    ├── config/
    ├── controllers/
    ├── services/
    └── views/
```

---

## 🐳 Docker (Avanzado)

**⚠️ IMPORTANTE**: Primero debes autenticar Google con Python (pasos anteriores).

```bash
# Una vez tengas token.json:
docker-compose up -d

# Ver logs:
docker-compose logs -f

# Detener:
docker-compose down
```

---

## 📚 Documentación Adicional

- `ARCHITECTURE.md` - Arquitectura técnica del proyecto
- `CHECKLIST.md` - Lista de verificación completa
- `QUICKSTART.md` - Guía detallada paso a paso

---

## ✅ Checklist Rápido

- [ ] Creé mi bot con @BotFather
- [ ] Copié el token a `.env`
- [ ] Ejecuté `START_SERVER.bat`
- [ ] Veo "Running on http://127.0.0.1:5000"
- [ ] Envié `/start` a mi bot en Telegram
- [ ] Mi bot respondió

**¿Todo listo?** ¡Felicidades! 🎉

**¿Tienes problemas?** Revisa la sección "Solución de Problemas" arriba.

---

**Hecho con ❤️ usando Flask, Python y Telegram Bot API**
