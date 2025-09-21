import numpy as np
import scipy.stats as stats
import json
from scipy.stats import chi2

def prueba_chi_cuadrado(datos, k=8, alpha=0.05):
    """
    Test Chi-cuadrado para verificar si los datos siguen una distribución uniforme
    
    Parámetros:
    - datos: lista o array de números pseudoaleatorios
    - k: número de intervalos para dividir los datos
    - alpha: nivel de significancia (default: 0.05)
    """
    n = len(datos)
    datos = np.array(datos)  # Convierte a array de NumPy para facilitar cálculos

    # PASO 1: Definir el rango y crear intervalos
    minimo, maximo = np.min(datos), np.max(datos)
    # Crea k+1 puntos para definir k intervalos iguales
    intervalos = np.linspace(minimo, maximo, k+1)
    
    # PASO 2: Contar frecuencias observadas en cada intervalo
    # np.histogram cuenta cuántos datos caen en cada intervalo
    frecuencias_obs, _ = np.histogram(datos, bins=intervalos)
    
    # PASO 3: Calcular frecuencia esperada
    # Si los datos son uniformes, cada intervalo debería tener n/k datos
    freq_esp = n / k
    
    # PASO 4: Calcular chi-cuadrado por intervalo
    # Chi² = (Observado - Esperado)² / Esperado
    chi2_vals = ((frecuencias_obs - freq_esp) ** 2) / freq_esp
    
    # PASO 5: Sumar para obtener estadístico chi-cuadrado total
    chi2_total = np.sum(chi2_vals)
    
    # PASO 6: Obtener valor crítico de la tabla chi-cuadrado
    # Grados de libertad = k - 1, pero aquí usa 7 (¿debería ser k-1?)
    chi2_critico = chi2.ppf(1 - alpha, 7)  # POSIBLE ERROR: debería ser k-1
    
    # PASO 7: Decisión estadística
    # Si chi2_total <= chi2_crítico, los datos siguen distribución uniforme
    pasa_prueba = chi2_total <= chi2_critico
    
    # PASO 8: Estructurar resultado como JSON
    resultado = {
        "test_name": "Prueba Chi-Cuadrado",
        "intervals": k,
        "n": n,
        "range": {
            "minimum": minimo,
            "maximum": maximo
        },
        "intervals_data": [],  # Se llenará con detalles de cada intervalo
        "statistics": {
            "frecuencia_obt_total": int(np.sum(frecuencias_obs)),  # Suma de observados (= n)
            "frecuencia_esp_total": int(freq_esp * k),             # Suma de esperados (= n)
            "chi2_total": chi2_total,                              # Estadístico chi-cuadrado
            "chi2_critico": chi2_critico,                          # Valor crítico de tabla
        },
        "decision": "Pasa la prueba chi-cuadrado." if pasa_prueba else "No pasa la prueba chi-cuadrado.",
        "isApproved": str(pasa_prueba)
    }

    # PASO 9: Llenar detalles de cada intervalo
    for i in range(k):
        resultado["intervals_data"].append({
            "no": i+1,                                    # Número del intervalo
            "inicio": float(intervalos[i]),     # Límite inferior
            "fin": float(intervalos[i+1]),      # Límite superior
            "frecuencia_obt": int(frecuencias_obs[i]),    # Datos observados en este intervalo
            "frecuencia_esp": float(freq_esp),  # Datos esperados (n/k)
            "chi2": float(chi2_vals[i])         # Contribución chi² de este intervalo
        })

    return json.dumps(resultado, ensure_ascii=False, indent=2)

"""
¿QUÉ HACE ESTE TEST?

El test Chi-cuadrado verifica si un conjunto de datos sigue una distribución uniforme,
dividiendo los datos en intervalos y comparando las frecuencias observadas vs esperadas.

FUNCIONAMIENTO:
1. Divide el rango de datos en k intervalos iguales
2. Cuenta cuántos datos caen en cada intervalo (frecuencia observada)
3. Calcula cuántos datos deberían caer en cada intervalo si fueran uniformes (frecuencia esperada = n/k)
4. Para cada intervalo, calcula: (Observado - Esperado)² / Esperado
5. Suma todos estos valores para obtener el estadístico chi-cuadrado
6. Compara con el valor crítico de la tabla

EJEMPLO:
- Si tienes 100 datos y 10 intervalos, cada intervalo debería tener ~10 datos
- Si un intervalo tiene 15 datos: chi² = (15-10)²/10 = 2.5
- Si otro tiene 5 datos: chi² = (5-10)²/10 = 2.5
- Si las diferencias son grandes, chi² total será alto → rechaza uniformidad

¡POSIBLE BUG!: 
La línea "chi2.ppf(1 - alpha, 7)" usa 7 grados de libertad fijos,
pero debería usar (k-1) grados de libertad.

PROPÓSITO: Verificar si un generador de números aleatorios produce
una distribución uniforme (todos los valores tienen igual probabilidad).
"""