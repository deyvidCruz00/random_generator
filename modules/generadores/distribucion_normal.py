import math
import pandas as pd
from modules.generadores.congruencia_lineal import generar as generar_cl

def distribucion_normal(std_dev, num_samples, mean, semilla, k, c, g, a=0, b=1):
    # Usa el generador congruencial lineal para obtener 2*num_samples números uniformes
    df_uniformes = generar_cl(semilla, k, c, g, num_samples * 2, a, b)
    uniformes = df_uniformes["Ri"].tolist()

    registros = []
    for i in range(num_samples):
        u = uniformes[2*i]
        v = uniformes[2*i + 1]
        x = math.sqrt(-2.0 * math.log(u)) * math.cos(2.0 * math.pi * v)
        ri = x * std_dev
        ni = mean + x * std_dev
        registros.append({
            "i": i,
            "Ri": ri,
            "Ni": ni
        })
    df = pd.DataFrame(registros)
    return df

# Ejemplo de uso:
# std_dev = 1.0
# num_samples = 10
# mean = 0.0
# semilla, k, c, g = 5, 3, 7, 16
# df = distribucion_normal(std_dev, num_samples, mean, semilla, k, c, g)
# print(df)