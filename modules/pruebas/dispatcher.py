from modules.pruebas.prueba_de_medias import prueba_de_medias
from modules.pruebas.prueba_de_varianza import prueba_de_varianza
from modules.pruebas.prueba_chi2_2 import prueba_chi_cuadrado
from modules.pruebas.ks import kolmogorov_smirnov_test
from modules.pruebas.poker import poker_test_json
##from modules.pruebas.prueba_rachas import prueba_rachas

PRUEBAS_DISPONIBLES = {
    "medias": prueba_de_medias,
    "varianza": prueba_de_varianza,
    "chi": prueba_chi_cuadrado,
    "kolmogorov": kolmogorov_smirnov_test,
    "poker": poker_test_json,
}

def ejecutar_pruebas(datos, pruebas, alpha):
    resultados = {}
    for nombre, seleccionada in pruebas.items():
        if nombre == "kolmogorov" and seleccionada and nombre in PRUEBAS_DISPONIBLES:
            resultados[nombre] = PRUEBAS_DISPONIBLES[nombre](datos, alpha=alpha)
        elif nombre == "poker" and seleccionada and nombre in PRUEBAS_DISPONIBLES:
            resultados[nombre] = PRUEBAS_DISPONIBLES[nombre](datos) 
        elif seleccionada and nombre in PRUEBAS_DISPONIBLES:
            resultados[nombre] = PRUEBAS_DISPONIBLES[nombre](datos, alpha=alpha)
    return resultados
