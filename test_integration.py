import sys
import os

# Aseguramos que Python vea la carpeta actual como un paquete
sys.path.append(os.getcwd())

try:
    print("1. Importando herramientas...")
    from tools.calendar_tools import conectar_google, tool_listar_eventos
    print("✅ Importación exitosa.")

    print("2. Probando conexión a Google...")
    service = conectar_google()
    print("✅ Conexión establecida.")

    print("3. Consultando eventos...")
    respuesta = tool_listar_eventos(service)
    print(f"📅 Respuesta del calendario:\n{respuesta}")

except Exception as e:
    print(f"❌ Error: {e}")