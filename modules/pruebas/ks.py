import json
import numpy as np

def ks_critical_classic_table(n, alpha):
    """
    Obtiene el valor crítico de la tabla de Kolmogorov-Smirnov
    según el nivel de significancia (alpha) y tamaño de muestra (n)
    """
    # Valores críticos estándar para diferentes niveles de confianza
    if alpha == 0.20:
        c_alpha = 1.073
    elif alpha == 0.15:
        c_alpha = 1.138
    elif alpha == 0.10:
        c_alpha = 1.224
    elif alpha == 0.05:
        c_alpha = 1.358  # Más común (95% de confianza)
    elif alpha == 0.01:
        c_alpha = 1.628
    elif alpha == 0.005:
        c_alpha = 1.731
    elif alpha == 0.002:
        c_alpha = 1.855
    elif alpha == 0.001:
        c_alpha = 1.950
    else:
        # Fórmula aproximada para otros valores de alpha
        c_alpha = np.sqrt(-0.5 * np.log(alpha/2))
    
    # El valor crítico final se ajusta por el tamaño de muestra
    return c_alpha / np.sqrt(n)

def kolmogorov_smirnov_test(data, k=10, alpha=0.05):
    """
    Prueba de Kolmogorov-Smirnov para verificar si los datos siguen
    una distribución uniforme (común en pruebas de aleatoriedad)
    
    Parámetros:
    - data: lista de números a analizar
    - k: número de intervalos para dividir los datos
    - alpha: nivel de significancia
    """
    n = len(data)
    
    # PASO 1: Ordenar los datos (crucial para el análisis correcto)
    data_sorted = sorted(data)
    
    # PASO 2: Calcular el rango y dividir en k intervalos iguales
    minimo, maximo = data_sorted[0], data_sorted[-1]
    amplitud = (maximo - minimo) / k  # Ancho de cada intervalo
    
    # PASO 3: Obtener valor crítico de las tablas KS
    critical_value = ks_critical_classic_table(n, alpha)
    print(f"Valor crítico KS para n={n}, alpha={alpha}: {critical_value}")
    
    # PASO 4: Crear los k intervalos
    intervalos = [(minimo + i * amplitud, minimo + (i+1) * amplitud) for i in range(k)]
    
    # PASO 5: Analizar cada intervalo
    intervalos_data = []
    frec_acum = 0  # Frecuencia acumulada observada
    max_diferencia = 0
    diferencias = []
    
    for i, (ini, fin) in enumerate(intervalos, start=1):
        # Contar datos en este intervalo
        if i == 1:
            # Primer intervalo incluye ambos límites [ini, fin]
            frec = sum(ini <= x <= fin for x in data_sorted)
        else:
            # Otros intervalos excluyen límite inferior (ini, fin]
            frec = sum(ini < x <= fin for x in data_sorted)
        
        frec_acum += frec
        
        # Probabilidad observada acumulada
        p_obt = frec_acum / n
        
        # Frecuencia esperada (distribución uniforme)
        frec_esp_acum = (i / k) * n
        
        # Probabilidad esperada acumulada
        p_esp = i / k
        
        # Diferencia entre lo observado y lo esperado
        dif = abs(p_obt - p_esp)
        diferencias.append(dif)
        max_diferencia = max(diferencias)  # Estadístico KS = máxima diferencia
        
        # Guardar resultados del intervalo
        intervalos_data.append({
            "No": i,
            "Inicial": ini,
            "Final": fin,
            "frecuencia_obt": frec,           # Datos en este intervalo
            "frecuencia_obt_acu": frec_acum,  # Datos acumulados hasta aquí
            "P_Obt": p_obt,                   # Proporción observada acumulada
            "frecuencia_esp_acu": frec_esp_acum,  # Frecuencia esperada acumulada
            "P_Esp_A": p_esp,                 # Proporción esperada acumulada
            "Dif": dif                        # |Observado - Esperado|
        })
    
    # PASO 6: Decisión estadística
    # Si max_diferencia <= critical_value, los datos siguen distribución uniforme
    pasa_prueba = max_diferencia <= critical_value
    
    # PASO 7: Estructurar resultado como JSON
    resultado = {
        "test_name": "Prueba KS",
        "sample_size": n,
        "intervals": k,
        "range": {
            "minimum": minimo,
            "maximum": maximo,
            "amplitude": amplitud,
        },
        "intervals_data": intervalos_data,  # Detalles de cada intervalo
        "statistics": {
            "max_difference": max_diferencia,   # Estadístico KS
            "critical_value": critical_value    # Valor de la tabla
        },
        "decision": "Pasa la prueba de ks." if pasa_prueba else "No pasa la prueba de ks.",
        "isApproved": str(pasa_prueba)
    }
    
    return json.dumps(resultado, indent=4, ensure_ascii=False)

"""
RESUMEN DEL FUNCIONAMIENTO:
1. Ordena los datos y los divide en k intervalos iguales
2. Para cada intervalo, cuenta cuántos datos caen en él
3. Compara la distribución observada vs la esperada (uniforme)
4. Calcula la máxima diferencia entre ambas distribuciones
5. Si esta diferencia es menor al valor crítico, los datos pasan la prueba
6. Retorna un JSON con todos los detalles del análisis

PROPÓSITO: Verificar si un conjunto de números sigue una distribución uniforme
(útil para validar generadores de números aleatorios)
"""