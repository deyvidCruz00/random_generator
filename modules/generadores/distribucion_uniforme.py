
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64


def distribucion_uniforme(ri_list, min_value, max_value):
    ni_list = [min_value + (max_value - min_value) * r for r in ri_list]
    
    # Crear DataFrame con los resultados
    df = pd.DataFrame({
        'i': range(1, len(ri_list) + 1),
        'Ri': ri_list,
        'Ni': ni_list
    })
    
    return df, ni_list


def graficar_distribucion_uniforme(ri, ni, min_value, max_value):
    num_samples = len(ri)
    
    plt.figure(figsize=(12, 5))
    
    # --- Gráfico 1: Valores Ri en función del índice ---
    plt.subplot(1, 2, 1)
    plt.plot(range(num_samples), ri, marker=".", linestyle="", alpha=0.6)
    plt.title("Valores Ri en función del índice")
    plt.xlabel("Iteración")
    plt.ylabel("Ri (0-1)")
    plt.grid(True, alpha=0.3)

    # --- Gráfico 2: Histograma de Ni ---
    plt.subplot(1, 2, 2)
    plt.hist(ni, bins=20, color="skyblue", edgecolor="black", alpha=0.7)
    plt.title(f"Histograma de Ni (distribución uniforme)")
    plt.xlabel(f"Valor en el intervalo [{min_value},{max_value}]")
    plt.ylabel("Frecuencia")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    
    # Guardar la figura en un buffer y devolverla como base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

