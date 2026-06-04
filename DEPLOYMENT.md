# Configuración para producción de la API

## Opciones de deployment

### 1. Con Gunicorn (Recomendado para Linux/Mac)

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con múltiples workers
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### 2. Con uvicorn en modo producción

```bash
# Ejecutar sin --reload (para desarrollo)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Con Docker

Crea un archivo `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Construir y ejecutar:

```bash
docker build -t respuestas-aleatorias .
docker run -p 8000:8000 respuestas-aleatorias
```

### 4. Con Docker Compose

Crea un archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

Ejecutar:

```bash
docker-compose up -d
```

### 5. Con Nginx (Reverse Proxy)

Archivo de configuración `/etc/nginx/sites-available/respuestas-api`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. En Heroku

1. Crear archivo `Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Deployar:

```bash
heroku create tu-app-name
git push heroku main
```

### 7. En AWS Lambda (con Zappa)

```bash
pip install zappa
zappa init
zappa deploy production
```

### 8. En Google Cloud Run

```bash
gcloud run deploy respuestas-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 9. En Azure App Service

```bash
az webapp up --name tu-app-name --resource-group tu-grupo
```

## Variables de entorno recomendadas

```bash
# .env
ENVIRONMENT=production
DEBUG=False
WORKERS=4
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info
```

## Monitoreo y Logging

### Con Prometheus

```bash
pip install prometheus-client
```

### Con ELK Stack

Integración recomendada para centralized logging.

### Con Sentry

```bash
pip install sentry-sdk
```

En `main.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="tu-dsn-aqui",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```

## Seguridad en producción

### 1. HTTPS/SSL

```bash
# Con Let's Encrypt
sudo certbot certonly --standalone -d tu-dominio.com
```

### 2. CORS

Si necesitas CORS desde otro dominio:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting

```bash
pip install slowapi
```

En `main.py`:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/preguntar")
@limiter.limit("10/minute")
def preguntar(request: Request, pregunta: Pregunta):
    ...
```

### 4. Autenticación API Key

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != "tu-api-key-secreto":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida"
        )
    return api_key

@app.post("/preguntar")
def preguntar(pregunta: Pregunta, api_key: str = Depends(verify_api_key)):
    ...
```

## Performance Tuning

### 1. Caché con Redis

```bash
pip install redis aioredis
```

### 2. Compresión

```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

### 3. Connection Pooling

Para bases de datos (si se agregan).

## Backup y Recuperación

Si agregas base de datos:

```bash
# PostgreSQL
pg_dump -U usuario bd_nombre > backup.sql

# MongoDB
mongodump --uri "mongodb://usuario:contraseña@localhost/bd"
```

## Monitoreo de salud

Agregar endpoint de health check:

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

Configurar monitoreo:

```bash
# Con uptime monitoring
curl http://localhost:8000/health
```

## Checklist de Producción

- [ ] SSL/HTTPS configurado
- [ ] Rate limiting habilitado
- [ ] CORS configurado
- [ ] Logging centralizado
- [ ] Monitoreo de errores (Sentry)
- [ ] Backups automatizados
- [ ] Health checks configurados
- [ ] Documentación actualizada
- [ ] Tests pasando
- [ ] Performance optimizado
