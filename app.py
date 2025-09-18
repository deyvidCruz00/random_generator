from flask import Flask, request, jsonify, render_template, send_file
from modules.pruebas.dispatcher import ejecutar_pruebas
from modules.generadores.minimos_cuadrados import generar as generar_mc
from modules.generadores.congruencia_lineal import generar as generar_cl
from modules.generadores.congruencia_multi import generar as generar_cm
from modules.generadores.distribucion_normal import distribucion_normal_inversa, graficar_distribucion_normal
from modules.generadores.distribucion_uniforme import distribucion_uniforme, graficar_distribucion_uniforme
#from modules.pruebas import media as prueba_media_mod

import pandas as pd
import json
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import base64
import io

# Variables globales para almacenar los Ri generados
ri_cuadrados = []
ri_lineal = []
ri_multiplicativo = []

# Variable global para rastrear el último método de generación usado
ultimo_metodo_generacion = None

app = Flask(__name__)

@app.route("/pruebas")
def pruebas():
    return render_template("pruebas.html")

@app.route("/evaluar", methods=["POST"])
def api_pruebas():
    data = request.get_json()
    datos = data.get("numeros", [])
    pruebas = data.get("pruebasSeleccionadas", {})
    alpha = data.get("alpha", 0.05)

    resultados = ejecutar_pruebas(datos, pruebas, alpha)
    return jsonify(resultados)

@app.route("/resultados")
def resultados():
    return render_template("results.html")


# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Cuadrados medios
@app.route("/cuadrados", methods=["GET", "POST"])
def cuadrados():
    data = None
    semilla = ""
    n = ""
    min_val = ""
    max_val = ""

    if request.method == "POST":
        semilla = request.form["semilla"]
        n = request.form["iteraciones"]
        # min_val = request.form["min"]
        # max_val = request.form["max"]

        #df = generar_mc(int(semilla), int(float(n)), float(min_val), float(max_val))
        df = generar_mc(int(semilla), int(float(n)))
        # Mapear los valores Ri a variable global
        global ri_cuadrados, ultimo_metodo_generacion
        ri_cuadrados = df['Ri'].tolist()
        ultimo_metodo_generacion = "cuadrados"
        data = df.to_html(classes="table table-bordered table-striped", index=False)

    return render_template("cuadrados.html", 
                           table=data, 
                           semilla=semilla, 
                           n=n, 
                           min_val=min_val, 
                           max_val=max_val)

@app.route("/lineal", methods=["GET", "POST"])
def lineal():
    data = None
    xo = ""
    k = ""
    c = ""
    g = ""
    n = ""
    # min_val = ""
    # max_val = ""

    if request.method == "POST":
        xo = request.form["xo"]
        k = request.form["k"]
        c = request.form["c"]
        g = request.form["g"]
        n = request.form["iteraciones"]
        # min_val = request.form["min"]
        # max_val = request.form["max"]

        # Aquí llamamos al generador de congruencia lineal
        # df = generar_cl(int(xo), int(k), int(c), int(g), int(float(n)), float(min_val), float(max_val))
        df = generar_cl(int(xo), int(k), int(c), int(g), int(float(n)),0,0)
        # Mapear los valores Ri a variable global
        global ri_lineal, ultimo_metodo_generacion
        ri_lineal = df['Ri'].tolist()
        ultimo_metodo_generacion = "lineal"
        data = df.to_html(classes="table table-bordered table-striped text-center", index=False)

    return render_template("lineal.html", 
                           table=data, 
                           xo=xo, 
                           k=k, 
                           c=c, 
                           g=g, 
                           n=n)
                        #    min_val=min_val, 
                        #    max_val=max_val)

@app.route("/multiplicativo", methods=["GET", "POST"])
def multiplicativo():
    data = None
    xo = ""
    k = ""
    t = ""
    g = ""
    n = ""
    # min_val = ""
    # max_val = ""

    if request.method == "POST":
        xo = request.form["xo"]
        t = request.form["t"]
        g = request.form["g"]
        n = request.form["iteraciones"]
        # min_val = request.form["min"]
        # max_val = request.form["max"]

        # Llamamos al generador de congruencia multiplicativa
        # df = generar_cm(int(xo), int(t), int(g), int(float(n)), float(min_val), float(max_val))
        df = generar_cm(int(xo), int(t), int(g), int(float(n)))
        # Mapear los valores Ri a variable global
        global ri_multiplicativo, ultimo_metodo_generacion
        ri_multiplicativo = df['Ri'].tolist()
        ultimo_metodo_generacion = "multiplicativo"
        data = df.to_html(classes="table table-bordered table-striped text-center", index=False)

    return render_template("multiplicativo.html",
                           table=data,
                           xo=xo,
                           k=k,
                           t=t,
                           g=g,
                           n=n)
                        #    min_val=min_val,
                        #    max_val=max_val)


# Exportar CSV
@app.route("/export_cuadrados_csv", methods=["POST"])
def exportar_csv():
    semilla = int(request.form["semilla"])
    n = int(request.form["iteraciones"])
    # min_val = float(request.form["min"])
    # max_val = float(request.form["max"])

    df = generar_mc(semilla, n)

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="cuadrados_medios.csv")

@app.route("/export_lineal_csv", methods=["POST"])
def exportar_csv_congruencial_lineal():
    xo = request.form["xo"]
    k = request.form["k"]
    c = request.form["c"]
    g = request.form["g"]
    n = request.form["iteraciones"]
    # min_val = request.form["min"]
    # max_val = request.form["max"]

        # Aquí llamamos al generador de congruencia lineal
    df = generar_cl(int(xo), int(k), int(c), int(g), int(float(n)), 0,0)

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="congruencial_lineal.csv")

@app.route("/export_multiplicativa_csv", methods=["POST"])
def exportar_csv_congruencial_multiplicativa():
    xo = request.form["xo"]
    t = request.form["t"]
    g = request.form["g"]
    n = request.form["iteraciones"]
    # min_val = request.form["min"]
    # max_val = request.form["max"]

    df = generar_cm(int(xo), int(t), int(g), int(float(n)), 0,0)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="congruencial_multiplicativa.csv")

@app.route("/graficar/cuadrados_medios", methods=["POST"])
def graficar_cuadrados_medios():
    semilla = int(request.form["semilla"])
    n = int(request.form["iteraciones"])
    min_val = float(request.form["min"])
    max_val = float(request.form["max"])

    df = generar_mc(semilla, n, min_val, max_val)

    # --- Serie Temporal (índice vs Ri) ---
    fig1, ax1 = plt.subplots()
    ax1.plot(range(len(df["Ri"])), df["Ri"], marker="o", linestyle="-", markersize=3)
    ax1.set_title("Serie Temporal - Cuadrados Medios")
    ax1.set_xlabel("Iteración")
    ax1.set_ylabel("Ri")

    buf1 = io.BytesIO()
    plt.savefig(buf1, format="png")
    buf1.seek(0)
    img1 = base64.b64encode(buf1.getvalue()).decode("utf-8")
    plt.close(fig1)

    # --- Histograma de Ri ---
    fig2, ax2 = plt.subplots()
    ax2.hist(df["Ri"], bins=20, edgecolor="black", alpha=0.7)
    ax2.set_title("Histograma Ri - Cuadrados Medios")
    ax2.set_xlabel("Valor Ri")
    ax2.set_ylabel("Frecuencia")

    buf2 = io.BytesIO()
    plt.savefig(buf2, format="png")
    buf2.seek(0)
    img2 = base64.b64encode(buf2.getvalue()).decode("utf-8")
    plt.close(fig2)

    return jsonify({"serie_temporal": img1, "histograma": img2})


# Gráfico
@app.route("/grafico", methods=["POST"])
def grafico():
    semilla = int(request.form["semilla"])
    n = int(request.form["iteraciones"])
    min_val = float(request.form["min"])
    max_val = float(request.form["max"])

    df = generar_mc(semilla, n, min_val, max_val)

    plt.figure(figsize=(6,4))
    plt.plot(df["i"], df["Ri"], marker="o", linestyle="--")
    plt.title("Comportamiento de Ri")
    plt.xlabel("Iteración")
    plt.ylabel("Ri")
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    return send_file(img, mimetype="image/png")

@app.route("/obtener_ri/<generador>")
def obtener_ri_endpoint(generador):
    if generador == "cuadrados":
        return {"ri": ri_cuadrados}
    elif generador == "lineal":
        return {"ri": ri_lineal}
    elif generador == "multiplicativo":
        return {"ri": ri_multiplicativo}
    else:
        return {"error": "Generador no válido"}

def ejecutar_pruebas_internas(ri_numeros, alpha=0.05):
    """
    Ejecuta todas las pruebas estadísticas sobre los números Ri
    """
    pruebas_seleccionadas = {
        "medias": True,
        "varianza": True,
        "chi": {"k": 8},
        "kolmogorov": {"k": 10},
        "poker": True,
        "rachas": True
    }
    
    try:
        resultados = ejecutar_pruebas(ri_numeros, pruebas_seleccionadas, alpha)
        return resultados
    except Exception as e:
        return {"error": f"Error ejecutando pruebas: {str(e)}"}

def procesar_resultados_para_template(resultados_pruebas):
    """
    Procesa los resultados de pruebas (JSON strings) para que sean compatibles con los templates
    """
    resultados_procesados = {}
    
    for nombre_prueba, resultado_json in resultados_pruebas.items():
        if nombre_prueba in ['error', 'mensaje_error']:
            resultados_procesados[nombre_prueba] = resultado_json
            continue
            
        try:
            # Parsear el JSON string
            resultado_dict = json.loads(resultado_json)
            
            # Crear un diccionario compatible con el template
            resultado_procesado = {
                'pasa': resultado_dict.get('isApproved') == 'True',
                'test_name': resultado_dict.get('test_name', nombre_prueba),
                'decision': resultado_dict.get('decision', ''),
                'isApproved': resultado_dict.get('isApproved', 'False')
            }
            
            # Agregar campos específicos según el tipo de prueba
            if 'estadistico' in resultado_dict:
                resultado_procesado['estadistico'] = float(resultado_dict['estadistico'])
            elif 'z' in resultado_dict:
                resultado_procesado['estadistico'] = float(resultado_dict['z'])
            elif 'chi2_total' in resultado_dict.get('statistics', {}):
                resultado_procesado['estadistico'] = float(resultado_dict['statistics']['chi2_total'])
            elif 'Chi2_calculado' in resultado_dict.get('statistics', {}):
                resultado_procesado['estadistico'] = float(resultado_dict['statistics']['Chi2_calculado'])
                
            if 'valor_critico' in resultado_dict:
                resultado_procesado['valor_critico'] = float(resultado_dict['valor_critico'])
            elif 'critical_value' in resultado_dict.get('statistics', {}):
                resultado_procesado['valor_critico'] = float(resultado_dict['statistics']['critical_value'])
            elif 'chi2_critico' in resultado_dict.get('statistics', {}):
                resultado_procesado['valor_critico'] = float(resultado_dict['statistics']['chi2_critico'])
                
            if 'p_value' in resultado_dict:
                resultado_procesado['p_value'] = float(resultado_dict['p_value'])
                
            resultados_procesados[nombre_prueba] = resultado_procesado
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Si hay error al procesar, crear un resultado por defecto
            resultados_procesados[nombre_prueba] = {
                'pasa': False,
                'test_name': nombre_prueba,
                'decision': 'Error al procesar resultado',
                'isApproved': 'False'
            }
    
    return resultados_procesados

def obtener_ri():
    """Función para obtener los Ri del último método de generación usado"""
    global ultimo_metodo_generacion, ri_cuadrados, ri_lineal, ri_multiplicativo
    
    if ultimo_metodo_generacion == "cuadrados":
        return ri_cuadrados
    elif ultimo_metodo_generacion == "lineal":
        return ri_lineal
    elif ultimo_metodo_generacion == "multiplicativo":
        return ri_multiplicativo
    else:
        return []

@app.route("/distribucion_normal", methods=["GET", "POST"])
def distribucion_normal():
    grafico = None
    table = None
    media = 0.0
    desviacion = 1.0
    metodo_usado = ultimo_metodo_generacion
    resultados_pruebas = None
    
    # Verificar si hay datos disponibles
    ri_disponibles = obtener_ri()
    if not ri_disponibles:
        mensaje_error = "No hay datos de números aleatorios disponibles. Genera números primero usando algún método."
        return render_template("distribucion_normal.html", 
                             grafico=grafico, 
                             table=table, 
                             media=media, 
                             desviacion=desviacion,
                             metodo_usado=metodo_usado,
                             error=mensaje_error)

    if request.method == "POST" and request.form.get("accion") == "calcular":
        media = float(request.form.get("media", 0.0))
        desviacion = float(request.form.get("desviacion", 1.0))
        
        # Ejecutar pruebas estadísticas primero
        resultados_pruebas_raw = ejecutar_pruebas_internas(ri_disponibles)
        
        # Procesar resultados para el template
        resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
        
        # Verificar si alguna prueba pasó
        if "error" not in resultados_pruebas_raw:
            # Validar que al menos una prueba haya pasado
            pruebas_pasaron = False
            for nombre_prueba, resultado_json in resultados_pruebas_raw.items():
                try:
                    # Parsear el JSON string para obtener el diccionario
                    resultado_dict = json.loads(resultado_json)
                    # Verificar si la prueba fue aprobada
                    if resultado_dict.get("isApproved") == "True":
                        pruebas_pasaron = True
                        break
                except (json.JSONDecodeError, AttributeError):
                    # Si hay error al parsear, continuar con la siguiente prueba
                    continue
            
            if pruebas_pasaron:
                # Al menos una prueba pasó, proceder con el cálculo
                df_normal = distribucion_normal_inversa(ri_disponibles, desviacion, media)
                table = df_normal.to_html(classes="table table-bordered table-striped text-center", index=False)
                
                # Generar gráfico
                grafico = graficar_distribucion_normal(ri_disponibles, desviacion, media)
            else:
                # Ninguna prueba pasó, mostrar mensaje de error
                resultados_pruebas["mensaje_error"] = "No se puede proceder con la distribución normal porque ninguna prueba estadística fue aprobada. Los números generados no cumplen con los criterios de aleatoriedad."

    return render_template("distribucion_normal.html", 
                         grafico=grafico, 
                         table=table, 
                         media=media, 
                         desviacion=desviacion,
                         metodo_usado=metodo_usado,
                         resultados_pruebas=resultados_pruebas)



@app.route("/distribucion_uniforme", methods=["GET", "POST"])
def distribucion_uniforme_endpoint():
    grafico = None
    table = None
    min_val = 0.0
    max_val = 1.0
    metodo_usado = ultimo_metodo_generacion
    resultados_pruebas = None
    
    # Verificar si hay datos disponibles
    ri_disponibles = obtener_ri()
    if not ri_disponibles:
        mensaje_error = "No hay datos de números aleatorios disponibles. Genera números primero usando algún método."
        return render_template("distribucion_uniforme.html", 
                             grafico=grafico, 
                             table=table, 
                             min_val=min_val, 
                             max_val=max_val,
                             metodo_usado=metodo_usado,
                             error=mensaje_error)

    if request.method == "POST" and request.form.get("accion") == "calcular":
        min_val = float(request.form.get("min_val", 0.0))
        max_val = float(request.form.get("max_val", 1.0))
        
        # Ejecutar pruebas estadísticas primero
        resultados_pruebas_raw = ejecutar_pruebas_internas(ri_disponibles)
        
        # Procesar resultados para el template
        resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
        
        # Verificar si alguna prueba pasó
        if "error" not in resultados_pruebas_raw:
            # Validar que al menos una prueba haya pasado
            pruebas_pasaron = False
            for nombre_prueba, resultado_json in resultados_pruebas_raw.items():
                try:
                    # Parsear el JSON string para obtener el diccionario
                    resultado_dict = json.loads(resultado_json)
                    # Verificar si la prueba fue aprobada
                    if resultado_dict.get("isApproved") == "True":
                        pruebas_pasaron = True
                        break
                except (json.JSONDecodeError, AttributeError):
                    # Si hay error al parsear, continuar con la siguiente prueba
                    continue
            
            if pruebas_pasaron:
                # Al menos una prueba pasó, proceder con el cálculo
                df_uniforme, ni_values = distribucion_uniforme(ri_disponibles, min_val, max_val)
                table = df_uniforme.to_html(classes="table table-bordered table-striped text-center", index=False)
                
                # Generar gráfico
                grafico = graficar_distribucion_uniforme(ri_disponibles, ni_values, min_val, max_val)
            else:
                # Ninguna prueba pasó, mostrar mensaje de error
                resultados_pruebas["mensaje_error"] = "No se puede proceder con la distribución uniforme porque ninguna prueba estadística fue aprobada. Los números generados no cumplen con los criterios de aleatoriedad."

    return render_template("distribucion_uniforme.html", 
                         grafico=grafico, 
                         table=table, 
                         min_val=min_val, 
                         max_val=max_val,
                         metodo_usado=metodo_usado,
                         resultados_pruebas=resultados_pruebas)


if __name__ == "__main__":
    app.run(debug=True)

