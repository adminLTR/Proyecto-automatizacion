"""
Sistema de Agendamiento de Reuniones con Computacion Autonomica
Implementa los 4 principios: Auto-configuracion, Auto-optimizacion,
Auto-curacion y Auto-proteccion
"""

import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ========================================================================
# PRINCIPIO 1: AUTO-CONFIGURACION
# ========================================================================

def detect_meeting_type(asunto: str, descripcion: str) -> str:
    """
    AUTO-CONFIGURACION: Detecta el tipo de reunion basandose en palabras clave.

    Tipos posibles:
    - estrategica: Reuniones de planificacion y objetivos
    - seguimiento: Status updates y avances
    - informal: Cafes y charlas casuales
    - presentacion: Demos y presentaciones
    - brainstorming: Sesiones creativas
    """
    text = f"{asunto} {descripcion}".lower()

    keywords = {
        'estrategica': ['estrategia', 'planificacion', 'objetivos', 'vision', 'direccion'],
        'seguimiento': ['seguimiento', 'status', 'avance', 'progreso', 'actualizacion'],
        'informal': ['cafe', 'charla', 'conversacion', 'informal', 'casual'],
        'presentacion': ['presentacion', 'demo', 'demostracion', 'pitch', 'exposicion'],
        'brainstorming': ['brainstorm', 'ideas', 'creativo', 'innovacion', 'lluvia']
    }

    scores = {meeting_type: 0 for meeting_type in keywords.keys()}

    for meeting_type, kws in keywords.items():
        for keyword in kws:
            if keyword in text:
                scores[meeting_type] += 1

    detected_type = max(scores, key=scores.get)
    if scores[detected_type] == 0:
        detected_type = 'seguimiento'

    return detected_type


def auto_configure_meeting(asunto: str, descripcion: str) -> Dict:
    """
    AUTO-CONFIGURACION: Configura automaticamente los parametros de la reunion.

    Retorna un diccionario con:
    - tipo: Tipo de reunion detectado
    - duracion_minutos: Duracion recomendada
    - prioridad: alta, media o baja
    - recordatorios: Lista de minutos antes para recordar
    - formato: formal, semi-formal, casual o creativo
    """
    meeting_type = detect_meeting_type(asunto, descripcion)

    configs = {
        'estrategica': {
            'duracion_minutos': 90,
            'recordatorios': [1440, 60, 15],
            'prioridad': 'alta',
            'formato': 'formal'
        },
        'seguimiento': {
            'duracion_minutos': 30,
            'recordatorios': [60, 15],
            'prioridad': 'media',
            'formato': 'semi-formal'
        },
        'informal': {
            'duracion_minutos': 20,
            'recordatorios': [15],
            'prioridad': 'baja',
            'formato': 'casual'
        },
        'presentacion': {
            'duracion_minutos': 60,
            'recordatorios': [1440, 120, 30],
            'prioridad': 'alta',
            'formato': 'formal'
        },
        'brainstorming': {
            'duracion_minutos': 45,
            'recordatorios': [60, 15],
            'prioridad': 'media',
            'formato': 'creativo'
        }
    }

    config = configs.get(meeting_type, configs['seguimiento'])
    config['tipo'] = meeting_type

    return config


# ========================================================================
# PRINCIPIO 2: AUTO-OPTIMIZACION
# ========================================================================

def validate_time_format(hora: str) -> bool:
    """Valida que la hora este en formato HH:MM"""
    try:
        datetime.strptime(hora, '%H:%M')
        return True
    except:
        return False


def validate_date_format(fecha: str) -> bool:
    """Valida que la fecha este en formato YYYY-MM-DD"""
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except:
        return False


def interpret_date_with_gpt(user_input: str) -> Dict:
    """
    Usa GPT para interpretar una fecha en lenguaje natural.

    Retorna un diccionario con:
    - success: bool - si se pudo interpretar la fecha
    - date: str - fecha en formato YYYY-MM-DD (si success=True)
    - message: str - mensaje para el usuario (si success=False)
    - needs_clarification: bool - si necesita más información del usuario
    """
    today = datetime.now()

    prompt = f"""Hoy es {today.strftime('%Y-%m-%d')} ({today.strftime('%A, %d de %B de %Y')}).

El usuario quiere agendar una reunión y ha proporcionado esta información sobre la fecha:
"{user_input}"

Tu tarea es interpretar esta fecha y responder en formato JSON con la siguiente estructura:
{{
    "success": true/false,
    "date": "YYYY-MM-DD" (solo si success=true),
    "message": "mensaje amable para el usuario si necesitas aclaración",
    "needs_clarification": true/false
}}

Reglas:
1. Si puedes interpretar la fecha claramente (ej: "15 de diciembre", "mañana", "próximo lunes"), establece success=true y proporciona la fecha en formato YYYY-MM-DD
2. Si el año no está especificado, asume el año actual ({today.year}) o el siguiente si ya pasó la fecha este año
3. Si la información es ambigua (ej: "la próxima semana" sin día específico), establece needs_clarification=true y proporciona un mensaje amable pidiendo más detalles
4. Si no puedes interpretar la fecha, establece success=false y proporciona un mensaje amable pidiendo que reformule
5. El mensaje debe ser cálido y natural, sin mencionar formatos técnicos como YYYY-MM-DD

Responde ÚNICAMENTE con el JSON, sin texto adicional."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente amable que interpreta fechas en lenguaje natural. Siempre respondes en formato JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        return {
            "success": False,
            "message": "Disculpa, tuve un problema al interpretar la fecha. ¿Podrías decirme de nuevo qué día quieres la reunión?",
            "needs_clarification": True
        }


def interpret_time_with_gpt(user_input: str) -> Dict:
    """
    Usa GPT para interpretar una hora en lenguaje natural.

    Retorna un diccionario con:
    - success: bool - si se pudo interpretar la hora
    - time: str - hora en formato HH:MM (si success=True)
    - message: str - mensaje para el usuario (si success=False)
    - needs_clarification: bool - si necesita más información del usuario
    """

    prompt = f"""El usuario quiere agendar una reunión y ha proporcionado esta información sobre la hora:
"{user_input}"

Tu tarea es interpretar esta hora y responder en formato JSON con la siguiente estructura:
{{
    "success": true/false,
    "time": "HH:MM" (solo si success=true, formato 24 horas),
    "message": "mensaje amable para el usuario si necesitas aclaración",
    "needs_clarification": true/false
}}

Reglas:
1. Si puedes interpretar la hora claramente (ej: "3 de la tarde", "14:30", "2 pm", "mediodía"), establece success=true y proporciona la hora en formato HH:MM (24 horas)
2. Si la información es ambigua (ej: "por la tarde" sin hora específica), establece needs_clarification=true y proporciona un mensaje amable pidiendo más detalles
3. Si no puedes interpretar la hora, establece success=false y proporciona un mensaje amable pidiendo que reformule
4. El mensaje debe ser cálido y natural, sin mencionar formatos técnicos como HH:MM
5. Convierte formatos de 12 horas (AM/PM) a 24 horas

Responde ÚNICAMENTE con el JSON, sin texto adicional."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente amable que interpreta horas en lenguaje natural. Siempre respondes en formato JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        return {
            "success": False,
            "message": "Disculpa, tuve un problema al interpretar la hora. ¿Podrías decirme de nuevo a qué hora quieres la reunión?",
            "needs_clarification": True
        }


def infer_meeting_info_from_message(user_message: str, existing_context: Dict = None) -> Dict:
    """
    Usa GPT para inferir toda la información posible de una reunión a partir de un mensaje.

    Args:
        user_message: Mensaje del usuario
        existing_context: Contexto existente con información ya capturada

    Returns:
        Dict con:
        - fecha: str (YYYY-MM-DD) o None
        - hora: str (HH:MM) o None
        - asunto: str o None
        - descripcion: str o None
        - missing_fields: List[str] - campos que faltan
        - needs_clarification: bool
        - clarification_message: str - mensaje para pedir lo que falta
    """
    today = datetime.now()

    # Preparar contexto existente
    context_str = ""
    if existing_context:
        context_str = f"""
Información ya capturada:
- Fecha: {existing_context.get('fecha', 'No especificada')}
- Hora: {existing_context.get('hora', 'No especificada')}
- Asunto: {existing_context.get('asunto', 'No especificado')}
- Descripción: {existing_context.get('descripcion', 'No especificada')}
"""

    prompt = f"""Hoy es {today.strftime('%Y-%m-%d')} ({today.strftime('%A, %d de %B de %Y')}).

{context_str}

El usuario quiere agendar una reunión y ha escrito:
"{user_message}"

Tu tarea es extraer TODA la información posible sobre la reunión. Responde en formato JSON:
{{
    "fecha": "YYYY-MM-DD o null si no está clara",
    "hora": "HH:MM (24h) o null si no está clara",
    "asunto": "texto o null si no está claro",
    "descripcion": "texto o null si no está clara o si el usuario no quiere proporcionar",
    "missing_fields": ["lista", "de", "campos", "faltantes"],
    "needs_clarification": true/false,
    "clarification_message": "mensaje amable pidiendo lo que falta"
}}

REGLAS IMPORTANTES:
1. Si el usuario menciona fecha/hora, extráelas aunque sea de forma natural ("mañana a las 3", "el lunes por la tarde")
2. Si mencionan el propósito/tema, úsalo como asunto
3. Cualquier detalle adicional va en descripción
4. LA DESCRIPCIÓN ES OPCIONAL: missing_fields debe incluir SOLO: "fecha", "hora", "asunto" (NO incluir "descripcion")
5. Si el usuario indica que no quiere dar más detalles, descripción, o dice "nada más", "sin descripción", etc., deja descripcion en null y NO pidas más información
6. Si ya existe información en el contexto, NO la sobrescribas con null - mantenla
7. El clarification_message debe ser conversacional y pedir SOLO lo que falta (fecha, hora o asunto). NUNCA pidas descripción
8. VALIDACIONES:
   - Fecha no puede ser más de 1 año en el futuro
   - Fecha no puede estar en el pasado
   - Hora debe estar entre 06:00 y 22:00
   - Si algo viola estas reglas, marca ese campo como null y explica en clarification_message

Responde ÚNICAMENTE con el JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente que extrae información de reuniones de mensajes en lenguaje natural. Siempre respondes en formato JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        # Combinar con contexto existente (mantener lo que ya existe)
        if existing_context:
            for field in ['fecha', 'hora', 'asunto', 'descripcion']:
                if existing_context.get(field) and not result.get(field):
                    result[field] = existing_context[field]

        return result

    except Exception as e:
        return {
            "fecha": None,
            "hora": None,
            "asunto": None,
            "descripcion": None,
            "missing_fields": ["fecha", "hora", "asunto"],
            "needs_clarification": True,
            "clarification_message": "Disculpa, tuve un problema. ¿Podrías decirme de nuevo los detalles de la reunión?"
        }


def calculate_end_time(hora_inicio: str, duracion_minutos: int) -> str:
    """Calcula la hora de fin basandose en inicio y duracion"""
    try:
        inicio = datetime.strptime(hora_inicio, '%H:%M')
        fin = inicio + timedelta(minutes=duracion_minutos)
        return fin.strftime('%H:%M')
    except:
        return "N/A"


def optimize_meeting_time(fecha: str, hora: str, duracion: int) -> Dict:
    """
    AUTO-OPTIMIZACION: Evalua si el horario propuesto es optimo.

    Retorna:
    - status: 'optimo', 'aceptable' o 'suboptimo'
    - score: Puntuacion del horario
    - recomendaciones: Lista de sugerencias
    """
    if not validate_time_format(hora) or not validate_date_format(fecha):
        return {
            'status': 'error',
            'score': -1,
            'recomendaciones': ['Formato de fecha u hora invalido']
        }

    hora_int = int(hora.split(':')[0])
    fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')

    score = 0
    recomendaciones = []

    # Verificar si es fin de semana
    if fecha_dt.weekday() >= 5:
        score += 20
        recomendaciones.append('Considera agendar en dia laboral')

    # Verificar horario laboral
    if hora_int < 8 or hora_int > 18:
        score += 30
        recomendaciones.append('Horario fuera del rango laboral recomendado (8:00-18:00)')
    elif 9 <= hora_int <= 11 or 15 <= hora_int <= 16:
        score -= 20
        recomendaciones.append('Excelente horario - alta productividad')

    # Verificar hora de almuerzo
    if 12 <= hora_int <= 13:
        score += 15
        recomendaciones.append('Evita agendar durante hora de almuerzo')

    # Verificar si la fecha ya paso
    if fecha_dt.date() < datetime.now().date():
        score += 100
        recomendaciones.append('ERROR: La fecha esta en el pasado')

    # Determinar status
    if score < 0:
        status = 'optimo'
    elif score < 20:
        status = 'aceptable'
    else:
        status = 'suboptimo'

    return {
        'status': status,
        'score': score,
        'recomendaciones': recomendaciones
    }


# ========================================================================
# PRINCIPIO 3: AUTO-CURACION
# ========================================================================

def detect_missing_fields(data: Dict) -> List[str]:
    """
    AUTO-CURACION - DETECCION: Detecta que campos faltan en los datos.
    Nota: 'descripcion' es opcional
    """
    required_fields = ['fecha', 'hora', 'asunto']  # descripcion es opcional
    missing = []

    for field in required_fields:
        if field not in data or not data[field] or data[field].strip() == '':
            missing.append(field)

    return missing


def diagnose_data(data: Dict) -> Dict:
    """
    AUTO-CURACION - DIAGNOSTICO: Analiza los datos y genera un diagnostico.

    Retorna:
    - missing_fields: Lista de campos faltantes
    - present_fields: Campos que ya estan presentes
    - severity: 'none', 'baja', 'media', 'alta'
    """
    missing = detect_missing_fields(data)
    present = {k: v for k, v in data.items() if k not in missing}

    if len(missing) == 0:
        severity = 'none'
    elif len(missing) <= 1:
        severity = 'baja'
    elif len(missing) <= 2:
        severity = 'media'
    else:
        severity = 'alta'

    return {
        'missing_fields': missing,
        'present_fields': present,
        'severity': severity
    }


def generate_repair_prompt(missing_fields: List[str]) -> str:
    """
    AUTO-CURACION - REPARACION: Genera un mensaje para solicitar campos faltantes.
    """
    if not missing_fields:
        return "Todos los datos estan completos."

    field_prompts = {
        'fecha': 'Por favor proporciona la FECHA (formato: YYYY-MM-DD, ejemplo: 2025-12-05)',
        'hora': 'Por favor proporciona la HORA (formato: HH:MM, ejemplo: 14:30)',
        'asunto': 'Por favor proporciona el ASUNTO de la reunion'
    }

    prompt = "Faltan los siguientes datos:\n\n"
    for field in missing_fields:
        prompt += f"- {field_prompts.get(field, field)}\n"

    return prompt


def verify_data_completeness(data: Dict) -> bool:
    """
    AUTO-CURACION - VERIFICACION: Verifica que todos los datos esten completos.
    """
    missing = detect_missing_fields(data)
    return len(missing) == 0


# ========================================================================
# PRINCIPIO 4: AUTO-PROTECCION
# ========================================================================

def sanitize_input(text: str) -> str:
    """
    AUTO-PROTECCION: Sanitiza entradas del usuario para prevenir inyecciones.
    """
    if not isinstance(text, str):
        return str(text)

    # Remover caracteres de control
    sanitized = text.replace('\x00', '')

    # Escapar caracteres HTML
    html_escape = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
    }

    for char, escaped in html_escape.items():
        sanitized = sanitized.replace(char, escaped)

    return sanitized


def detect_malicious_patterns(text: str) -> Tuple[bool, List[str]]:
    """
    AUTO-PROTECCION: Detecta patrones maliciosos en las entradas.

    Retorna (es_malicioso, lista_patrones_detectados)
    """
    malicious_patterns = [
        r'<script[^>]*>',
        r'javascript:',
        r'DROP\s+TABLE',
        r'--',
        r'UNION\s+SELECT',
        r'eval\s*\(',
        r'exec\s*\(',
        r'__import__',
    ]

    detected = []
    for pattern in malicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            detected.append(pattern)

    return len(detected) > 0, detected


def validate_meeting_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    AUTO-PROTECCION: Valida que los datos de reunion sean validos y seguros.

    Retorna (es_valido, lista_errores)
    """
    errors = []

    # Validar fecha
    if 'fecha' in data and data['fecha']:
        if not validate_date_format(data['fecha']):
            errors.append('Formato de fecha invalido (debe ser YYYY-MM-DD)')
        else:
            try:
                fecha_dt = datetime.strptime(data['fecha'], '%Y-%m-%d')
                if fecha_dt.date() < datetime.now().date():
                    errors.append('La fecha no puede estar en el pasado')
                if fecha_dt.date() > (datetime.now() + timedelta(days=365)).date():
                    errors.append('La fecha no puede estar mas de 1 ano en el futuro')
            except:
                errors.append('Fecha invalida')

    # Validar hora
    if 'hora' in data and data['hora']:
        if not validate_time_format(data['hora']):
            errors.append('Formato de hora invalido (debe ser HH:MM)')
        else:
            try:
                hora_dt = datetime.strptime(data['hora'], '%H:%M')
                if hora_dt.hour < 6 or hora_dt.hour > 22:
                    errors.append('Hora fuera del rango razonable (06:00 - 22:00)')
            except:
                errors.append('Hora invalida')

    # Validar asunto
    if 'asunto' in data and data['asunto']:
        if len(data['asunto']) > 200:
            errors.append('Asunto demasiado largo (maximo 200 caracteres)')
        if len(data['asunto']) < 3:
            errors.append('Asunto demasiado corto (minimo 3 caracteres)')

        # Detectar patrones maliciosos
        is_malicious, patterns = detect_malicious_patterns(data['asunto'])
        if is_malicious:
            errors.append('Patron malicioso detectado en asunto')

    # Validar descripcion (opcional)
    if 'descripcion' in data and data['descripcion']:
        if len(data['descripcion']) > 1000:
            errors.append('Descripcion demasiado larga (maximo 1000 caracteres)')

        # Detectar patrones maliciosos
        is_malicious, patterns = detect_malicious_patterns(data['descripcion'])
        if is_malicious:
            errors.append('Patron malicioso detectado en descripcion')

    return len(errors) == 0, errors


def protect_data(data: Dict) -> Dict:
    """
    AUTO-PROTECCION: Sanitiza y valida todos los datos.

    Retorna datos sanitizados o lanza excepcion si hay problemas.
    """
    sanitized = {}

    # Sanitizar todos los campos de texto
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        else:
            sanitized[key] = value

    # Validar datos
    is_valid, errors = validate_meeting_data(sanitized)
    if not is_valid:
        raise ValueError(f"Datos invalidos: {', '.join(errors)}")

    return sanitized


# ========================================================================
# MANEJO DE CONTEXTO (context.txt)
# ========================================================================

def get_context_filepath(user_id: int) -> str:
    """Retorna la ruta del archivo de contexto para un usuario específico"""
    context_dir = os.path.join(os.path.dirname(__file__), 'contextos')
    os.makedirs(context_dir, exist_ok=True)
    return os.path.join(context_dir, f'context_{user_id}.txt')


def save_context(user_id: int, context_data: Dict) -> None:
    """
    Guarda el contexto de la conversación en un archivo.

    Args:
        user_id: ID del usuario
        context_data: Diccionario con la información capturada
    """
    filepath = get_context_filepath(user_id)

    content = f"""CONTEXTO DE AGENDAMIENTO DE REUNIÓN
Usuario ID: {user_id}
Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INFORMACIÓN CAPTURADA:
"""

    for field in ['fecha', 'hora', 'asunto', 'descripcion']:
        value = context_data.get(field, 'No especificado')
        if value is None or value == '':
            value = 'No especificado'
        content += f"{field.capitalize()}: {value}\n"

    content += f"""
HISTORIAL DE MENSAJES:
{context_data.get('message_history', '')}
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def load_context(user_id: int) -> Dict:
    """
    Carga el contexto desde el archivo.

    Args:
        user_id: ID del usuario

    Returns:
        Dict con la información del contexto o un dict vacío si no existe
    """
    filepath = get_context_filepath(user_id)

    if not os.path.exists(filepath):
        return {
            'fecha': None,
            'hora': None,
            'asunto': None,
            'descripcion': None,
            'message_history': ''
        }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parsear el contenido
        context = {
            'fecha': None,
            'hora': None,
            'asunto': None,
            'descripcion': None,
            'message_history': ''
        }

        # Extraer información
        for field in ['fecha', 'hora', 'asunto', 'descripcion']:
            pattern = f"{field.capitalize()}: (.+)"
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if value != 'No especificado' and value != 'None':
                    context[field] = value

        # Extraer historial de mensajes
        history_match = re.search(r'HISTORIAL DE MENSAJES:\n(.+)', content, re.DOTALL)
        if history_match:
            context['message_history'] = history_match.group(1).strip()

        return context

    except Exception as e:
        print(f"Error al cargar contexto: {e}")
        return {
            'fecha': None,
            'hora': None,
            'asunto': None,
            'descripcion': None,
            'message_history': ''
        }


def update_context(user_id: int, new_message: str, new_data: Dict) -> Dict:
    """
    Actualiza el contexto con nueva información.

    Args:
        user_id: ID del usuario
        new_message: Nuevo mensaje del usuario
        new_data: Nuevos datos extraídos

    Returns:
        Dict con el contexto actualizado
    """
    context = load_context(user_id)

    # Actualizar campos que tengan valor
    for field in ['fecha', 'hora', 'asunto', 'descripcion']:
        if new_data.get(field) and new_data[field] != 'None':
            context[field] = new_data[field]

    # Agregar mensaje al historial
    timestamp = datetime.now().strftime('%H:%M:%S')
    context['message_history'] += f"[{timestamp}] Usuario: {new_message}\n"

    # Guardar contexto actualizado
    save_context(user_id, context)

    return context


def delete_context(user_id: int) -> None:
    """
    Elimina el archivo de contexto de un usuario.

    Args:
        user_id: ID del usuario
    """
    filepath = get_context_filepath(user_id)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            print(f"Contexto eliminado: {filepath}")
        except Exception as e:
            print(f"Error al eliminar contexto: {e}")


# ========================================================================
# SISTEMA INTEGRADO
# ========================================================================

def process_meeting_request(data: Dict) -> Dict:
    """
    Sistema autonomico integrado que procesa una solicitud de reunion.

    Aplica los 4 principios en orden:
    1. AUTO-PROTECCION: Valida y sanitiza
    2. AUTO-CURACION: Detecta datos faltantes
    3. AUTO-CONFIGURACION: Configura parametros automaticos
    4. AUTO-OPTIMIZACION: Evalua el horario

    Retorna un diccionario con:
    - status: 'completo', 'incompleto', 'error'
    - data: Datos procesados
    - config: Configuracion automatica
    - optimization: Resultado de optimizacion
    - missing_fields: Campos faltantes (si hay)
    - repair_prompt: Mensaje para reparar (si hay)
    - errors: Lista de errores (si hay)
    """
    result = {
        'status': 'error',
        'data': {},
        'config': {},
        'optimization': {},
        'missing_fields': [],
        'repair_prompt': '',
        'errors': []
    }

    try:
        # PASO 1: AUTO-PROTECCION
        try:
            protected_data = protect_data(data)
        except ValueError as e:
            result['errors'].append(str(e))
            return result

        # PASO 2: AUTO-CURACION - Diagnostico
        diagnosis = diagnose_data(protected_data)

        if diagnosis['missing_fields']:
            result['status'] = 'incompleto'
            result['missing_fields'] = diagnosis['missing_fields']
            result['repair_prompt'] = generate_repair_prompt(diagnosis['missing_fields'])
            result['data'] = protected_data
            return result

        # PASO 3: AUTO-CONFIGURACION
        # La descripción es opcional, usar cadena vacía si no existe
        config = auto_configure_meeting(
            protected_data.get('asunto', ''),
            protected_data.get('descripcion', '') if protected_data.get('descripcion') else ''
        )

        # Calcular hora de fin
        hora_fin = calculate_end_time(
            protected_data['hora'],
            config['duracion_minutos']
        )
        config['hora_fin'] = hora_fin

        # PASO 4: AUTO-OPTIMIZACION
        optimization = optimize_meeting_time(
            protected_data['fecha'],
            protected_data['hora'],
            config['duracion_minutos']
        )

        # Todo exitoso
        result['status'] = 'completo'
        result['data'] = protected_data
        result['config'] = config
        result['optimization'] = optimization

    except Exception as e:
        result['errors'].append(f"Error inesperado: {str(e)}")

    return result


def save_meeting_to_file(meeting_data: Dict, config: Dict, optimization: Dict, filename: Optional[str] = None) -> str:
    """
    Guarda los datos de la reunion en un archivo de texto.

    Retorna la ruta del archivo creado.
    """
    if filename is None:
        # Generar nombre de archivo basado en fecha y hora
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        asunto_clean = re.sub(r'[^\w\s-]', '', meeting_data.get('asunto', 'reunion'))
        asunto_clean = re.sub(r'[-\s]+', '_', asunto_clean)[:30]
        filename = f"reunion_{asunto_clean}_{timestamp}.txt"

    # Crear directorio de reuniones si no existe
    meetings_dir = os.path.join(os.path.dirname(__file__), 'reuniones')
    os.makedirs(meetings_dir, exist_ok=True)

    filepath = os.path.join(meetings_dir, filename)

    # Generar contenido del archivo
    # Manejar descripción opcional
    descripcion = meeting_data.get('descripcion', '')
    if not descripcion or descripcion.strip() == '':
        descripcion = 'Sin descripción adicional'

    content = f"""
{'='*70}
REUNION AGENDADA
{'='*70}

DATOS DE LA REUNION:
  Fecha:        {meeting_data.get('fecha', 'N/A')}
  Hora inicio:  {meeting_data.get('hora', 'N/A')}
  Hora fin:     {config.get('hora_fin', 'N/A')}
  Duracion:     {config.get('duracion_minutos', 'N/A')} minutos

  Asunto:       {meeting_data.get('asunto', 'N/A')}
  Descripcion:  {descripcion}

CONFIGURACION AUTOMATICA:
  Tipo:         {config.get('tipo', 'N/A')}
  Prioridad:    {config.get('prioridad', 'N/A')}
  Formato:      {config.get('formato', 'N/A')}
  Recordatorios: {', '.join(map(str, config.get('recordatorios', [])))} minutos antes

OPTIMIZACION:
  Status:       {optimization.get('status', 'N/A')}
  Score:        {optimization.get('score', 'N/A')}
  Recomendaciones:
"""

    for rec in optimization.get('recomendaciones', []):
        content += f"    - {rec}\n"

    content += f"""
{'='*70}
Archivo generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""

    # Guardar archivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def format_meeting_summary(meeting_data: Dict, config: Dict, optimization: Dict) -> str:
    """
    Formatea un resumen de la reunion para mostrar al usuario.
    """
    # Manejar descripción opcional
    descripcion = meeting_data.get('descripcion', '')
    if not descripcion or descripcion.strip() == '':
        descripcion = 'Sin descripción adicional'

    summary = f"""
RESUMEN DE LA REUNION

Fecha: {meeting_data.get('fecha', 'N/A')}
Hora: {meeting_data.get('hora', 'N/A')} - {config.get('hora_fin', 'N/A')}
Duracion: {config.get('duracion_minutos', 'N/A')} minutos

Asunto: {meeting_data.get('asunto', 'N/A')}
Descripcion: {descripcion}

Tipo: {config.get('tipo', 'N/A').capitalize()}
Prioridad: {config.get('prioridad', 'N/A').upper()}
Formato: {config.get('formato', 'N/A').capitalize()}

Estado del horario: {optimization.get('status', 'N/A').upper()}
"""

    if optimization.get('recomendaciones'):
        summary += "\nRecomendaciones:\n"
        for rec in optimization['recomendaciones']:
            summary += f"  - {rec}\n"

    return summary
