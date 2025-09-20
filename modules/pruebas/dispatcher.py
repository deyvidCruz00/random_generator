# Importa las diferentes funciones de pruebas estadísticas desde sus módulos
from modules.pruebas.prueba_de_medias import prueba_de_medias
from modules.pruebas.prueba_de_varianza import prueba_de_varianza
from modules.pruebas.prueba_chi2_2 import prueba_chi_cuadrado
from modules.pruebas.ks import kolmogorov_smirnov_test
from modules.pruebas.poker import poker_test_json
from modules.pruebas.rachas import prueba_rachas
##from modules.pruebas.prueba_rachas import prueba_rachas  # Línea duplicada comentada

# Diccionario que mapea nombres cortos con las funciones de prueba
# Actúa como un registro de todas las pruebas disponibles
PRUEBAS_DISPONIBLES = {
    "medias": prueba_de_medias,      # Prueba de medias
    "varianza": prueba_de_varianza,  # Prueba de varianza
    "chi": prueba_chi_cuadrado,      # Prueba chi-cuadrado
    "kolmogorov": kolmogorov_smirnov_test,  # Test Kolmogorov-Smirnov
    "poker": poker_test_json,        # Test de poker
    "rachas": prueba_rachas          # Prueba de rachas
}

def ejecutar_pruebas(datos, pruebas, alpha):
    """
    Ejecuta múltiples pruebas estadísticas según la configuración proporcionada
    
    Parámetros:
    - datos: los números a analizar
    - pruebas: diccionario con configuración de qué pruebas ejecutar
    - alpha: nivel de significancia (ej: 0.05)
    """
    resultados = {}
    
    # Itera sobre cada prueba solicitada
    for nombre, info in pruebas.items():
        
        # Casos especiales: Kolmogorov y Chi-cuadrado necesitan parámetro 'k'
        if nombre == "kolmogorov" and info != False and nombre in PRUEBAS_DISPONIBLES:
            # Extrae el parámetro 'k' de la configuración y ejecuta la prueba
            resultados[nombre] = PRUEBAS_DISPONIBLES[nombre](datos, k=info.get("k"), alpha=alpha)
            
        elif nombre == "chi" and info != False and nombre in PRUEBAS_DISPONIBLES:
            # Mismo proceso para chi-cuadrado
            resultados[nombre] = PRUEBAS_DISPONIBLES[nombre](datos, k=info.get("k"), alpha=alpha)
            
        # Caso general: otras pruebas que solo necesitan datos y alpha
        elif info and nombre in PRUEBAS_DISPONIBLES:
            resultados[nombre] = PRUEBAS_DISPONIBLES[nombre](datos, alpha=alpha)
    
    return resultados

"""
FUNCIONAMIENTO:
1. Define un catálogo de pruebas estadísticas disponibles
2. La función principal recibe datos y configuración de pruebas
3. Para cada prueba activa, verifica si necesita parámetros especiales
4. Ejecuta la prueba correspondiente y guarda el resultado
5. Retorna un diccionario con todos los resultados

EJEMPLO DE USO:
datos = [0.1, 0.2, 0.3, ...]
config_pruebas = {
    "medias": True,
    "chi": {"k": 10},
    "kolmogorov": {"k": 5}
}
resultados = ejecutar_pruebas(datos, config_pruebas, 0.05)
"""