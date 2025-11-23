from fastapi import FastAPI
import uvicorn

app = FastAPI()


# ------------------------------------------
#  BASE DE DATOS FICTICIA (MEMORIA)
# ------------------------------------------

BD_HORARIOS = {
    "2025-11-22": [
        {"hora": "09:00", "texto": "Revisión diaria del equipo"},
        {"hora": "11:00", "texto": "Reunión scrum"},
        {"hora": "15:00", "texto": "Planificación semanal"}
    ],
    "2025-11-23": [
        {"hora": "10:00", "texto": "Revisión de incidencias"},
        {"hora": "12:30", "texto": "Reunión con cliente"},
        {"hora": "16:00", "texto": "Reporte de avances"}
    ]
}

BD_SEMANA = {
    "resumen": """
Lunes: Revisión diaria
Martes: Capacitaciones internas
Miércoles: Gestión de incidencias
Jueves: Implementaciones del sprint
Viernes: Retro semanal
"""
}


BD_SUGERENCIAS = [
    "Toma agua cada 2 horas",
    "Haz pausas activas cada 60 minutos",
    "Divide tareas grandes en subtareas pequeñas",
    "Prioriza tareas con la técnica Pomodoro"
]


# ------------------------------------------
#  ENDPOINT PRINCIPAL
# ------------------------------------------

@app.post("/consulta")
async def consulta(json_in: dict):

    tipo = json_in.get("consulta")

    # ---- 1) Horario de hoy ----
    if tipo == "horario_hoy":
        dia = "2025-11-22"
        return {
            "tipo": "respuesta_horario",
            "dia": dia,
            "actividades": BD_HORARIOS.get(dia, [])
        }

    # ---- 2) Horario de mañana ----
    if tipo == "horario_manana":
        dia = "2025-11-23"
        return {
            "tipo": "respuesta_horario",
            "dia": dia,
            "actividades": BD_HORARIOS.get(dia, [])
        }

    # ---- 3) Resumen de semana ----
    if tipo == "semana":
        return {
            "tipo": "respuesta_semana",
            "resumen": BD_SEMANA["resumen"]
        }

    # ---- 4) Sugerencias IA ----
    if tipo == "sugerencias":
        return {
            "tipo": "respuesta_sugerencias",
            "sugerencias": BD_SUGERENCIAS
        }

    return {"tipo": "error", "detalle": "Consulta no soportada"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
