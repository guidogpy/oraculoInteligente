"""
Cliente de ejemplo para probar la API de Generador de Respuestas Aleatorias
Puedes usar este script para hacer preguntas a la API
"""

import requests
import json
from typing import Dict, Any

# URL base de la API
BASE_URL = "http://localhost:8000"


class ClienteGeneradorRespuestas:
    """Cliente para interactuar con la API de respuestas aleatorias"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def hacer_pregunta(self, pregunta: str) -> Dict[str, Any]:
        """Hace una pregunta a la API y retorna la respuesta"""
        try:
            response = requests.post(
                f"{self.base_url}/preguntar",
                json={"texto": pregunta}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def obtener_tipos(self) -> Dict[str, Any]:
        """Obtiene los tipos de respuestas disponibles"""
        try:
            response = requests.get(f"{self.base_url}/tipos")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def obtener_respuestas_tipo(self, tipo: str) -> Dict[str, Any]:
        """Obtiene todas las respuestas de un tipo específico"""
        try:
            response = requests.get(f"{self.base_url}/respuestas/{tipo}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def respuesta_aleatoria(self) -> Dict[str, Any]:
        """Obtiene una respuesta completamente aleatoria"""
        try:
            response = requests.get(f"{self.base_url}/respuesta-aleatoria")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def main():
    """Función principal para demostrar el uso del cliente"""
    cliente = ClienteGeneradorRespuestas()
    
    print("=" * 60)
    print("GENERADOR DE RESPUESTAS ALEATORIAS - Cliente de Prueba")
    print("=" * 60)
    print()
    
    # Ejemplo 1: Obtener tipos disponibles
    print("1. Tipos de respuestas disponibles:")
    print("-" * 60)
    tipos = cliente.obtener_tipos()
    print(json.dumps(tipos, indent=2, ensure_ascii=False))
    print()
    
    # Ejemplo 2: Hacer una pregunta positiva
    print("2. Pregunta positiva:")
    print("-" * 60)
    pregunta1 = "¿Conseguiré el trabajo que deseo?"
    print(f"Pregunta: {pregunta1}")
    respuesta1 = cliente.hacer_pregunta(pregunta1)
    print(json.dumps(respuesta1, indent=2, ensure_ascii=False))
    print()
    
    # Ejemplo 3: Hacer una pregunta negativa
    print("3. Pregunta negativa:")
    print("-" * 60)
    pregunta2 = "¿Esto nunca funcionará?"
    print(f"Pregunta: {pregunta2}")
    respuesta2 = cliente.hacer_pregunta(pregunta2)
    print(json.dumps(respuesta2, indent=2, ensure_ascii=False))
    print()
    
    # Ejemplo 4: Hacer una pregunta filosófica
    print("4. Pregunta filosófica:")
    print("-" * 60)
    pregunta3 = "¿Cuál es el verdadero significado de la vida?"
    print(f"Pregunta: {pregunta3}")
    respuesta3 = cliente.hacer_pregunta(pregunta3)
    print(json.dumps(respuesta3, indent=2, ensure_ascii=False))
    print()
    
    # Ejemplo 5: Respuesta aleatoria
    print("5. Respuesta completamente aleatoria:")
    print("-" * 60)
    respuesta_aleatoria = cliente.respuesta_aleatoria()
    print(json.dumps(respuesta_aleatoria, indent=2, ensure_ascii=False))
    print()
    
    # Ejemplo 6: Obtener todas las respuestas de un tipo
    print("6. Todas las respuestas humorísticas:")
    print("-" * 60)
    respuestas_humor = cliente.obtener_respuestas_tipo("humoristicas")
    print(json.dumps(respuestas_humor, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
