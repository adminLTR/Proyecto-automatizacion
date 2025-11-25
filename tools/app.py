from flask import Flask, jsonify
from auth import conectar_servicios
from correo_tools import tool_enviar_correo

app = Flask(__name__)

# Abrir el navegador la primera vez si no existe token.json
print("Autenticando servicios de Google...")
service_calendar, service_gmail = conectar_servicios()

@app.route('/')
def home():
    return "Bot de Telegram activo"

@app.route('/test-email')
def test_email():    
    resultado = tool_enviar_correo(
        service_gmail, 
        # Correo de prueba (CAMBIAR POR EL DESTINO, SOLO PARA PRUEBAS)
        destinatario="email@example.com", 
        asunto="Prueba desde el Bot de Telegram",
        cuerpo="Hola, este es un mensaje enviado automáticamente por el asistente virtual."
    )
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(debug=True, port=5000)