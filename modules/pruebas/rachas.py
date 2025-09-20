import numpy as np
from scipy.stats import norm
import json

def prueba_rachas(muestra, alpha=0.05, mediana_teorica=0.5):
    """
    Test de Rachas (Runs Test): evalúa si una secuencia de números
    es aleatoria analizando la alternancia de valores por encima y por debajo de la mediana.
    
    Una "racha" es una secuencia consecutiva de valores del mismo tipo (+ o -).
    
    Parámetros:
        muestra: Lista de números a evaluar
        alpha: Nivel de significancia (default 0.05)
        mediana_teorica: Valor de referencia para clasificar (default 0.5)
    """
    
    # PASO 1: Preparar datos
    muestra = np.array(muestra)
    
    # Calcular mediana de la muestra (para información)
    mediana_muestral = np.median(muestra)
    
    # PASO 2: Convertir números a signos
    # '+' si el valor es >= mediana_teorica, '-' si es menor
    # Ejemplo: [0.3, 0.7, 0.8, 0.2] → ['-', '+', '+', '-']
    signos = ['+' if x >= mediana_teorica else '-' for x in muestra]
    
    # PASO 3: Contar signos positivos y negativos
    n_pos = signos.count('+')  # Cantidad de valores >= 0.5
    n_neg = signos.count('-')  # Cantidad de valores < 0.5
    n = n_pos + n_neg         # Total (debe ser = len(muestra))
    
    # PASO 4: Contar número de rachas
    # Una racha = secuencia consecutiva del mismo signo
    # Ejemplo: ['+', '+', '-', '-', '+'] → 3 rachas: (++), (--), (+)
    rachas = 1  # Empezamos con 1 racha
    for i in range(1, len(signos)):
        if signos[i] != signos[i-1]:  # Cambio de signo = nueva racha
            rachas += 1
    
    # PASO 5: Calcular estadísticos esperados
    # Valor esperado del número de rachas bajo hipótesis de aleatoriedad
    ur = ((2 * n_pos * n_neg) / n) + 1
    
    # Varianza del número de rachas
    varianza = (2 * n_pos * n_neg * (2 * n_pos * n_neg - n)) / (n**2 * (n - 1))
    
    # PASO 6: Calcular estadístico Z normalizado
    # Compara las rachas observadas vs las esperadas
    z = (rachas - ur) / np.sqrt(varianza)
    
    # PASO 7: Obtener valores críticos para test bilateral
    z_crit = norm.ppf(1 - alpha/2)  # Valor crítico Z (ej: 1.96 para α=0.05)
    rango_min, rango_max = -z_crit, z_crit  # [-1.96, 1.96] para α=0.05
    
    # PASO 8: Decisión estadística
    # Si Z está en [-z_crit, z_crit], la secuencia es aleatoria
    cumple = rango_min <= z <= rango_max
    
    # PASO 9: Estructurar resultado
    result = {
        "test_name": "Prueba de Rachas",
        "Mediana_muestral": mediana_muestral,      # Mediana observada
        "Mediana_teorica": mediana_teorica,        # Punto de corte (0.5)
        "Total_may": n_pos,                        # Cantidad de valores ≥ 0.5
        "Total_min": n_neg,                        # Cantidad de valores < 0.5
        "Total": n,                                # Total de valores
        "Rachas": rachas,                          # Rachas observadas
        "UR": ur,                                  # Rachas esperadas
        "Varianza": varianza,                      # Varianza de las rachas
        "Z": z,                                    # Estadístico Z normalizado
        "Rango_min": rango_min,                    # Límite inferior [-z_crit]
        "Rango_max": rango_max,                    # Límite superior [+z_crit]
        "decision": "Pasa la prueba de rachas." if cumple else "No pasa la prueba de rachas.",
        "isApproved": str(cumple)
    }
    
    return json.dumps(result, indent=4)
"""
¿QUÉ HACE ESTE TEST?

El test de rachas evalúa la ALEATORIEDAD de una secuencia analizando si los valores
se alternan de forma natural entre "altos" y "bajos" respecto a la mediana.

CONCEPTO DE "RACHA":
Una racha es una secuencia consecutiva de valores del mismo tipo.
Ejemplo con mediana=0.5:
[0.3, 0.2, 0.7, 0.8, 0.1] → [-, -, +, +, -] → 3 rachas: (--), (++), (-)

¿QUÉ DETECTA?
1. MUY POCAS RACHAS: 
   - Tendencia o patrón (ej: [-, -, -, +, +, +])
   - Los valores tienden a agruparse
   
2. DEMASIADAS RACHAS:
   - Alternancia excesiva (ej: [-, +, -, +, -, +])
   - Oscilación artificial

3. RACHAS NORMALES:
   - Alternancia natural esperada en datos aleatorios

LÓGICA ESTADÍSTICA:
- Bajo aleatoriedad, el número de rachas sigue una distribución conocida
- Se calcula cuántas rachas se esperan teóricamente
- Se compara con las observadas usando estadístico Z
- Si Z está en rango normal → secuencia es aleatoria

EJEMPLO PRÁCTICO:
Secuencia: [0.2, 0.3, 0.7, 0.8, 0.1] con mediana=0.5
→ Signos: [-, -, +, +, -]
→ Rachas: 3 (dos grupos de -, un grupo de +, un grupo final de -)
→ Se compara 3 vs el número esperado estadísticamente

PROPÓSITO:
Detectar patrones temporales o tendencias en secuencias que deberían ser aleatorias.
Es especialmente útil para validar generadores de números pseudoaleatorios.
"""