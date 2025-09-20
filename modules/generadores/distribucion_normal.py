import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


def distribucion_normal_inversa(uniformes, std_dev, mean):
    # Generar uniformes con tu congruencial lineal
    # print(uniformes)
    registros = []
    for i, u in enumerate(uniformes):
        # Validar que el valor uniforme esté en un rango válido
        # Evitar valores exactamente 0 o 1 que causan -inf o +inf
        u_clamp = max(1e-10, min(1 - 1e-10, u))
        
        # Inversa de la CDF de la normal (usa la f.d.p. integrada)
        x = norm.ppf(u_clamp, loc=mean, scale=std_dev)
        
        # Verificar que el resultado sea finito
        if np.isfinite(x):
            registros.append({
                "i": i,
                "U": u,
                "Ni": x
            })

    return pd.DataFrame(registros)

def graficar_distribucion_normal(df_uniformes, std_dev, mean):
    # Generar datos
    df = distribucion_normal_inversa(df_uniformes, std_dev, mean)
    muestras = df["Ni"].values
    
    # Verificar que tenemos datos válidos
    if len(muestras) == 0:
        raise ValueError("No se generaron muestras válidas para la distribución normal")
    
    # Filtrar valores infinitos o NaN que puedan haber pasado
    muestras_finitas = muestras[np.isfinite(muestras)]
    
    if len(muestras_finitas) == 0:
        raise ValueError("Todas las muestras generadas contienen valores no finitos")
    
    plt.figure(figsize=(8, 5))

    # Histograma de las muestras simuladas
    plt.hist(muestras_finitas, bins=40, density=True, alpha=0.6, color='skyblue', edgecolor='black', label="Muestras simuladas")

    # Curva teórica de la distribución normal
    # Usar un rango apropiado basado en los datos reales
    x_min, x_max = np.percentile(muestras_finitas, [0.1, 99.9])
    x_range = x_max - x_min
    x_min -= 0.1 * x_range
    x_max += 0.1 * x_range
    
    x = np.linspace(x_min, x_max, 200)
    pdf = norm.pdf(x, loc=mean, scale=std_dev)
    plt.plot(x, pdf, 'r-', linewidth=2, label="Curva teórica N(μ,σ)")

    plt.title("Distribución Normal simulada vs teórica")
    plt.xlabel("Valor")
    plt.ylabel("Densidad de probabilidad")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Guardar la figura en un buffer y devolverla como base64
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64