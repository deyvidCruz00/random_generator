import numpy as np
import math
import json
from scipy import stats

def prueba_de_varianza(datos, alpha=0.05, mu_esperada=0.5):
    # Convertir a array
    datos = np.array(datos).tolist()  # para que sea serializable en JSON
    n = len(datos)

    # Varianza muestral
    varianza = np.var(datos, ddof=1) 

    # Valor crítico Chi-cuadrado
    Xi1 = stats.chi2.ppf(alpha/2, n-1)
    Xi2 = stats.chi2.ppf(1 - alpha/2, n-1)

    # Intervalo de confianza (para Uniforme(0,1))
    li = Xi1 / (12 * (n-1))
    ls = Xi2 / (12 * (n-1))

    chi2 = ((n - 1) * varianza) / (1 / 12)

    # Decisión
    if li <= varianza <= ls:
        decision = "Paso la prueba de varianza."
    else:
        decision = "No paso la prueba de varianza."

    # Construcción del resultado con todas las variables
    resultado = {
        "test_name": "Prueba de Varianza",
        "n": n,
        "alpha": alpha,
        "mu_esperada": mu_esperada,
        "varianza_muestral": varianza,
        "Xi1": Xi1,
        "Xi2": Xi2,
        "limite_inferior": li,
        "limite_superior": ls,
        "chi2": chi2,
        "decision": decision
    }

    return json.dumps(resultado, indent=4)


# Ejemplo de uso
np.random.seed(42)
datos = np.random.uniform(0,1,50)


resultado = prueba_de_varianza(datos, alpha=0.05)
print(resultado)
