@REM Ejemplos de uso de la API con cURL

@REM ============================================
@REM 1. INFORMACIÓN DE LA API
@REM ============================================
curl http://localhost:8000/


@REM ============================================
@REM 2. OBTENER TIPOS DE RESPUESTAS DISPONIBLES
@REM ============================================
curl http://localhost:8000/tipos


@REM ============================================
@REM 3. HACER UNA PREGUNTA POSITIVA
@REM ============================================
curl -X POST http://localhost:8000/preguntar ^
  -H "Content-Type: application/json" ^
  -d "{\"texto\": \"¿Conseguiré el trabajo que deseo?\"}"


@REM ============================================
@REM 4. HACER UNA PREGUNTA NEGATIVA
@REM ============================================
curl -X POST http://localhost:8000/preguntar ^
  -H "Content-Type: application/json" ^
  -d "{\"texto\": \"¿Esto nunca funcionará?\"}"


@REM ============================================
@REM 5. HACER UNA PREGUNTA NEUTRALA
@REM ============================================
curl -X POST http://localhost:8000/preguntar ^
  -H "Content-Type: application/json" ^
  -d "{\"texto\": \"¿Debería cambiar de carrera?\"}"


@REM ============================================
@REM 6. HACER UNA PREGUNTA FILOSÓFICA
@REM ============================================
curl -X POST http://localhost:8000/preguntar ^
  -H "Content-Type: application/json" ^
  -d "{\"texto\": \"¿Cuál es el verdadero significado de la vida?\"}"


@REM ============================================
@REM 7. HACER UNA PREGUNTA HUMORÍSTICA
@REM ============================================
curl -X POST http://localhost:8000/preguntar ^
  -H "Content-Type: application/json" ^
  -d "{\"texto\": \"¿Esto es una broma?\"}"


@REM ============================================
@REM 8. OBTENER RESPUESTA ALEATORIA
@REM ============================================
curl http://localhost:8000/respuesta-aleatoria


@REM ============================================
@REM 9. OBTENER TODAS LAS RESPUESTAS POSITIVAS
@REM ============================================
curl http://localhost:8000/respuestas/positivas


@REM ============================================
@REM 10. OBTENER TODAS LAS RESPUESTAS NEGATIVAS
@REM ============================================
curl http://localhost:8000/respuestas/negativas


@REM ============================================
@REM 11. OBTENER TODAS LAS RESPUESTAS NEUTRALES
@REM ============================================
curl http://localhost:8000/respuestas/neutrales


@REM ============================================
@REM 12. OBTENER TODAS LAS RESPUESTAS FILOSÓFICAS
@REM ============================================
curl http://localhost:8000/respuestas/filosoficas


@REM ============================================
@REM 13. OBTENER TODAS LAS RESPUESTAS HUMORÍSTICAS
@REM ============================================
curl http://localhost:8000/respuestas/humoristicas


@REM ============================================
@REM 14. HACER MÚLTIPLES PREGUNTAS (LOTE)
@REM ============================================
curl -X POST http://localhost:8000/preguntar-lote ^
  -H "Content-Type: application/json" ^
  -d "[{\"texto\": \"¿Tendré suerte?\"}, {\"texto\": \"¿Debo cambiar de carrera?\"}, {\"texto\": \"¿Funcionará mi idea?\"}]"


@REM ============================================
@REM NOTAS:
@REM - Asegúrate de que el servidor esté ejecutándose en http://localhost:8000
@REM - Los caracteres ^ al final de las líneas son continuaciones de línea en Batch
@REM - Los caracteres \" representan comillas dentro de JSON
@REM ============================================
