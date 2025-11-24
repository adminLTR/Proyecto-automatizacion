# 📅 Calendar Tools (Documentación)

Este documento describe el uso del script `calendar_tools.py`, diseñado para que un Agente de IA interactúe con **Google Calendar**.

## 📋 Capacidades
El agente puede:
1. **Listar** los próximos 10 eventos.
2. **Crear** nuevos eventos validando fechas y horas.
3. **Actualizar** eventos existentes (reprogramar o renombrar).
4. **Eliminar** eventos por ID.

---

## ☁️ Configuración de Google Cloud (Proyecto Existente)

El proyecto en Google Cloud Platform ya ha sido creado y configurado. El correo de prueba ya ha sido añadido a la lista de acceso.

### 1. Descargar Credenciales (Paso Obligatorio)
Para que el script funcione en tu máquina local, necesitas descargar el archivo de credenciales del proyecto compartido:

1. Ve a la sección de **Credenciales** en la consola de Google Cloud del proyecto.
2. Busca el **ID de cliente de OAuth 2.0** (Tipo: Aplicación de escritorio) que ya fue creado.
3. Haz clic en el icono de descarga (⬇️) para bajar el archivo JSON.
4. **Renombra** el archivo descargado a `credentials.json`.
5. **Mueve** el archivo `credentials.json` dentro de esta carpeta `tools/`.

> **Nota:** Sin este archivo, el script fallará inmediatamente.

---

## 📦 Instalación de Dependencias

Antes de ejecutar nada, instala las librerías de Google en tu entorno virtual:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib


---

## 🤖 ¿Cómo usa el Agente este script?

Este archivo está diseñado para funcionar como una "caja de herramientas" para el Agente, no para ser ejecutado manualmente por un humano todo el tiempo.

El flujo de trabajo es el siguiente:

1. **Importación:** El script principal del bot (ej. `main.py` o `agent.py`) importa las funciones que comienzan con `tool_`.
2. **Detección de Intención:**
   - Usuario dice: *"Agenda una reunión de revisión mañana a las 3 de la tarde"*.
   - El Agente (LLM) analiza la frase, entiende que necesita el calendario y decide usar la herramienta `tool_crear_evento`.
3. **Extracción de Parámetros:**
   - El Agente calcula automáticamente los datos necesarios:
     - `titulo`: "Reunión de revisión"
     - `fecha`: "2025-11-25" (Calculado basado en "mañana")
     - `hora_inicio`: "15:00"
4. **Ejecución:** El script `calendar_tools.py` se conecta a Google, crea el evento y devuelve un mensaje de confirmación (String).
5. **Respuesta Final:** El Agente lee ese mensaje de confirmación y le dice al usuario: "Listo, he agendado tu reunión para mañana a las 15:00 hrs".

