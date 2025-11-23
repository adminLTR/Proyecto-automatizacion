from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post("/consulta")
async def recibir_consulta(json_in: dict):
    """
    Recibe JSON desde bot.py y este archivo simula
    como otro servicio (Google Calendar) devolverá su respuesta
    """

    tipo = json_in.get("consulta")

    if tipo == "horario_hoy":
        return {
            "tipo": "respuesta_horario",
            "dia": "2025-11-22",
            "actividades": [
                {"hora": "09:00", "texto": "Revisión diaria"},
                {"hora": "11:00", "texto": "Reunión scrum"},
                {"hora": "15:00", "texto": "Planificación semanal"}
            ]
        }

    if tipo == "sugerencias":
        return {
            "tipo": "respuesta_sugerencias",
            "sugerencias": [
                "Toma agua cada 2 horas",
                "Haz pausas activas cada hora"
            ]
        }

    return {
        "tipo": "error",
        "detalle": "Consulta no implementada aún"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
