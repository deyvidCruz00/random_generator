import numpy as np
import math
from scipy.stats import norm
import json

def prueba_de_medias(datos, alpha=0.05, mu_esperada=0.5):
    # Convertir a array
    datos = np.array(datos).tolist()  # Para que sea serializable en JSON
    n = len(datos)

    # Estadísticos básicos
    media_muestra = np.mean(datos)

    # Valor crítico Z
    z = norm.ppf(1 - alpha/2)

    # Intervalo de confianza (para Uniforme(0,1))
    error = z * (1 / math.sqrt(12 * n))
    limite_inferior = mu_esperada - error
    limite_superior = mu_esperada + error

    # Decisión
    if limite_inferior <= media_muestra <= limite_superior:
        decision = "No se rechaza H0 (la media esperada coincide con la muestral)."
    else:
        decision = "Se rechaza H0 (la media esperada difiere de la muestral)."

    # Construcción del diccionario con todas las variables
    resultado = {
        "datos": datos,
        "n": n,
        "alpha": alpha,
        "mu_esperada": mu_esperada,
        "media_muestra": media_muestra,
        "z": z,
        "error": error,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "decision": decision
    }

    # Retornar en formato JSON
    return json.dumps(resultado, indent=4)


# Ejemplo de uso
np.random.seed(42)
datos = np.random.uniform(0,1,50)

resultado = prueba_de_medias(datos, alpha=0.05)
print(resultado)
