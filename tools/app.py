from flask import Flask, jsonify
from auth import conectar_servicios
from correo_tools import tool_enviar_correo

app = Flask(__name__)

# 1. Inicialización Global (Al arrancar la app)
# Esto abrirá el navegador la primera vez si no existe token.json
print("Autenticando servicios de Google...")
service_calendar, service_gmail = conectar_servicios()

@app.route('/')
def home():
    return "Bot de Telegram activo"

# ESTA SERÍA LA LÓGICA QUE USARÍA TU AGENTE LANGCHAIN
# Simulación de uso manual para probar tu módulo:
@app.route('/test-email')
def test_email():
    # Supongamos que el Agente decidió enviar un correo
    resultado = tool_enviar_correo(
        service_gmail, 
        destinatario="giacomo.madrid@unmsm.edu.pe", # Pon tu correo aquí para probar
        asunto="Prueba desde el Bot de Telegram",
        cuerpo="Hola, este es un mensaje enviado automáticamente por el asistente virtual. \nPD: Miau :3"
    )
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(debug=True, port=5000)