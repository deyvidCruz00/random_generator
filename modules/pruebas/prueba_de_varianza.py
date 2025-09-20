import numpy as np
import math
import json
from scipy import stats

def prueba_de_varianza(datos, alpha=0.05, mu_esperada=0.5):
    """
    Test de Varianza: verifica si la varianza de los datos es consistente
    con la varianza esperada de una distribución uniforme (1/12 ≈ 0.0833)
    
    Parámetros:
    - datos: lista de números pseudoaleatorios
    - alpha: nivel de significancia (default: 0.05)
    - mu_esperada: media esperada (no se usa realmente en el cálculo)
    """
    
    # PASO 1: Preparar datos
    datos = np.array(datos).tolist()  # Para serialización JSON
    
    # Cálculo manual de la media (podría usar np.mean directamente)
    sum = 0.0
    for num in datos:
        sum += num
    mu_muestral = sum / len(datos)

    # Variables auxiliares para el cálculo
    alphaDiv2 = alpha / 2
    alpha_2 = 1 - alphaDiv2  # Nivel de confianza
        
    n = len(datos)

    # PASO 2: Calcular varianza muestral
    # ddof=1 usa denominador (n-1) en lugar de n (varianza insesgada)
    varianza = np.var(datos, ddof=1) 

    # PASO 3: Obtener valores críticos de Chi-cuadrado
    # Para test bilateral de varianza, se usan dos puntos críticos
    Xi1 = stats.chi2.ppf(alpha/2, n-1)      # Percentil inferior (α/2)
    Xi2 = stats.chi2.ppf(1 - alpha/2, n-1)  # Percentil superior (1-α/2)

    # PASO 4: Construir intervalo de confianza para la varianza
    # Para distribución uniforme [0,1]: varianza teórica = 1/12
    # Fórmula: χ²/(12(n-1)) donde χ² son los valores críticos
    li = Xi1 / (12 * (n-1))  # Límite inferior del intervalo
    ls = Xi2 / (12 * (n-1))  # Límite superior del intervalo

    # PASO 5: Calcular estadístico Chi-cuadrado observado
    # χ² = (n-1) × varianza_muestral / varianza_teórica
    # donde varianza_teórica = 1/12 para Uniforme[0,1]
    chi2 = ((n - 1) * varianza) / (1 / 12)

    # PASO 6: Decisión estadística
    # Si la varianza observada está dentro del intervalo de confianza, pasa la prueba
    if li <= varianza <= ls:
        decision = "Pasa la prueba de varianza."
        pasa_prueba = True
    else:
        decision = "No pasa la prueba de varianza."
        pasa_prueba = False

    # PASO 7: Estructurar resultado
    resultado = {
        "test_name": "Prueba de Varianza",
        "n": n,                              # Tamaño de muestra
        "alpha": alpha,                      # Nivel de significancia
        "media_muestral": mu_muestral,       # Media observada (calculada manualmente)
        "mu_esperada": mu_esperada,          # Media esperada (no se usa en cálculos)
        "alphaDiv2": alphaDiv2,              # α/2
        "z": alpha_2,                        # Nivel de confianza (1-α/2)
        "varianza_muestral": varianza,       # Varianza observada
        "Xi1": Xi1,                          # Chi² crítico inferior
        "Xi2": Xi2,                          # Chi² crítico superior
        "limite_inferior": li,               # Límite inferior para varianza
        "limite_superior": ls,               # Límite superior para varianza
        "chi2": chi2,                        # Estadístico Chi² calculado
        "decision": decision,                # Texto de la decisión
        "isApproved": str(pasa_prueba)      # Boolean como string
    }

    return json.dumps(resultado, indent=4)

"""
¿QUÉ HACE ESTE TEST?

El test de varianza verifica si la variabilidad de los números pseudoaleatorios
es consistente con la varianza esperada de una distribución uniforme (1/12 ≈ 0.0833).

LÓGICA ESTADÍSTICA:
1. Para números uniformes en [0,1], la varianza teórica es 1/12
2. La varianza de cualquier muestra tendrá cierta fluctuación aleatoria
3. Usa la distribución Chi-cuadrado para construir un intervalo de confianza
4. Si la varianza observada está fuera del intervalo, es sospechosa

FÓRMULAS CLAVE:
- Varianza teórica: σ² = 1/12 (para Uniforme[0,1])
- Estadístico: χ² = (n-1)×s²/σ² ~ χ²(n-1)
- Intervalo de confianza: [χ²α/2/(12(n-1)), χ²1-α/2/(12(n-1))]

¿QUÉ DETECTA?
- Varianza muy baja: números muy concentrados (poca aleatoriedad)
- Varianza muy alta: números muy dispersos (posible problema en el generador)

EJEMPLO:
- Con n=100, α=0.05, varianza teórica ≈ 0.0833
- Si varianza observada = 0.12 → podría no pasar (muy alta)
- Si varianza observada = 0.08 → probablemente pasa (normal)

PROPÓSITO:
Detectar generadores que producen números con variabilidad anormal,
ya sea muy concentrados o muy dispersos respecto a lo esperado.

NOTA TÉCNICA:
- Usa Chi-cuadrado porque (n-1)s²/σ² sigue distribución χ²(n-1)
- El test bilateral verifica si la varianza es diferente (mayor O menor) de 1/12
"""