import numpy as np
from scipy.stats import norm
import json

def prueba_rachas(muestra, alpha=0.05, mediana_teorica=0.5):
    """
    Test de Rachas (Runs Test): evalúa si una secuencia de números
    es aleatoria analizando la alternancia de valores por encima y por debajo de la mediana.
    """
    
    # PASO 1: Preparar datos
    muestra = np.array(muestra)
    mediana_muestral = np.median(muestra)
    
    # PASO 2: Convertir números a signos
    signos = ['+' if x >= mediana_teorica else '-' for x in muestra]
    
    # PASO 3: Contar signos
    n_pos = signos.count('+')
    n_neg = signos.count('-')
    n = n_pos + n_neg
    
    # PASO 4: Contar rachas
    rachas = 1
    for i in range(1, len(signos)):
        if signos[i] != signos[i-1]:
            rachas += 1
    
    # PASO 5: Estadísticos esperados
    ur = ((2 * n_pos * n_neg) / n) + 1
    varianza = (2 * n_pos * n_neg * (2 * n_pos * n_neg - n)) / (n**2 * (n - 1))
    
    # PASO 6: Calcular Z (controlando varianza=0)
    if varianza == 0:
        z = None
        if rachas == ur:
            decision = "El número de rachas está completamente determinado. La prueba no aplica (compatible con H0)."
            cumple = False
        else:
            decision = "Error: rachas observadas no pueden diferir del valor esperado cuando Var=0."
            cumple = False
        rango_min, rango_max = None, None
    else:
        z = (rachas - ur) / np.sqrt(varianza)
        z_crit = norm.ppf(1 - alpha/2)
        rango_min, rango_max = -z_crit, z_crit
        cumple = rango_min <= z <= rango_max
        decision = "Pasa la prueba de rachas." if cumple else "No pasa la prueba de rachas."
    
    # PASO 7: Resultado
    result = {
        "test_name": "Prueba de Rachas",
        "Mediana_muestral": mediana_muestral,
        "Mediana_teorica": mediana_teorica,
        "Total_may": n_pos,
        "Total_min": n_neg,
        "Total": n,
        "Rachas": rachas,
        "UR": ur,
        "Varianza": varianza,
        "Z": None if z is None else float(z),
        "Rango_min": rango_min,
        "Rango_max": rango_max,
        "decision": decision,
        "isApproved": str(cumple)
    }
    
    return json.dumps(result, indent=4)
