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
        r_i = truncar(x_i / m, 5)

        registros.append({
            "i": i+1,
            "Xi": int(x_i),
            "Ri": r_i
        })

    df = pd.DataFrame(registros)
    return df

def truncar(n, decimales=0):
    factor = 10.0 ** decimales
    return int(n * factor) / factor