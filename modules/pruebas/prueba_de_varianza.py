import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy import stats

def prueba_de_varianza(datos, alpha=0.05, mu_esperada=0.5):
    # Convertir a array
    datos = np.array(datos)
    n = len(datos)

    #varianza muestral
    varianza = np.var(datos, ddof=1) 

    # Valor crítico Z
    z = norm.ppf(1 - alpha/2)

    #Valor crítico Chi-cuadrado
    Xi1 =  stats.chi2.ppf(alpha/2, n-1)
    Xi2 =  stats.chi2.ppf(z, n-1)

    #Intervalo de confianza    
    li = Xi1/(12*(n-1))
    ls = Xi2/(12*(n-1))

    # Decisión
    if li <= varianza <= ls:
        decision = "Paso la prueba de varianza."
    else:
        decision = "No paso la prueba de varianza."

        
    return {
        "decision": decision
    }


np.random.seed(42)
datos = np.random.uniform(0,1,50)

resultado = prueba_de_varianza(datos, alpha=0.05)

print(datos)