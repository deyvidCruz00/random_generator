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
        ri = truncar(ext / 10000, 5)
        ni = truncar(a + (b - a) * ri, 5)

        registros.append({
            "i": i,
            "Xi": x_i,
            "Xi^2": x_cuadrado,
            "Extension": int(math.log10(abs(x_cuadrado))) + 1,
            "Extraccion": ext,
            "Ri": ri,
            "Ni": ni
        })
        x_i = ext

    df = pd.DataFrame(registros)
    return df

def extraer_numero(valor_c, valor_d):
    c_str = str(valor_c)

    if valor_d == 8:
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

    extraido = c_str[inicio:inicio + longitud]
    return int(extraido)

def truncar(n, decimales=0):
    factor = 10.0 ** decimales
    return int(n * factor) / factor

# # Ejemplo de uso
# df = generar(2222, 50, a=5, b=15)  # puedes cambiar a y b
# print(df)
