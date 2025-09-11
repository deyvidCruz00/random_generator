import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm

def prueba_de_medias(datos, alpha=0.05, mu_esperada=0.5):
    # Convertir a array
    datos = np.array(datos)
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

    # Gráfica
    plt.figure(figsize=(7,4))
    plt.axvline(mu_esperada, color='red', linestyle='--', label=f"Media esperada = {mu_esperada}")
    plt.axvline(media_muestra, color='blue', linestyle='-', label=f"Media muestral = {media_muestra:.3f}")
    plt.hlines(y=0.5, xmin=limite_inferior, xmax=limite_superior, color='green', linewidth=3, label="IC 95%")
    plt.scatter(media_muestra, 0.5, color='blue', zorder=5)
    plt.title("Prueba de Medias con Intervalo de Confianza")
    plt.xlabel("Valor de la media")
    plt.legend()
    plt.show()

    return {
        "media_muestra": media_muestra,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "decision": decision
    }


np.random.seed(42)
datos = np.random.uniform(0,1,50)

resultado = prueba_de_medias(datos, alpha=0.05)

print(datos)