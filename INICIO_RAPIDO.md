# 🚀 GUÍA DE INICIO RÁPIDO

## ✅ El bot YA ESTÁ FUNCIONANDO!

Tu servidor Flask está operativo. Ahora sigue estos pasos para usarlo:

## 📝 Paso 1: Configurar el Bot de Telegram

1. **Abre Telegram** y busca `@BotFather`
2. **Envía** `/newbot`
3. **Sigue las instrucciones** y elige un nombre para tu bot
4. **Copia el token** que te da (formato: `123456789:ABCdefGHI...`)

5. **Edita el archivo `.env`**:
   ```bash
   notepad .env  # Windows
   nano .env     # Linux/Mac
   ```

6. **Pega tu token**:
   ```
   TELEGRAM_BOT_TOKEN=TU_TOKEN_AQUI
   DEFAULT_EMAIL_RECIPIENT=tu-email@ejemplo.com
   ```

## 🎯 Paso 2: Iniciar el Servidor

**Opción A - Script automático (Recomendado)**:
```bash
# Hacer doble click en:
quickstart.bat

# O ejecutar:
.\quickstart.bat
```

**Opción B - Manual**:
```bash
# Activar entorno virtual
env\Scripts\activate

# Iniciar servidor
python start.py
```

El servidor se iniciará en: `http://localhost:5000`

## 📱 Paso 3: Probar tu Bot

1. **Abre Telegram**
2. **Busca tu bot** (el nombre que le diste)
3. **Envía** `/start`
4. **Prueba comandos**:
   - `111` - Enviar email (requiere Google configurado)
   - `211` - Ver eventos (requiere Google configurado)

## 🔧 Configuración de Google (Opcional)

Para usar funciones de Gmail y Calendar:

1. **Ve a** [Google Cloud Console](https://console.cloud.google.com/)
2. **Crea un proyecto**
3. **Habilita**:
   - Gmail API
   - Google Calendar API
4. **Crea credenciales** OAuth 2.0 (Aplicación de escritorio)
5. **Descarga** el archivo JSON
6. **Renómbralo** a `credentials.json`
7. **Colócalo** en la carpeta del proyecto
8. **Ejecuta** `python start.py` - se abrirá el navegador para autorizar

## ✅ Verificar que Funciona

```powershell
# En otra terminal, prueba:
Invoke-WebRequest -Uri "http://localhost:5000/health"

# Deberías ver:
{"status":"healthy","service":"telegram-automation-bot"}
```

## 📋 Comandos Disponibles

### Sin configuración de Google (solo información):
- `/start` - Menú de ayuda
- `/help` - Lista de comandos

### Con Google configurado:
**Email:**
- `111` - Enviar email de prueba
- `112` - Eliminar emails antiguos (7 días por defecto)
- `113` - Leer emails de hoy

**Calendar:**
- `211` - Ver eventos del mes
- `212` - Crear evento de cumpleaños
- `213` - Eliminar eventos de hoy

## 🐛 Solución de Problemas

### El bot no responde
```bash
# 1. Verifica que el servidor está corriendo
# Deberías ver: "Running on http://127.0.0.1:5000"

# 2. Verifica que tienes el token correcto en .env
type .env

# 3. Verifica los logs en la terminal
```

### Error: "Google service not authenticated"
```
Esto es normal si no has configurado credentials.json
El bot funcionará, pero sin funciones de Gmail/Calendar
```

### Puerto 5000 en uso
```powershell
# Detener proceso que usa el puerto 5000:
netstat -ano | findstr :5000
# Anota el PID y luego:
taskkill /PID <número> /F
```

## 🐳 Usar con Docker (Avanzado)

```bash
# IMPORTANTE: Primero debes tener credentials.json y token.json
# Ejecuta primero con Python para autenticar Google

# Luego:
docker-compose up -d

# Ver logs:
docker-compose logs -f

# Detener:
docker-compose down
```

## 📚 Documentación Completa

- `README.md` - Guía detallada
- `ARCHITECTURE.md` - Arquitectura técnica
- `CHECKLIST.md` - Lista de verificación completa

## 🎉 ¡Listo!

Tu bot está funcionando. Solo necesitas:
1. ✅ Configurar el token de Telegram en `.env`
2. ✅ Ejecutar `python start.py`
3. ✅ Hablar con tu bot en Telegram

**Para funciones de Google** (opcional):
4. ⚠️ Configurar `credentials.json`
5. ⚠️ Autenticar con `python start.py`

---

**¿Necesitas ayuda?** Lee los archivos de documentación o abre un issue en GitHub.
