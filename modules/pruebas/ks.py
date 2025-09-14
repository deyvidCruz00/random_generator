import json
import numpy as np

def truncar(num, decimales=5):
    factor = 10.0 ** decimales
    return int(num * factor) / factor

def kolmogorov_smirnov_test(data, k):
    n = len(data)
    minimo, maximo = min(data), max(data)
    amplitud = (maximo - minimo) / k
    
    # Construcción de intervalos
    intervalos = [(minimo + i * amplitud, minimo + (i+1) * amplitud) for i in range(k)]
    
    # Resultados de intervalos
    intervalos_data = []
    frec_acum = 0 
    frec_esp_acum = 0
    max_diferencia = 0
    
    for i, (ini, fin) in enumerate(intervalos, start=1):
        # Frecuencia observada
        frec = sum(ini < x <= fin if i > 1 else ini <= x <= fin for x in data)
        frec_acum += frec
        
        # Probabilidad observada
        p_obt = frec_acum / n
        
        # Frecuencia esperada acumulada
        frec_esp_acum = round((i / k) * n)
        
        # Probabilidad esperada acumulada
        p_esp = i / k
        
        # Diferencia
        dif = abs(p_obt - p_esp)
        max_diferencia = max(max_diferencia, dif)
        
        intervalos_data.append({
            "No": i,
            "Inicial": truncar(ini, 5),
            "Final": truncar(fin, 5),
            "Frec.Obt": frec,
            "F.Obt.A": frec_acum,
            "P.Obt": round(p_obt, 2),
            "F.Esp.A": frec_esp_acum,
            "P.Esp.A": round(p_esp, 2),
            "Dif": round(dif, 2)
        })
    
    # Estructura del JSON con información de la prueba KS
    resultado = {
        "test_name": "Prueba KS",
        "sample_size": n,
        "intervals": k,
        "range": {
            "minimum": truncar(minimo, 5),
            "maximum": truncar(maximo, 5),
            "amplitude": truncar(amplitud, 5)
        },
        "intervals_data": intervalos_data,
        "statistics": {
            "max_difference": round(max_diferencia, 4),
            "critical_value": "Debe compararse con tabla de valores críticos",
            "decision": "Requiere comparación con valor crítico para α dado"
        }
    }
    
    return json.dumps(resultado, indent=4, ensure_ascii=False)

# Datos de prueba
datos = [
    0.95566, 0.58314, 0.28671, 0.79605, 0.11594,
    0.06598, 0.6813, 0.81999, 0.72519, 0.35326,
    0.66431, 0.5021, 0.41395, 0.14755, 0.18275,
    0.13903, 0.28591, 0.93443, 0.38034, 0.22912,
    0.83146, 0.8996, 0.29869, 0.27757, 0.54731,
    0.99148, 0.64326, 0.41247, 0.92034, 0.50894,
    0.29583, 0.85801, 0.76282, 0.89218, 0.80185,
    0.50215, 0.65604, 0.16559, 0.19552, 0.87442,
    0.62158, 0.13009, 0.44851, 0.76215, 0.33402,
    0.95514, 0.36094, 0.63874, 0.60779, 0.8233
]

resultado_json = kolmogorov_smirnov_test(datos, k=10)
print(resultado_json)