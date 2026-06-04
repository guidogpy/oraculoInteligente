# Generador de Respuestas Aleatorias - API REST

Una API REST en Python que simula un oráculo generador de respuestas aleatorias a preguntas ingresadas por el usuario.

## Características

- 🎲 Generación de respuestas aleatorias inteligentes
- 📊 5 tipos diferentes de respuestas:
  - **Positivas**: Afirmativas y motivadoras
  - **Negativas**: De advertencia o desaprobación
  - **Neutrales**: Equilibradas y reflexivas
  - **Filosóficas**: Profundas y contemplativas
  - **Humorísticas**: Chistosas e irónicas
- 🎯 Detección automática del tipo de pregunta
- 📝 Procesamiento de lotes de preguntas
- 🌐 Interfaz interactiva Swagger UI
- ⚡ Construida con FastAPI (framework moderno y rápido)

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar o descargar el proyecto**

```bash
cd "c:\Users\tuUser\PROYECTOS\responsa-ai"
```

2. **Instalar las dependencias**

```bash
pip install -r requirements.txt
```

## Uso

### 1. Iniciar el servidor

```bash
python main.py
```

O alternativamente:

```bash
uvicorn main:app --reload
```

El servidor se iniciará en `http://localhost:8000`

### 2. Acceder a la interfaz interactiva

Abre tu navegador en: **http://localhost:8000/docs**

Aquí puedes probar todos los endpoints de forma interactiva.

## Endpoints disponibles

### 1. **GET `/`**
Información general de la API

**Respuesta:**
```json
{
  "mensaje": "Bienvenido al Generador de Respuestas Aleatorias",
  "descripcion": "Haz una pregunta y recibe una respuesta aleatoria",
  "endpoints": {...}
}
```

### 2. **POST `/preguntar`**
Endpoint principal para hacer preguntas

**Solicitud:**
```json
{
  "texto": "¿Conseguiré el trabajo que deseo?"
}
```

**Respuesta:**
```json
{
  "pregunta": "¿Conseguiré el trabajo que deseo?",
  "respuesta": "¡Definitivamente sí!",
  "tipo": "positivas",
  "timestamp": "2024-12-15T10:30:45.123456"
}
```

### 3. **GET `/tipos`**
Obtiene los tipos de respuestas disponibles

**Respuesta:**
```json
{
  "tipos_disponibles": [
    "positivas",
    "negativas",
    "neutrales",
    "filosoficas",
    "humoristicas"
  ],
  "descripcion": {...}
}
```

### 4. **GET `/respuestas/{tipo}`**
Obtiene todas las respuestas de un tipo específico

**Ejemplo:** `GET /respuestas/humoristicas`

**Respuesta:**
```json
{
  "tipo": "humoristicas",
  "cantidad": 10,
  "respuestas": [
    "42... esa es la respuesta a todo",
    "¿Me preguntaste a mí o al universo?",
    ...
  ]
}
```

### 5. **GET `/respuesta-aleatoria`**
Devuelve una respuesta completamente aleatoria sin hacer una pregunta

**Respuesta:**
```json
{
  "respuesta": "La respuesta está dentro de ti",
  "tipo": "filosoficas",
  "timestamp": "2024-12-15T10:30:45.123456"
}
```

### 6. **POST `/preguntar-lote`**
Procesa múltiples preguntas de una sola vez (máximo 100)

**Solicitud:**
```json
[
  {"texto": "¿Tendré suerte?"},
  {"texto": "¿Debo cambiar de carrera?"},
  {"texto": "¿Funcionará mi idea?"}
]
```

**Respuesta:**
```json
{
  "total_preguntas": 3,
  "respuestas": [
    {...},
    {...},
    {...}
  ]
}
```

## Ejemplos de uso

### Con cURL

```bash
# Hacer una pregunta
curl -X POST "http://localhost:8000/preguntar" \
  -H "Content-Type: application/json" \
  -d '{"texto": "¿Conseguiré el trabajo?"}'

# Obtener tipos de respuestas
curl "http://localhost:8000/tipos"

# Obtener respuestas humorísticas
curl "http://localhost:8000/respuestas/humoristicas"
```

### Con Python (cliente incluido)

```bash
python cliente.py
```

Este script ejecuta automáticamente varios ejemplos de uso.

### Con Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Hacer una pregunta
response = requests.post(
    f"{BASE_URL}/preguntar",
    json={"texto": "¿Debo empezar un negocio?"}
)

resultado = response.json()
print(f"Pregunta: {resultado['pregunta']}")
print(f"Respuesta: {resultado['respuesta']}")
print(f"Tipo: {resultado['tipo']}")
```

## Detección automática de tipos

La API detecta automáticamente el tipo de pregunta basándose en palabras clave:

- **Positivas**: Detecta palabras como "si", "puedo", "conseguiré", "ganará", "éxito"
- **Negativas**: Detecta "nunca", "no podré", "perderé", "fracaso", "imposible"
- **Filosóficas**: Detecta "significado", "propósito", "verdad", "realidad", "existencia"
- **Humorísticas**: Detecta "jajaja", "broma", "humor", "chistoso"

Si no detecta ninguna palabra clave especial, elige un tipo aleatorio.

## Estructura del proyecto

```
responsa-ai/
├── main.py              # API principal con FastAPI
├── cliente.py           # Cliente Python para probar la API
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## Personalización

### Agregar nuevas respuestas

Edita el diccionario `RESPUESTAS_ALEATORIAS` en `main.py`:

```python
RESPUESTAS_ALEATORIAS = {
    "tupo_personalizado": [
        "Tu respuesta aquí",
        "Otra respuesta",
        ...
    ]
}
```

### Agregar nuevas palabras clave

Modifica el diccionario `PALABRAS_CLAVE`:

```python
PALABRAS_CLAVE = {
    "tu_tipo": ["palabra1", "palabra2", "palabra3"]
}
```

## Notas técnicas

- **Framework**: FastAPI
- **Servidor**: Uvicorn
- **Puerto predeterminado**: 8000
- **Host predeterminado**: 0.0.0.0 (accesible desde cualquier máquina en la red)
- **Documentación interactiva**: Swagger UI en `/docs`

## Posibles mejoras futuras

- Agregar persistencia (base de datos)
- Agregar autenticación y autorización
- Crear un frontend web
- Agregar análisis de sentimientos para mejor detección
- Integrar con bases de datos de IA
- Agregar caché de respuestas
- Implementar rate limiting
- Agregar logs más detallados

## Licencia

Este proyecto es de código abierto y está disponible para uso personal y comercial.

## Contacto

Para sugerencias o problemas, puedes crear un issue en el repositorio.
