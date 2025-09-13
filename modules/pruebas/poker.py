import json
from collections import Counter

def truncate(num, decimals=5):
    """Trunca un número a 'decimals' decimales"""
    factor = 10 ** decimals
    return int(num * factor) / factor

def poker_test_json(numbers):
    """
    numbers: lista de números pseudoaleatorios
    Retorna un JSON con observados, esperados, chi² y decisión.
    """

    n = len(numbers)

    # Probabilidades teóricas
    probs = {
        "D": 0.3024,   # Todos diferentes
        "O": 0.504,    # Un par
        "T": 0.108,    # Dos pares
        "K": 0.072,    # Tercia
        "F": 0.009,    # Full
        "P": 0.0045,   # Poker
        "Q": 0.0001    # Quintilla
    }

    # Clasificación de cada número
    def classify(num):
        digits = list(str(num).replace("0.", ""))[:5]  # tomamos 5 dígitos
        counts = sorted(Counter(digits).values(), reverse=True)

        if counts == [5]:
            return "Q"  # Quintilla
        elif counts == [4,1]:
            return "P"  # Poker
        elif counts == [3,2]:
            return "F"  # Full
        elif counts == [3,1,1]:
            return "K"  # Tercia
        elif counts == [2,2,1]:
            return "T"  # Dos pares
        elif counts == [2,1,1,1]:
            return "O"  # Un par
        else:
            return "D"  # Todos diferentes

    # Recuento de observados
    observed = {cat: 0 for cat in probs}
    classified = []  # Para guardar clasificación individual
    for num in numbers:
        cat = classify(num)
        observed[cat] += 1
        classified.append({"number": truncate(num), "category": cat})

    # Esperados
    expected = {cat: truncate(n * p) for cat, p in probs.items()}

    # Cálculo de Chi²
    chi2_terms = {cat: truncate(((observed[cat] - expected[cat])**2) / expected[cat]) 
                  for cat in probs if expected[cat] > 0}
    chi2_stat = truncate(sum(chi2_terms.values()))

    # Valor crítico (gl = categorias-1 = 6, alfa=0.05 → 12.59 aprox.)
    chi2_critical = 12.5916

    result = {
        "n": n,
        "observed": observed,
        "expected": expected,
        "chi2_terms": chi2_terms,
        "chi2_stat": chi2_stat,
        "chi2_critical": truncate(chi2_critical),
        "decision": "No se rechaza H0 (pasa la prueba)" if chi2_stat < chi2_critical else "Se rechaza H0 (no pasa la prueba)",
        "classified_numbers": classified
    }

    return json.dumps(result, indent=4)


data = [
    0.12464, 0.61107, 0.56206, 0.79678, 0.06278,
    0.04791, 0.70251, 0.09538, 0.49120, 0.31151,
    0.83612, 0.61222, 0.68150, 0.52925, 0.95868
]

print(poker_test_json(data))

