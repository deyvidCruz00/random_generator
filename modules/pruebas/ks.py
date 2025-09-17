import json
import numpy as np

def ks_critical_classic_table(n, alpha):
    """
    Calcula valores críticos usando la fórmula clásica de las tablas KS
    """
    if alpha == 0.20:
        c_alpha = 1.073
    elif alpha == 0.15:
        c_alpha = 1.138
    elif alpha == 0.10:
        c_alpha = 1.224
    elif alpha == 0.05:
        c_alpha = 1.358  # Este es el valor clave
    elif alpha == 0.01:
        c_alpha = 1.628
    elif alpha == 0.005:
        c_alpha = 1.731
    elif alpha == 0.002:
        c_alpha = 1.855
    elif alpha == 0.001:
        c_alpha = 1.950
    else:
        c_alpha = np.sqrt(-0.5 * np.log(alpha/2))
    
    return c_alpha / np.sqrt(n)

def truncar(num, decimales=5):
    factor = 10.0 ** decimales
    return int(num * factor) / factor

def kolmogorov_smirnov_test(data, k=10, alpha=0.05):
    n = len(data)
    
    # ¡CORRECCIÓN CRÍTICA! - Ordenar los datos
    data_sorted = sorted(data)
    
    minimo, maximo = data_sorted[0], data_sorted[-1]
    amplitud = (maximo - minimo) / k
    critical_value = ks_critical_classic_table(n, alpha)

    print(f"Valor crítico KS (tabla clásica) para n={n}, alpha={alpha}: {critical_value}")
    
    # Construcción de intervalos
    intervalos = [(minimo + i * amplitud, minimo + (i+1) * amplitud) for i in range(k)]
    
    # Resultados de intervalos
    intervalos_data = []
    frec_acum = 0 
    max_diferencia = 0
    diferencias = []
    
    for i, (ini, fin) in enumerate(intervalos, start=1):
        # Frecuencia observada - CORREGIDA para usar datos ordenados
        if i == 1:
            # Primer intervalo incluye ambos límites
            frec = sum(ini <= x <= fin for x in data_sorted)
        else:
            # Otros intervalos excluyen límite inferior
            frec = sum(ini < x <= fin for x in data_sorted)
        
        frec_acum += frec
        
        # Probabilidad observada acumulada
        p_obt = frec_acum / n
        
        # Frecuencia esperada acumulada
        frec_esp_acum = (i / k) * n
        
        # Probabilidad esperada acumulada
        p_esp = i / k
        
        # Diferencia
        dif = abs(p_obt - p_esp)
        diferencias.append(dif)
        max_diferencia = max(diferencias)
        
        intervalos_data.append({
            "No": i,
            "Inicial": ini,
            "Final": fin,
            "frecuencia_obt": frec,
            "frecuencia_obt_acu": frec_acum,
            "P_Obt": p_obt,
            "frecuencia_esp_acu": frec_esp_acum,
            "P_Esp_A": p_esp,
            "Dif": dif
        })
    
    # Estructura del JSON con información de la prueba KS
    resultado = {
        "test_name": "Prueba KS",
        "sample_size": n,
        "intervals": k,
        "range": {
            "minimum": minimo,
            "maximum": maximo,
            "amplitude": amplitud,
        },
        "intervals_data": intervalos_data,
        "statistics": {
            "max_difference": max_diferencia, 
            "critical_value": critical_value
        },
        "decision": "pasa la prueba" if max_diferencia <= critical_value else "no pasa la prueba"
    }
    
    return json.dumps(resultado, indent=4, ensure_ascii=False)

# Ejemplo de uso con tus datos
if __name__ == "__main__":
    datos_str = "0,65516114 0,53701667 0,05697293 0,51775919 0,71467019 0,08172166 0,89613258 0,54189652 0,40455124 0,01066283 0,87110388 0,3281254 0,45500566 0,01730704 0,21659212 0,64103245 0,03743258 0,95634111 0,26592891 0,52502441 0,10911019 0,13742832 0,74915092 0,91857336 0,13611925 0,00660023 0,85685072 0,07533873 0,48251404 0,83777623 0,52223382 0,24647604 0,16622532 0,87189949 0,91607754 0,65321761 0,31097361 0,54335514 0,29750588 0,45247067 0,270814 0,41232463 0,93488253 0,19651657 0,40469919 0,62746595 0,00934499 0,11210389 0,95380576 0,61504508"
    data = [float(x.replace(',', '.')) for x in datos_str.split()]
    
    print(f"Total de datos: {len(data)}")
    print(f"Datos ordenados (primeros 5): {sorted(data)[:5]}")
    print(f"Datos ordenados (últimos 5): {sorted(data)[-5:]}")
    print()
    
    resultado = kolmogorov_smirnov_test(data)
    print(resultado)