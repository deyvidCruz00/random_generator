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
    
    Retorna: JSON string con los resultados del test
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

    def extract_digits(num):
        """Extrae exactamente 5 dígitos después del punto decimal"""
        str_num = str(num)
        if '.' in str_num:
            decimal_part = str_num.split('.')[1]
        else:
            decimal_part = ""
        
        # Asegurar exactamente 5 dígitos
        if len(decimal_part) < 5:
            decimal_part = decimal_part.ljust(5, '0')
        else:
            decimal_part = decimal_part[:5]
            
        return list(decimal_part)

    def classify(num):
        """Clasifica un número según el patrón de sus dígitos"""
        digits = extract_digits(num)
        counts = sorted(Counter(digits).values(), reverse=True)
        
        if counts == [5]:           return "Q"  # Quintilla
        elif counts == [4, 1]:      return "P"  # Poker
        elif counts == [3, 2]:      return "F"  # Full
        elif counts == [3, 1, 1]:   return "K"  # Tercia
        elif counts == [2, 2, 1]:   return "T"  # Dos pares
        elif counts == [2, 1, 1, 1]: return "O"  # Un par
        else:                       return "D"  # Todos diferentes

    # Clasificar cada número según su patrón
    observed = {cat: 0 for cat in probs}
    for num in datos:
        cat = classify(num)
        observed[cat] += 1

    # Calcular frecuencias esperadas
    expected = {cat: n * p for cat, p in probs.items()}

    # Preparar datos para la prueba chi-cuadrado
    categories_data = []
    suma_oi = 0
    suma_chi2 = 0
    
    descriptions = {
        "D": "Todos diferentes", "O": "Un par", "T": "Dos pares", 
        "K": "Tercia", "F": "Full House", "P": "Poker", "Q": "Quintilla"
    }
    
    for cat in ["D", "O", "T", "K", "F", "P", "Q"]:
        oi = observed[cat]
        prob = probs[cat]
        ei = expected[cat]
        chi2_component = ((oi - ei)**2) / ei if ei > 0 else 0
        
        categories_data.append({
            "Cat": cat,
            "Descripcion": descriptions[cat],
            "Oi": oi,
            "Prob": round(prob, 4),
            "Ei": round(ei, 4),
            "(Oi-Ei)^2/Ei": round(chi2_component, 6)
        })
        
        suma_oi += oi
        suma_chi2 += chi2_component

    # Obtener valor crítico y p-value
    gl = len(probs) - 1
    chi2_critical = stats.chi2.ppf(1 - alpha, gl)
    pasa_prueba = suma_chi2 <= chi2_critical

    # Estructurar resultado
    result = {
        "test_name": "Prueba de Poker",
  
        "intervals_data": categories_data,
        "statistics": {
            "Suma_Oi": suma_oi,
            "Chi2_calculado": suma_chi2,
            "critical_value": chi2_critical 
        },      
        "decision": "Pasa la prueba de poker" if pasa_prueba else "No pasa la prueba de poker", 
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