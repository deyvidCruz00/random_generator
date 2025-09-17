import numpy as np
import scipy.stats as stats
import json

def truncar(num, decimales=5):
    factor = 10.0 ** decimales
    return int(num * factor) / factor

def prueba_chi_cuadrado(datos, k=8, alpha=0.05):
    """
    Prueba Chi-cuadrado de uniformidad
    datos: lista o array de números pseudoaleatorios
    k: número de intervalos
    alpha: nivel de significancia
    """
    n = len(datos)
    datos = np.array(datos)

    # Usar el rango real de los datos
    minimo, maximo = np.min(datos), np.max(datos)
    intervalos = np.linspace(minimo, maximo, k+1)
    
    # Frecuencias observadas
    frecuencias_obs, _ = np.histogram(datos, bins=intervalos)
    
    # Frecuencia esperada
    freq_esp = n / k
    
    # Chi2 por intervalo
    chi2_vals = ((frecuencias_obs - freq_esp) ** 2) / freq_esp
    
    # Chi2 total
    chi2_total = np.sum(chi2_vals)
    
    # Valor crítico
    chi2_critico = stats.chi2.ppf(1 - alpha, df=k-1)
    
    # Construcción de la respuesta en formato JSON
    resultado = {
        "test_name": "Prueba Chi-Cuadrado",
        "intervals": k,
        "n": n,
        "range": {
            "minimum": truncar(minimo, 5),
            "maximum": truncar(maximo, 5)
        },
        "intervals_data": [],
        "statistics": {
            "frecuencia_obt_total": int(np.sum(frecuencias_obs)),
            "frecuencia_esp_total": int(freq_esp * k),
            "chi2_total": truncar(chi2_total, 5),
            "chi2_critico": truncar(chi2_critico, 5),
        },
        "decision": "No se rechaza H0 (pasa la prueba)" if chi2_total < chi2_critico else "Se rechaza H0 (no pasa la prueba)"
    }

    for i in range(k):
        resultado["intervals_data"].append({
            "no": i+1,
            "inicio": round(float(intervalos[i]), 8),
            "fin": round(float(intervalos[i+1]), 8),
            "frecuencia_obt": int(frecuencias_obs[i]),
            "frecuencia_esp": round(float(freq_esp), 3),
            "chi2": round(float(chi2_vals[i]), 3)
        })

    return json.dumps(resultado, ensure_ascii=False, indent=2)