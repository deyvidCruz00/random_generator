import numpy as np
import pandas as pd

def generar(x_o, k, c, g, n):
    registros = []
    a = 1 + 2 * k
    x_a = x_o
    m = 2 ** g

    for i in range(n):
        x_i = np.mod(((a * x_a) + c), m)
        x_a = x_i
        r_i = truncar_decimales_inteligente(x_i / m)

        registros.append({
            "i": i+1,
            "Xi": int(x_i),
            "Ri": r_i
        })

    df = pd.DataFrame(registros)
    return df

def truncar_decimales_inteligente(numero):
    
    # Truncar a 5 decimales máximo usando truncamiento, no redondeo
    factor = 10.0 ** 5
    truncado = int(numero * factor) / factor
    
    # Convertir a string para eliminar ceros trailing
    resultado_str = f"{truncado:.5f}".rstrip('0').rstrip('.')
    
    # Si queda vacío después del punto, agregar un 0
    if resultado_str.endswith('.'):
        resultado_str = resultado_str[:-1]
    
    # Convertir de vuelta a float
    return float(resultado_str)

def graficar_serie_temporal(ri_values, parametros_info="", titulo_adicional=""):
    """
    Genera un gráfico de serie temporal de los valores Ri generados por congruencia lineal.
    
    Args:
        ri_values: Lista de valores Ri
        parametros_info: Información de parámetros (x0, k, c, g)
        titulo_adicional: Información adicional para el título
    
    Returns:
        String con el gráfico codificado en base64
    """
    import matplotlib.pyplot as plt
    import io
    import base64
    
    # Configurar el gráfico
    plt.figure(figsize=(12, 6))
    
    # Crear índices (1, 2, 3, ...)
    indices = list(range(1, len(ri_values) + 1))
    
    # Gráfico de líneas con puntos
    plt.plot(indices, ri_values, 'g-o', linewidth=1.5, markersize=3, alpha=0.7)
    
    # Personalización
    plt.title(f'Serie Temporal - Congruencia Lineal\n{parametros_info}\n{titulo_adicional}', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Índice (i)', fontsize=12)
    plt.ylabel('Valores Ri', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Ajustar límites del eje Y
    plt.ylim(0, 1)
    
    # Estadísticas básicas en el gráfico
    mean_val = sum(ri_values) / len(ri_values)
    plt.axhline(y=mean_val, color='red', linestyle='--', alpha=0.7, label=f'Media: {mean_val:.4f}')
    plt.axhline(y=0.5, color='green', linestyle='--', alpha=0.5, label='Valor esperado: 0.5')
    
    plt.legend()
    plt.tight_layout()
    
    # Convertir a base64
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url