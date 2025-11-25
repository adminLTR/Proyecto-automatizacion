# Notas de Desarrollo

## 🔧 Configuración del Entorno de Desarrollo

### Python Virtual Environment
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Variables de Entorno
Para desarrollo, usa `.env.development`:
```bash
cp .env.development .env
```

## 🧪 Testing (Preparado para implementar)

### Estructura Propuesta
```
tests/
├── unit/
│   ├── test_email_controller.py
│   ├── test_calendar_controller.py
│   └── test_services.py
├── integration/
│   └── test_webhook_flow.py
└── conftest.py
```

### Ejecutar Tests
```bash
# Instalar pytest
pip install pytest pytest-cov

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/unit/test_email_controller.py
```

## 📝 Coding Guidelines

### Style Guide
- Seguir PEP 8
- Línea máxima: 100 caracteres
- Usar type hints en funciones públicas
- Docstrings en formato Google

### Ejemplo de Función
```python
def send_email(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Send an email via Gmail API.
    
    Args:
        recipient: Email address of the recipient
        subject: Email subject
        body: Email body text
        
    Returns:
        Dict with status and message
        
    Raises:
        ValueError: If recipient is invalid
    """
    pass
```

## 🔍 Debugging

### Local Development
```python
# En run.py, Flask debug está activado por defecto
# Puedes agregar breakpoints:
import pdb; pdb.set_trace()
```

### Docker Debugging
```bash
# Ver logs en tiempo real
docker-compose logs -f telegram-bot

# Entrar al contenedor
docker-compose exec telegram-bot bash

# Ver variables de entorno
docker-compose exec telegram-bot env
```

## 🌐 Webhook vs Polling

### Webhook (Producción)
```python
# Configurar en .env
USE_WEBHOOK=True
WEBHOOK_URL=https://tu-dominio.com/webhook

# Usar ngrok para desarrollo local
ngrok http 5000
```

### Polling (Desarrollo)
Para usar polling en lugar de webhook, crear un script separado:
```python
# polling_bot.py
import time
import requests
from app.config import config

offset = None
while True:
    updates = get_updates(offset)
    # Procesar updates...
    time.sleep(1)
```

## 🔐 Seguridad

### Secretos
- NUNCA commitear `.env`, `credentials.json`, `token.json`
- Rotar SECRET_KEY en producción
- Usar HTTPS en producción
- Validar inputs de usuario

### Google OAuth
```python
# Token se refresca automáticamente
# Si expira, eliminar token.json y re-autenticar
```

## 📦 Dependencias

### Principales
- Flask: Web framework
- google-api-python-client: Google APIs
- requests: HTTP client
- python-dotenv: Environment variables

### Desarrollo
- pytest: Testing
- black: Code formatter
- flake8: Linter

### Agregar Nueva Dependencia
```bash
pip install nueva-dependencia
pip freeze > requirements.txt
```

## 🚀 Deployment

### Docker Production
```yaml
# docker-compose.prod.yml
services:
  telegram-bot:
    restart: always
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
```

### Environment Variables en Producción
- Usar secretos de Docker/Kubernetes
- No usar archivos .env en producción
- Inyectar via CI/CD

## 🔄 Git Workflow

### Branches
- `main`: Producción estable
- `develop`: Desarrollo
- `feature/nombre`: Nuevas características
- `hotfix/nombre`: Correcciones urgentes

### Commits
```bash
# Formato recomendado
git commit -m "feat: agregar comando para leer emails"
git commit -m "fix: corregir formato de fecha en calendario"
git commit -m "docs: actualizar README con nuevos comandos"
```

### Tipos de Commit
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato, sin cambios de código
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Mantenimiento

## 📊 Monitoring (Futuro)

### Health Checks
```bash
# Verificar servicio
curl http://localhost:5000/health

# En Docker
docker-compose ps  # Ver estado
```

### Logging
```python
# Los logs ya están configurados
import logging
logger = logging.getLogger(__name__)

logger.debug("Mensaje de debug")
logger.info("Información")
logger.warning("Advertencia")
logger.error("Error")
```

### Métricas (Implementación futura)
- Prometheus + Grafana
- Tiempo de respuesta
- Tasa de errores
- Uso de recursos

## 🔧 Troubleshooting Común

### Puerto 5000 en uso
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Problemas con Google Auth
```bash
# Eliminar token y re-autenticar
rm token.json
python run.py
```

### Docker no inicia
```bash
# Verificar logs
docker-compose logs

# Rebuild sin cache
docker-compose build --no-cache

# Limpiar todo y reiniciar
docker-compose down -v
docker system prune -f
docker-compose up -d --build
```

## 🎯 Performance Tips

### Flask
- Usar gunicorn en producción
- Ajustar número de workers según CPU
- Implementar caching para respuestas comunes

### Google APIs
- Usar batch requests cuando sea posible
- Implementar rate limiting
- Cachear respuestas frecuentes

### Docker
- Multi-stage builds para imágenes más pequeñas
- .dockerignore para reducir contexto
- Volume mounts solo lo necesario

## 📚 Recursos Útiles

### Documentación
- Flask: https://flask.palletsprojects.com/
- Google APIs: https://developers.google.com/
- Telegram Bot API: https://core.telegram.org/bots/api
- Docker: https://docs.docker.com/

### Comunidad
- Stack Overflow
- Reddit: r/flask, r/learnpython
- Discord: Python Discord

---

**Mantener este archivo actualizado con descubrimientos y soluciones**
