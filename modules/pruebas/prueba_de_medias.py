import numpy as np
import math
from scipy.stats import norm
import json

def prueba_de_medias(datos, alpha=0.05, mu_esperada=0.5):
    """
    Test de Medias: verifica si la media de los datos es estadísticamente
    igual a la media esperada de una distribución uniforme (0.5)
    
    Parámetros:
    - datos: lista de números pseudoaleatorios
    - alpha: nivel de significancia (default: 0.05)
    - mu_esperada: media esperada para distribución uniforme [0,1] (default: 0.5)
    """
    
    # PASO 1: Preparar los datos
    datos = np.array(datos).tolist()  # Convierte a lista para serialización JSON
    n = len(datos)

    # PASO 2: Calcular estadísticos básicos
    media_muestra = np.mean(datos)  # Media observada de los datos

    # PASO 3: Obtener valor crítico Z para test bilateral
    # alpha/2 porque es prueba bilateral (media puede ser mayor O menor)
    z = norm.ppf(1 - alpha/2)  # Valor Z de la distribución normal estándar

    # PASO 4: Calcular margen de error
    # Para distribución uniforme [0,1]: varianza = 1/12
    # Error estándar = desviación_estándar / sqrt(n) = sqrt(1/12) / sqrt(n)
    error = z * (1 / math.sqrt(12 * n))
    
    # PASO 5: Construir intervalo de confianza
    # Si la media verdadera es 0.5, la media muestral debería estar en este intervalo
    limite_inferior = mu_esperada - error  # 0.5 - margen_error
    limite_superior = mu_esperada + error  # 0.5 + margen_error

    # PASO 6: Decisión estadística
    # Si la media observada está dentro del intervalo, los datos pasan la prueba
    if limite_inferior <= media_muestra <= limite_superior:
        decision = "Pasa la prueba de medias."
        pasa_prueba = True
    else:
        decision = "No pasa la prueba de medias."
        pasa_prueba = False

    # PASO 7: Estructurar resultado
    resultado = {
        "test_name": "Prueba de Medias",
        "n": n,                                    # Tamaño de muestra
        "alpha": alpha,                            # Nivel de significancia
        "mu_esperada": mu_esperada,                # Media esperada (0.5)
        "media_muestra": media_muestra,            # Media observada
        "z": z,                                    # Valor crítico Z
        "error": error,                            # Margen de error
        "limite_inferior": limite_inferior,        # Límite inferior del intervalo
        "limite_superior": limite_superior,        # Límite superior del intervalo
        "decision": decision,                      # Texto de la decisión
        "isApproved": str(pasa_prueba)            # Boolean como string
    }

    return json.dumps(resultado, indent=4)

"""
¿QUÉ HACE ESTE TEST?

El test de medias verifica si la media de un conjunto de números pseudoaleatorios
es estadísticamente consistente con la media esperada de una distribución uniforme (0.5).

LÓGICA ESTADÍSTICA:
1. Para números uniformes en [0,1], la media teórica es 0.5
2. La media de cualquier muestra tendrá cierta variabilidad aleatoria
3. Construye un intervalo de confianza alrededor de 0.5
4. Si la media observada cae fuera del intervalo, es sospechosa

FÓRMULAS CLAVE:
- Media esperada: μ = 0.5 (para Uniforme[0,1])
- Varianza esperada: σ² = 1/12 (para Uniforme[0,1])
- Error estándar: σ/√n = √(1/12)/√n = 1/√(12n)
- Intervalo de confianza: μ ± Z(α/2) × error_estándar

EJEMPLO:
- Si tienes 100 números con media 0.52 y α=0.05
- Error estándar ≈ 1/√(12×100) ≈ 0.029
- Intervalo 95%: 0.5 ± 1.96 × 0.029 ≈ [0.443, 0.557]
- Como 0.52 está en [0.443, 0.557], pasa la prueba

PROPÓSITO: 
Detectar si un generador produce números con media sesgada
(por ejemplo, genera más números altos que bajos, o viceversa).

NOTA TÉCNICA:
Usa la distribución normal como aproximación (Teorema Central del Límite)
para muestras suficientemente grandes (n ≥ 30 típicamente).
"""