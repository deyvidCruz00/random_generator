import json
from collections import Counter
import scipy.stats as stats

def poker_test_json(datos, alpha=0.05):
    """
    Test de Poker: verifica aleatoriedad analizando patrones de dígitos
    en números pseudoaleatorios (como patrones de cartas en poker)
    
    Parámetros:
    - datos: lista de números pseudoaleatorios a analizar
    - alpha: nivel de significancia (default: 0.05)
    """
    n = len(datos)

    # Probabilidades teóricas para cada patrón (basadas en teoría combinatoria)
    probs = {
        "D": 0.3024,   # Todos diferentes (ej: 12345)
        "O": 0.504,    # Un par (ej: 11234)
        "T": 0.108,    # Dos pares (ej: 11223)
        "K": 0.072,    # Tercia (ej: 11123)
        "F": 0.009,    # Full - tercia + par (ej: 11122)
        "P": 0.0045,   # Poker - cuádrupla (ej: 11112)
        "Q": 0.0001    # Quintilla - todos iguales (ej: 11111)
    }

    def classify(num):
        """
        Clasifica un número según el patrón de sus dígitos
        Toma los primeros 5 dígitos después del punto decimal
        """
        # Extrae 5 dígitos del número (quita "0." del inicio)
        digits = list(str(num).replace("0.", ""))[:5]
        
        # Cuenta cuántas veces aparece cada dígito
        counts = sorted(Counter(digits).values(), reverse=True)
        
        # Clasifica según el patrón de repeticiones
        if counts == [5]:           # Todos iguales: 11111
            return "Q"  # Quintilla
        elif counts == [4,1]:       # Cuatro iguales: 11112
            return "P"  # Poker
        elif counts == [3,2]:       # Tres + dos: 11122
            return "F"  # Full
        elif counts == [3,1,1]:     # Tres iguales: 11123
            return "K"  # Tercia
        elif counts == [2,2,1]:     # Dos pares: 11223
            return "T"  # Dos pares
        elif counts == [2,1,1,1]:   # Un par: 11234
            return "O"  # Un par
        else:                       # Todos diferentes: 12345
            return "D"  # Todos diferentes

    # PASO 1: Clasificar cada número según su patrón
    observed = {cat: 0 for cat in probs}  # Contador de observaciones
    for num in datos:
        cat = classify(num)
        observed[cat] += 1

    # PASO 2: Calcular frecuencias esperadas
    expected = {cat: n * p for cat, p in probs.items()}

    # PASO 3: Preparar datos para la prueba chi-cuadrado
    categories_data = []
    suma_oi = 0      # Suma de observados (debe ser = n)
    suma_chi2 = 0    # Estadístico chi-cuadrado
    
    for cat in ["D", "O", "T", "K", "F", "P", "Q"]:
        oi = observed[cat]     # Frecuencia observada
        prob = probs[cat]      # Probabilidad teórica
        ei = expected[cat]     # Frecuencia esperada
        
        # Componente chi-cuadrado: (Observado - Esperado)² / Esperado
        chi2_component = ((oi - ei)**2) / ei if ei > 0 else 0
        
        categories_data.append({
            "Cat": cat,                    # Categoría (D, O, T, K, F, P, Q)
            "Oi": oi,                      # Observados
            "Prob": prob,                  # Probabilidad teórica
            "Ei": ei,                      # Esperados
            "(Oi-Ei)^2/Ei": chi2_component # Contribución al chi-cuadrado
        })
        
        suma_oi += oi
        suma_chi2 += chi2_component

    # PASO 4: Obtener valor crítico de chi-cuadrado
    # gl = grados de libertad = categorías - 1 = 7 - 1 = 6
    chi2_critical = stats.chi2.ppf(1 - alpha, 6)

    # PASO 5: Decisión estadística
    # Si chi2_calculado <= chi2_crítico, los datos pasan la prueba
    pasa_prueba = suma_chi2 <= chi2_critical

    # PASO 6: Estructurar resultado
    result = {
        "test_name": "Prueba de Poker",
        "intervals_data": categories_data,     # Detalles por categoría
        "statistics": {
            "Suma_Oi": suma_oi,               # Total observado (= n)
            "Chi2_calculado": suma_chi2,       # Estadístico chi-cuadrado
            "critical_value": chi2_critical    # Valor crítico de tabla
        },      
        "decision": "Pasa la prueba de poker." if pasa_prueba else "No pasa la prueba de poker.",
        "isApproved": str(pasa_prueba)
    }

    return json.dumps(result, indent=4, ensure_ascii=False)

"""
¿QUÉ HACE ESTE TEST?

El test de Poker analiza si los dígitos de números pseudoaleatorios
aparecen con patrones similares a las manos de poker.

LÓGICA:
1. Toma los primeros 5 dígitos de cada número
2. Clasifica cada número según el patrón de repetición de dígitos
3. Compara las frecuencias observadas vs las esperadas teóricamente
4. Usa chi-cuadrado para determinar si las diferencias son significativas

EJEMPLO:
- Número: 0.12345 → Dígitos: [1,2,3,4,5] → Patrón: "D" (todos diferentes)
- Número: 0.11234 → Dígitos: [1,1,2,3,4] → Patrón: "O" (un par)
- Número: 0.11122 → Dígitos: [1,1,1,2,2] → Patrón: "F" (full)

PROPÓSITO: Detectar si un generador produce patrones no aleatorios
en la secuencia de dígitos de sus números.
"""