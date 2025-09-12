import numpy as np
import pandas as pd

def generar(x_o, k, c, g, n, a_intervalo=0, b_intervalo=10):
    registros = []
    a = 1 + 2 * k
    x_a = x_o
    m = 2 ** g

    for i in range(n):
        x_i = np.mod(((a * x_a) + c), m)
        x_a = x_i
        r_i = truncar(x_i / m, 5)
        ni = truncar(a_intervalo + (b_intervalo - a_intervalo) * r_i, 5)

        registros.append({
            "i": i,
            "Xi": int(x_i),
            "a": a,
            "c": c,
            "m": m,
            "Ri": r_i,
            "Ni": ni
        })

    df = pd.DataFrame(registros)
    return df

def truncar(n, decimales=0):
    factor = 10.0 ** decimales
    return int(n * factor) / factor
# Ejemplo de uso
# x_o = 123456
# k = 7
# c = 9
# g = 20
# df = generar(x_o, k, c, g, 1000, a_intervalo=5, b_intervalo=15)
# print(df)