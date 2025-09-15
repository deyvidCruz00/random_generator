import json
import numpy as np

def ks_critical_classic_table(n, alpha):
    """
    Calcula valores críticos usando la fórmula clásica de las tablas KS
    Esta es la fórmula que se usa en las tablas impresas tradicionales
    """
    # Valores críticos aproximados para diferentes alfas
    # Estos son los multiplicadores estándar de las tablas KS
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
        # Aproximación general
        c_alpha = np.sqrt(-0.5 * np.log(alpha/2))
    
    # Fórmula clásica: D_crítico = c_alpha / sqrt(n)
    return c_alpha / np.sqrt(n)

def truncar(num, decimales=5):
    factor = 10.0 ** decimales
    return int(num * factor) / factor

def kolmogorov_smirnov_test(data, k=10, alpha=0.05):
    n = len(data)
    minimo, maximo = min(data), max(data)
    amplitud = (maximo - minimo) / k
    critical_value = truncar(ks_critical_classic_table(n, alpha),3)

    print(f"Valor crítico KS (tabla clásica) para n={n}, alpha={alpha}: {critical_value}")
    
    # Construcción de intervalos
    intervalos = [(minimo + i * amplitud, minimo + (i+1) * amplitud) for i in range(k)]
    
    # Resultados de intervalos
    intervalos_data = []
    frec_acum = 0 
    frec_esp_acum = 0
    max_diferencia = 0

    diferencias = []
    
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
        diferencias.append(dif)
        max_diferencia = max(diferencias)
        
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
        "intervals": k,
        "range": {
            "minimum": truncar(minimo, 5),
            "maximum": truncar(maximo, 5),
            "amplitude": truncar(amplitud, 5)
        },
        "intervals_data": intervalos_data,
        "statistics": {
            "max_difference": round(max_diferencia, 4),
            "critical_value": critical_value,
            "decision": "pasa la prueba" if max_diferencia <= critical_value else "no pasa la prueba"
        }
    }
    
    return json.dumps(resultado, indent=4, ensure_ascii=False)
