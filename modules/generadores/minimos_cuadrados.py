import math
import pandas as pd

def generar(seed, amount, a=0, b=10):
    registros = []
    x_i = seed
    for i in range(amount):
        x_cuadrado = x_i ** 2
        ext = extraer_numero(x_cuadrado, int(math.log10(abs(x_cuadrado))) + 1)
        if ext is None:
            break  # No se puede extraer, termina la secuencia
        
        ri = truncar_decimales_inteligente(ext / 10000)
        
        registros.append({
            "i": i,
            "Xi": x_i,
            "Xi^2": x_cuadrado,
            "Extension": int(math.log10(abs(x_cuadrado))) + 1,
            "Extraccion": ext,
            "Ri": ri
            # "Ni": ni
        })
        x_i = ext

    df = pd.DataFrame(registros)
    return df

def extraer_numero(valor_c, valor_d):
    c_str = str(valor_c)

    if valor_d == 12:
        inicio, longitud = 4, 4
    elif valor_d == 11:
        inicio, longitud = 3, 4
    elif valor_d == 10:
        inicio, longitud = 3, 4
    elif valor_d == 9:
        inicio, longitud = 2, 4
    elif valor_d == 8:
        inicio, longitud = 2, 4
    elif valor_d == 7:
        inicio, longitud = 1, 4
    elif valor_d == 6:
        inicio, longitud = 0, 4
    elif valor_d == 5:
        inicio, longitud = 0, 3
    elif valor_d == 4:
        inicio, longitud = 0, 2
    elif valor_d == 3:
        inicio, longitud = 0, 1
    else:
        return None  

    # Verificar que la extracción no se salga de los límites
    if inicio + longitud > len(c_str):
        # Ajustar la longitud si es necesario
        longitud = len(c_str) - inicio
        if longitud <= 0:
            return None
    
    extraido = c_str[inicio:inicio + longitud]
    return int(extraido)

def truncar(n, decimales=0):
    factor = 10.0 ** decimales
    return int(n * factor) / factor

def truncar_decimales_inteligente(numero):
    """
    Trunca a máximo 5 decimales, pero elimina ceros innecesarios al final.
    Ejemplos:
    - 0.51100 -> 0.511
    - 0.50000 -> 0.5
    - 0.12345 -> 0.12345
    """
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

def graficar_serie_temporal(ri_values, metodo="Cuadrados Medios", titulo_adicional=""):
    """
    Genera un gráfico de serie temporal de los valores Ri generados.
    
    Args:
        ri_values: Lista de valores Ri
        metodo: Nombre del método generador
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
    plt.plot(indices, ri_values, 'b-o', linewidth=1.5, markersize=3, alpha=0.7)
    
    # Personalización
    plt.title(f'Serie Temporal - {metodo}\n{titulo_adicional}', fontsize=14, fontweight='bold')
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

# # Ejemplo de uso
# df = generar(2222, 50, a=5, b=15)  # puedes cambiar a y b
# print(df)
