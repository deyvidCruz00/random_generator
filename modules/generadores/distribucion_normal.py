import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


def distribucion_normal_inversa(uniformes,std_dev, mean):
    # Generar uniformes con tu congruencial lineal
    # print(uniformes)
    registros = []
    for i, u in enumerate(uniformes):
        # Inversa de la CDF de la normal (usa la f.d.p. integrada)
        x = norm.ppf(u, loc=mean, scale=std_dev)
        registros.append({
            "i": i,
            "U": u,
            "Ni": x
        })

    return pd.DataFrame(registros)

def graficar_distribucion_normal(df_uniformes,std_dev, mean):

    # Generar datos
    df = distribucion_normal_inversa(df_uniformes,std_dev, mean)
    muestras = df["Ni"].values

    plt.figure(figsize=(8, 5))

    # Histograma de las muestras simuladas
    plt.hist(muestras, bins=40, density=True, alpha=0.6, color='skyblue', edgecolor='black', label="Muestras simuladas")

    # Curva teórica de la distribución normal
    x = np.linspace(min(muestras), max(muestras), 200)
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