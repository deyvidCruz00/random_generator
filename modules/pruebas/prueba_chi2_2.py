import numpy as np
import scipy.stats as stats
import json

def prueba_chi_cuadrado(datos, k, alpha=0.05):
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
        "test_name": "chi-cuadrado",
        "sample_size": n,
        "intervals": k,
        "significance_level": alpha,
        "degrees_freedom": k-1,
        "range": {
            "minimum": round(float(minimo), 8),
            "maximum": round(float(maximo), 8)
        },
        "intervalos": [],
        "totales": {
            "frecuencia_obt_total": int(np.sum(frecuencias_obs)),
            "frecuencia_esp_total": int(freq_esp * k),
            "chi2_total": round(float(chi2_total), 4),
            "chi2_critico": round(float(chi2_critico), 4),
            "pasa_prueba": bool(chi2_total < chi2_critico)
        },
        "decision": "No se rechaza H0 (pasa la prueba)" if chi2_total < chi2_critico else "Se rechaza H0 (no pasa la prueba)"
    }

    for i in range(k):
        resultado["intervalos"].append({
            "no": i+1,
            "inicio": round(float(intervalos[i]), 8),
            "fin": round(float(intervalos[i+1]), 8),
            "frecuencia_obt": int(frecuencias_obs[i]),
            "frecuencia_esp": round(float(freq_esp), 3),
            "chi2": round(float(chi2_vals[i]), 3)
        })

    return json.dumps(resultado, ensure_ascii=False, indent=2)

# ==============================
# Ejemplo de uso:
# ==============================

datos = [0.08936784,0.20157843,0.31378902,0.42599961,0.53821019,
         0.65042078,0.76263137,0.87484196,0.98705254,0.20157843,
         0.31378902,0.87484196,0.20157843,0.42599961,0.87484196]

resultado = prueba_chi_cuadrado(datos, k=8, alpha=0.05)

print(resultado)