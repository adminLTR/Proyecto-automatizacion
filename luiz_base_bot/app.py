
import asyncio
import os
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime
import prompts

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Token obtenido desde archivo .env
TOKEN = os.getenv("TOKEN")

# Diccionario para mantener el estado de cada usuario
# user_states[user_id] = {'state': 'idle/collecting', 'data': {...}}
user_states = {}


# ========================================================================
# COMANDOS DEL BOT
# ========================================================================

async def start_command(update, context):
    """Handler para el comando /start"""
    user_id = update.effective_user.id

    # Inicializar estado del usuario
    user_states[user_id] = {
        'state': 'idle',
        'data': {}
    }

    welcome_message = """
¡Bienvenido al Asistente de Agendamiento de Reuniones!

Puedo ayudarte a agendar reuniones de manera conversacional.
Solo háblame de forma natural y yo entenderé.

Este bot utiliza computación autonómica con 4 principios:
- Auto-configuración: Configura parámetros automáticamente
- Auto-optimización: Sugiere mejores horarios
- Auto-curación: Detecta y repara datos faltantes
- Auto-protección: Valida y protege tus datos

Comandos disponibles:
/agendar - Iniciar el proceso para agendar una reunión
/cancelar - Cancelar el proceso actual
/ayuda - Mostrar esta ayuda

¡Puedes empezar escribiendo: /agendar
"""

    await update.message.reply_text(welcome_message)


async def help_command(update, context):
    """Handler para el comando /ayuda"""
    help_message = """
AYUDA - Asistente de Agendamiento de Reuniones

COMANDOS:
/start - Iniciar el bot
/agendar - Agendar una nueva reunión
/cancelar - Cancelar el proceso actual
/ayuda - Mostrar esta ayuda

CÓMO AGENDAR UNA REUNIÓN:
1. Escribe /agendar
2. El bot te pedirá la información de manera conversacional:
   - Fecha: Puedes decir "mañana", "15 de diciembre", "próximo lunes", etc.
   - Hora: Puedes decir "3 de la tarde", "14:30", "2 PM", "mediodía", etc.
   - Asunto: El título de tu reunión
   - Descripción: Los detalles de la reunión

3. El sistema autonómico:
   - Interpretará fechas y horas en lenguaje natural
   - Detectará el tipo de reunión
   - Configurará duración y recordatorios
   - Validará que los datos sean correctos
   - Sugerirá optimizaciones si es necesario

4. Confirmarás los datos
5. Se creará un archivo con la información de tu reunión

¡Habla de manera natural! El bot entiende diferentes formatos.
"""

    await update.message.reply_text(help_message)


async def agendar_command(update, context):
    """Handler para el comando /agendar"""
    user_id = update.effective_user.id

    # Inicializar estado para agendar reunion
    user_states[user_id] = {
        'state': 'collecting_info',
        'data': {}
    }

    # Limpiar contexto anterior si existe
    prompts.delete_context(user_id)

    message = """
¡Perfecto! Vamos a agendar tu reunión.

Dime todos los detalles que tengas sobre la reunión. Puedes incluir:
• Fecha (ej: "mañana", "el 15 de diciembre", "próximo lunes")
• Hora (ej: "a las 3 de la tarde", "14:30", "por la mañana")
• Asunto (el tema de la reunión)
• Descripción (detalles adicionales)

Habla de forma natural, yo entenderé. Por ejemplo:
"Quiero agendar una reunión mañana a las 3 pm sobre el proyecto de marketing para discutir la estrategia del Q4"

Iré capturando la información y te pediré lo que falte.

(Escribe /cancelar si deseas cancelar)
"""

    await update.message.reply_text(message)


async def cancelar_command(update, context):
    """Handler para el comando /cancelar"""
    user_id = update.effective_user.id

    if user_id in user_states:
        user_states[user_id] = {
            'state': 'idle',
            'data': {}
        }

    # Eliminar contexto si existe
    prompts.delete_context(user_id)

    await update.message.reply_text("❌ Proceso cancelado. Escribe /agendar para comenzar de nuevo.")


# ========================================================================
# FUNCIONES AUXILIARES
# ========================================================================

async def process_complete_meeting(update, user_id, context_data):
    """
    Procesa una reunión cuando toda la información está completa.

    Args:
        update: Update object de Telegram
        user_id: ID del usuario
        context_data: Diccionario con toda la información de la reunión
    """
    await update.message.reply_text("¡Perfecto! Déjame procesar toda la información...")

    # Preparar datos para el sistema autonómico
    data = {
        'fecha': context_data.get('fecha'),
        'hora': context_data.get('hora'),
        'asunto': context_data.get('asunto'),
        'descripcion': context_data.get('descripcion')
    }

    result = prompts.process_meeting_request(data)

    if result['status'] == 'error':
        error_msg = "❌ Hubo errores al procesar la reunión:\n"
        for error in result['errors']:
            error_msg += f"• {error}\n"
        error_msg += "\nPor favor, corrige la información y vuelve a intentar."

        await update.message.reply_text(error_msg)
        return

    if result['status'] == 'incompleto':
        await update.message.reply_text(
            f"⚠️ Datos incompletos:\n{result['repair_prompt']}"
        )
        return

    # Si llegamos aquí, todo está completo
    # Guardar resultado para confirmación
    user_states[user_id]['result'] = result
    user_states[user_id]['state'] = 'confirming'

    # Generar resumen
    summary = prompts.format_meeting_summary(
        result['data'],
        result['config'],
        result['optimization']
    )

    confirmation_msg = f"""
{summary}

¿Confirmas que deseas agendar esta reunión?
Responde 'si' para confirmar o 'no' para cancelar
"""

    await update.message.reply_text(confirmation_msg)


# ========================================================================
# HANDLER PRINCIPAL DE MENSAJES
# ========================================================================

async def handle_message(update, context):
    """Handler principal para mensajes de texto"""
    user_id = update.effective_user.id
    user_message = update.message.text.strip()

    print(f"Usuario {user_id}: {user_message}")

    # Inicializar estado si no existe
    if user_id not in user_states:
        user_states[user_id] = {
            'state': 'idle',
            'data': {}
        }

    state = user_states[user_id]['state']
    data = user_states[user_id]['data']

    # ====================================================================
    # ESTADO: IDLE (esperando comando)
    # ====================================================================
    if state == 'idle':
        response = """
No estoy seguro de que necesitas.

Escribe /agendar para agendar una reunion
Escribe /ayuda para ver todos los comandos disponibles
"""
        await update.message.reply_text(response)

    # ====================================================================
    # ESTADO: RECOLECTANDO INFORMACIÓN
    # ====================================================================
    elif state == 'collecting_info':
        await update.message.reply_text("📝 Procesando tu mensaje...")

        # Cargar contexto existente
        existing_context = prompts.load_context(user_id)

        # Inferir información del mensaje
        inferred_data = prompts.infer_meeting_info_from_message(user_message, existing_context)

        # Actualizar contexto
        updated_context = prompts.update_context(user_id, user_message, inferred_data)

        # Verificar si necesita aclaración
        if inferred_data.get('needs_clarification', True):
            # Aún falta información
            missing_fields = inferred_data.get('missing_fields', [])

            if not missing_fields:
                # Verificar completitud con el contexto actualizado (descripcion es opcional)
                complete = all(updated_context.get(field) for field in ['fecha', 'hora', 'asunto'])

                if complete:
                    # Toda la información está completa, procesar
                    await process_complete_meeting(update, user_id, updated_context)
                else:
                    await update.message.reply_text(inferred_data.get('clarification_message', 'Por favor proporciona más información.'))
            else:
                # Mostrar lo que se ha capturado y pedir lo que falta
                captured_info = "✅ He capturado:\n"
                for field in ['fecha', 'hora', 'asunto', 'descripcion']:
                    value = updated_context.get(field)
                    if value:
                        field_name = {'fecha': 'Fecha', 'hora': 'Hora', 'asunto': 'Asunto', 'descripcion': 'Descripción'}
                        captured_info += f"• {field_name[field]}: {value}\n"

                response = f"{captured_info}\n{inferred_data.get('clarification_message', 'Por favor proporciona la información faltante.')}"
                await update.message.reply_text(response)
        else:
            # Toda la información está completa
            await process_complete_meeting(update, user_id, updated_context)

    # ====================================================================
    # ESTADO: CONFIRMANDO
    # ====================================================================
    elif state == 'confirming':
        response = user_message.lower()

        if response in ['si', 'sí', 's', 'yes', 'confirmar']:
            # CONFIRMAR Y GUARDAR REUNION
            result = user_states[user_id]['result']

            try:
                # Guardar en archivo
                filepath = prompts.save_meeting_to_file(
                    result['data'],
                    result['config'],
                    result['optimization']
                )

                success_msg = f"""
✅ REUNIÓN AGENDADA EXITOSAMENTE

Los detalles de la reunión han sido guardados en:
{filepath}

El sistema autonómico ha:
• Protegido y validado tus datos
• Detectado el tipo de reunión: {result['config']['tipo']}
• Configurado duración: {result['config']['duracion_minutos']} minutos
• Evaluado el horario: {result['optimization']['status']}

Escribe /agendar para agendar otra reunión
"""

                await update.message.reply_text(success_msg)

                # Programar eliminación del contexto después de 5 segundos
                async def delete_context_after_delay():
                    await asyncio.sleep(5)
                    prompts.delete_context(user_id)
                    print(f"Contexto del usuario {user_id} eliminado después de 5 segundos")

                # Ejecutar eliminación en segundo plano
                asyncio.create_task(delete_context_after_delay())

                # Resetear estado
                user_states[user_id] = {
                    'state': 'idle',
                    'data': {}
                }

            except Exception as e:
                await update.message.reply_text(
                    f"❌ Error al guardar la reunión: {str(e)}\n"
                    "Por favor intenta de nuevo."
                )
                user_states[user_id]['state'] = 'idle'

        elif response in ['no', 'n', 'cancelar']:
            await update.message.reply_text(
                "❌ Reunión cancelada.\n"
                "Escribe /agendar para comenzar de nuevo."
            )

            # Eliminar contexto también cuando se cancela
            prompts.delete_context(user_id)

            user_states[user_id] = {
                'state': 'idle',
                'data': {}
            }

        else:
            await update.message.reply_text(
                "Por favor responde 'si' para confirmar o 'no' para cancelar."
            )


# ========================================================================
# INICIALIZACION DEL BOT
# ========================================================================

def run_bot():
    """Ejecuta el bot de Telegram en un hilo separado"""
    # Crear y establecer un nuevo loop para este hilo
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Crear aplicacion del bot
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    # Registrar handlers de comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ayuda", help_command))
    application.add_handler(CommandHandler("agendar", agendar_command))
    application.add_handler(CommandHandler("cancelar", cancelar_command))

    # Registrar handler de mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("BOT: Ejecutando polling...")

    # Ejecutar el bot
    application.run_polling()


# ========================================================================
# SERVIDOR FLASK
# ========================================================================

@app.route("/")
def index():
    return "Flask server running - Bot de agendamiento de reuniones activo"


@app.route("/status")
def status():
    """Endpoint para verificar el estado del bot"""
    return {
        "status": "online",
        "active_users": len(user_states),
        "bot_name": "Asistente de Agendamiento de Reuniones"
    }


# ========================================================================
# MAIN
# ========================================================================

if __name__ == "__main__":
    print("Iniciando Asistente de Agendamiento de Reuniones con Computacion Autonomica")
    print("="*70)

    # Flask bloquea el hilo principal, asi que el bot va al hilo secundario
    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    print("FLASK: Iniciando servidor Flask...")
    # Flask debe ir al final ya que app.run() bloquea
    # use_reloader=False evita que se creen multiples instancias del bot
    app.run(host="0.0.0.0", port=5000, use_reloader=False)
