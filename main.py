"""
Generador de Respuestas Inteligentes con IA Local - API REST
Oráculo que genera respuestas personalizadas usando modelo local de IA
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
import os
import random
from datetime import datetime
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import httpx

# Cargar variables de entorno desde el archivo .env si existe
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()
        logger.info("Variables de entorno cargadas desde archivo .env")
    except Exception as e:
        logger.warning(f"No se pudo leer el archivo .env: {e}")

# Establecer certificados SSL con certifi para Hugging Face
try:
    import certifi
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
    os.environ["CURL_CA_BUNDLE"] = certifi.where()
    logger.info("Certificados SSL configurados con certifi")
except ImportError:
    logger.warning("certifi no está instalado. Puede haber errores SSL al descargar modelos.")

# Intentar importar PyTorch y Transformers
try:
    import torch
    TORCH_AVAILABLE = True
    logger.info("PyTorch cargado exitosamente")
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch no está instalado. Las capacidades del modelo local no estarán disponibles.")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
    logger.info("Transformers cargado exitosamente")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers no está instalado. Usando respuestas predefinidas.")

LLM_ENGINE_AVAILABLE = TRANSFORMERS_AVAILABLE and TORCH_AVAILABLE

# Inicializar modelo de IA (se carga en primer acceso)
llm_pipeline = None

def cargar_modelo():
    """Carga el modelo de IA local de forma lazy"""
    global llm_pipeline
    if llm_pipeline is None and LLM_ENGINE_AVAILABLE:
        try:
            logger.info("Cargando modelo de IA local...")
            # Usar DistilGPT2 que es más ligero
            llm_pipeline = pipeline('text-generation', model='distilgpt2', device='cpu')
            logger.info("Modelo cargado exitosamente")
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {e}")
            llm_pipeline = None
    return llm_pipeline

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Oráculo Inteligente - Generador de Respuestas con IA",
    description="API que genera respuestas personalizadas usando IA local",
    version="2.0.0"
)

# Modelos de datos
class Pregunta(BaseModel):
    """Modelo para la pregunta del usuario"""
    texto: str
    categoria: str = "general"

class Respuesta(BaseModel):
    """Modelo para la respuesta generada"""
    pregunta: str
    respuesta: str
    tipo: str
    timestamp: str


# Base de datos de respuestas por tipo
RESPUESTAS_ALEATORIAS = {
    "positivas": [
        "¡Definitivamente sí!",
        "Es muy probable que sí",
        "Las perspectivas son buenas",
        "¡Excelente idea!",
        "Claro que sí",
        "Sin duda alguna",
        "¡Adelante con eso!",
        "Todas las señales apuntan a sí",
        "Es casi seguro",
        "¡Absolutamente!"
    ],
    "negativas": [
        "No creo que sea posible",
        "Mejor espera un poco",
        "No parece ser el momento",
        "Las probabilidades no son buenas",
        "Podría ser un error",
        "No es recomendable",
        "Habría que pensarlo más",
        "Parece difícil en este momento",
        "No me da buena sensación",
        "Probablemente no"
    ],
    "neutrales": [
        "Podría funcionar",
        "Es posible",
        "Depende de las circunstancias",
        "Necesitas más información",
        "El tiempo lo dirá",
        "Es difícil predecirlo",
        "Podrían pasar varias cosas",
        "Requiere análisis más profundo",
        "Todo es relativo",
        "Hay factores a considerar"
    ],
    "filosoficas": [
        "La respuesta está dentro de ti",
        "Todo es cuestión de perspectiva",
        "A veces la pregunta es más importante que la respuesta",
        "Lo que buscas está más cerca de lo que crees",
        "Reflexiona sobre lo que realmente deseas",
        "La verdad siempre está en el medio",
        "Cada pregunta contiene su propia respuesta",
        "Quizás deba reformular tu pregunta",
        "La sabiduría viene de hacer las preguntas correctas",
        "No siempre hay una respuesta clara"
    ],
    "humoristicas": [
        "42... esa es la respuesta a todo",
        "¿Me preguntaste a mí o al universo?",
        "Pregunta interesante, lástima que no sé la respuesta",
        "Si tuviera un dólar por cada vez que se pregunta eso...",
        "Consulta tu bola de cristal, la mía está en el taller",
        "¡Ojalá tuviera esa respuesta!",
        "¿Es una pregunta con trampa?",
        "Eso no está en mi manual de instrucciones",
        "¿Acaso pareço un gurú?",
        "Incluso Google duda de esa respuesta"
    ]
}

# Palabras clave para categorizar preguntas
PALABRAS_CLAVE = {
    "positivas": ["si", "puedo", "conseguiré", "ganará", "éxito", "logrará", "funcionará"],
    "negativas": ["nunca", "no podré", "perderé", "fracaso", "imposible", "malo"],
    "filosoficas": ["significado", "proposito", "sentido", "alma", "verdad", "realidad", "existencia"],
    "humoristicas": ["jajaja", "broma", "humor", "chistoso", "jocoso"]
}


@app.get("/")
def root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "Bienvenido al Generador de Respuestas Aleatorias",
        "descripcion": "Haz una pregunta y recibe una respuesta aleatoria",
        "endpoints": {
            "preguntar": "/preguntar",
            "tipos": "/tipos",
            "respuestas": "/respuestas/{tipo}"
        }
    }


@app.post("/preguntar", response_model=Respuesta)
def preguntar(pregunta: Pregunta):
    """
    Endpoint principal para hacer preguntas
    Recibe una pregunta y devuelve una respuesta aleatoria categorizada
    """
    if not pregunta.texto or len(pregunta.texto.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="La pregunta no puede estar vacía"
        )
    
    # Detectar tipo de pregunta según palabras clave
    texto_lower = pregunta.texto.lower()
    tipo_respuesta = "neutrales"  # Por defecto
    
    for tipo, palabras in PALABRAS_CLAVE.items():
        if any(palabra in texto_lower for palabra in palabras):
            tipo_respuesta = tipo
            break
    
    # Si no se detectó ninguna categoría especial, elegir aleatoriamente
    if tipo_respuesta == "neutrales":
        tipos = list(RESPUESTAS_ALEATORIAS.keys())
        tipo_respuesta = random.choice(tipos)
    
    # Seleccionar respuesta aleatoria del tipo detectado
    respuesta_texto = random.choice(RESPUESTAS_ALEATORIAS[tipo_respuesta])
    
    return Respuesta(
        pregunta=pregunta.texto,
        respuesta=respuesta_texto,
        tipo=tipo_respuesta,
        timestamp=datetime.now().isoformat()
    )


# Función para generar respuestas inteligentes basadas en análisis de la pregunta
def generar_respuesta_inteligente(pregunta_texto: str, categoria: str = "general") -> dict:
    """
    Genera una respuesta más inteligente analizando la pregunta
    Extrae palabras clave, emociones y contexto para personalizar la respuesta
    """
    texto_lower = pregunta_texto.lower().strip()
    tipo_respuesta = "inteligente"
    respuestas_personalizadas = []
    
    # Si el usuario seleccionó una categoría específica, usar esa
    if categoria == "amor":
        respuestas_personalizadas = [
            "El amor es la respuesta a la mayoría de las preguntas.",
            "Lo que sientes es real. Atrévete a expresarlo.",
            "El corazón siempre sabe el camino correcto.",
            "Amar es el acto más valiente que podemos hacer.",
            "El verdadero amor requiere vulnerabilidad y valentía.",
            "Cuando amas genuinamente, el universo se alinea contigo.",
            "No tengas miedo de abrirte. La vulnerabilidad es fuerza.",
            "El amor verdadero no tiene prisa. Confía en el timing.",
        ]
        tipo_respuesta = "corazon"
    
    elif categoria == "trabajo":
        respuestas_personalizadas = [
            "Tu trabajo debe estar alineado con tu propósito. Si no es así, reconsidera.",
            "La paciencia y la dedicación abren todas las puertas.",
            "No busques solo dinero. Busca satisfacción y crecimiento.",
            "Eres más valioso de lo que crees. Negocia tu valor.",
            "El éxito viene a quien persevera con intención.",
            "Tu pasión es tu poder. Úsalo.",
            "Los obstáculos en el trabajo son oportunidades disfrazadas.",
            "El crecimiento profesional comienza con creer en ti mismo.",
        ]
        tipo_respuesta = "exito"
    
    elif categoria == "dinero":
        respuestas_personalizadas = [
            "El dinero es energía. Úsalo con propósito y sabiduría.",
            "La abundancia viene para quien cree merecerla.",
            "Invertir en ti mismo es la mejor inversión.",
            "El dinero sigue al valor. Crea valor antes de buscar riqueza.",
            "La verdadera riqueza está en la paz mental y las relaciones.",
            "La escasez es un estado mental. Cambia tu perspectiva.",
            "La prosperidad es tu derecho natural. Reclámanla.",
            "Donde enfocas tu atención, fluye tu energía y dinero.",
        ]
        tipo_respuesta = "abundancia"
    
    elif categoria == "miedo":
        respuestas_personalizadas = [
            "El miedo es solo una ilusión. La verdad está dentro de ti.",
            "No tengas miedo de lo que no puedes controlar. Enfócate en lo que sí puedes.",
            "La valentía no es la ausencia de miedo, sino actuar a pesar de él.",
            "Lo que tememos generalmente nunca llega a ocurrir. Respira profundo.",
            "El universo está contigo. Confía en el proceso de la vida.",
            "El miedo es el guardián de las grandes transformaciones.",
            "Cuando enfrentas tus miedos, descubres tu verdadera fuerza.",
            "El otro lado del miedo es la libertad.",
        ]
        tipo_respuesta = "emocional"
    
    elif categoria == "duda":
        respuestas_personalizadas = [
            "La duda es el primer paso hacia la verdad. Cuestiona todo.",
            "No hay certeza absoluta. Actúa con la información que tienes.",
            "La incertidumbre es donde reside la libertad. Elige tu camino.",
            "A veces no hay respuesta correcta. Solo hay aprendizaje.",
            "Confía en tu intuición cuando la razón falla.",
            "La duda crece en la inacción. Haz un paso pequeño.",
            "Tu intuición sabe más de lo que tu mente cree.",
            "La claridad viene después de la acción, no antes.",
        ]
        tipo_respuesta = "sabiduria"
    
    else:  # categoria == "general"
        # Análisis automático de contexto
        palabras_urgencia = ["urgente", "prisa", "rápido", "ahora", "ya", "inmediato"]
        palabras_miedo = ["miedo", "asustado", "preocupado", "ansiedad", "nervioso", "tengo miedo", "me asusta"]
        palabras_esperanza = ["espero", "quiero", "deseo", "sueño", "ojalá", "espera", "confío"]
        
        tiene_urgencia = any(p in texto_lower for p in palabras_urgencia)
        tiene_miedo = any(p in texto_lower for p in palabras_miedo)
        tiene_esperanza = any(p in texto_lower for p in palabras_esperanza)
        
        if tiene_miedo:
            respuestas_personalizadas = [
                "El miedo es solo una ilusión. La verdad está dentro de ti.",
                "La valentía es actuar a pesar del miedo.",
                "Lo que tememos rara vez ocurre.",
            ]
            tipo_respuesta = "emocional"
        elif tiene_urgencia:
            respuestas_personalizadas = [
                "La prisa es enemiga de la sabiduría.",
                "Las mejores decisiones se toman con calma.",
                "El momento perfecto llegará.",
            ]
            tipo_respuesta = "reflexion"
        elif tiene_esperanza:
            respuestas_personalizadas = [
                "La esperanza es el combustible del cambio.",
                "Sueña en grande, actúa pequeño.",
                "Lo que imaginas, puedes crearlo.",
            ]
            tipo_respuesta = "inspiracion"
        else:
            respuestas_personalizadas = [
                "Cada pregunta contiene la semilla de su propia respuesta.",
                "La vida responde a la energía que proyectas.",
                "Lo que buscas afuera, lo llevas adentro.",
                "El cambio comienza con una pregunta.",
                "Confía en el proceso. Todo está sucediendo como debe ser.",
                "La respuesta que buscas es una oportunidad para crecer.",
                "Sigue tu intuición. Rara vez te engaña.",
                "La verdad siempre surge cuando estamos listos.",
            ]
    
    respuesta = random.choice(respuestas_personalizadas)
    
    return {
        "respuesta": respuesta,
        "tipo": tipo_respuesta,
        "timestamp": datetime.now().isoformat()
    }


def generar_respuesta_con_ia(pregunta_texto: str, categoria: str = "general") -> dict:
    """
    Genera respuesta usando la API de Gemini 2.5 Flash o fallback a respuestas inteligentes locales
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        logger.info("GEMINI_API_KEY no configurada. Usando respuestas predefinidas locales en español.")
        return generar_respuesta_inteligente(pregunta_texto, categoria)
        
    try:
        logger.info(f"Generando respuesta con Gemini para: {pregunta_texto[:50]}...")
        
        # Preparar el prompt del oráculo según la categoría
        prompts = {
            "amor": "Actúa como un oráculo sabio. Responde en español con sabiduría y empatía a esta pregunta sobre amor: ",
            "trabajo": "Actúa como un mentor sabio. Responde en español con visión y realismo a esta pregunta sobre carrera y trabajo: ",
            "dinero": "Actúa como un asesor espiritual. Responde en español con consejos sobre abundancia y mentalidad de prosperidad a esta pregunta sobre dinero: ",
            "miedo": "Actúa como un guía compasivo. Responde en español inspirando valentía y calma ante este miedo: ",
            "duda": "Actúa como un filósofo. Responde en español con claridad, perspicacia y profundidad a esta duda: ",
            "general": "Actúa como un oráculo antiguo y sabio. Responde en español con un tono misterioso, profundo y reflexivo a esta pregunta: ",
        }
        
        system_instruction = prompts.get(categoria, prompts["general"])
        prompt = system_instruction + pregunta_texto
        
        # Realizar la solicitud a la API de Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 150
            }
        }
        
        response = httpx.post(url, headers=headers, json=payload, timeout=10.0)
        response.raise_for_status()
        
        result = response.json()
        respuesta_texto = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        return {
            "respuesta": respuesta_texto,
            "tipo": f"gemini_{categoria}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error al generar con Gemini: {e}. Usando fallback local...")
        return generar_respuesta_inteligente(pregunta_texto, categoria)


@app.post("/preguntar-inteligente", response_model=Respuesta)
def preguntar_inteligente(pregunta: Pregunta):
    """
    Endpoint que genera respuestas con IA local
    Primero intenta usar el modelo de IA, si no está disponible usa respuestas predefinidas
    """
    if not pregunta.texto or len(pregunta.texto.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="La pregunta no puede estar vacía"
        )
    
    # Generar respuesta con IA
    respuesta_data = generar_respuesta_con_ia(pregunta.texto, pregunta.categoria)
    
    return Respuesta(
        pregunta=pregunta.texto,
        respuesta=respuesta_data["respuesta"],
        tipo=respuesta_data["tipo"],
        timestamp=respuesta_data["timestamp"]
    )



@app.get("/ui", response_class=HTMLResponse)
def ui():
    """Interfaz web simple para hacer preguntas y ver respuestas"""
    html_path = Path(__file__).resolve().parent / "templates" / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/tipos")
def obtener_tipos():
    """Endpoint que devuelve los tipos de respuestas disponibles"""
    return {
        "tipos_disponibles": list(RESPUESTAS_ALEATORIAS.keys()),
        "descripcion": {
            "positivas": "Respuestas afirmativas y motivadoras",
            "negativas": "Respuestas de advertencia o desaprobación",
            "neutrales": "Respuestas equilibradas y reflexivas",
            "filosoficas": "Respuestas profundas y contemplativas",
            "humoristicas": "Respuestas chistosas e irónicas"
        }
    }


@app.get("/respuestas/{tipo}")
def obtener_respuestas_por_tipo(tipo: str):
    """Endpoint que devuelve todas las respuestas de un tipo específico"""
    tipo_lower = tipo.lower()
    
    if tipo_lower not in RESPUESTAS_ALEATORIAS:
        raise HTTPException(
            status_code=404,
            detail=f"Tipo '{tipo}' no encontrado. Tipos disponibles: {', '.join(RESPUESTAS_ALEATORIAS.keys())}"
        )
    
    return {
        "tipo": tipo_lower,
        "cantidad": len(RESPUESTAS_ALEATORIAS[tipo_lower]),
        "respuestas": RESPUESTAS_ALEATORIAS[tipo_lower]
    }


@app.get("/respuesta-aleatoria")
def respuesta_aleatoria_simple():
    """Endpoint que devuelve una respuesta completamente aleatoria"""
    tipo_aleatorio = random.choice(list(RESPUESTAS_ALEATORIAS.keys()))
    respuesta = random.choice(RESPUESTAS_ALEATORIAS[tipo_aleatorio])
    
    return {
        "respuesta": respuesta,
        "tipo": tipo_aleatorio,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/preguntar-lote")
def preguntar_lote(preguntas: List[Pregunta]):
    """Endpoint que procesa múltiples preguntas de una sola vez"""
    if len(preguntas) == 0:
        raise HTTPException(
            status_code=400,
            detail="Se requiere al menos una pregunta"
        )
    
    if len(preguntas) > 100:
        raise HTTPException(
            status_code=400,
            detail="Máximo 100 preguntas por solicitud"
        )
    
    respuestas = []
    for pregunta in preguntas:
        respuesta = preguntar(pregunta)
        respuestas.append(respuesta)
    
    return {
        "total_preguntas": len(respuestas),
        "respuestas": respuestas
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
