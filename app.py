from flask import Flask, request, jsonify, render_template, send_file
import time
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

# Variables globales para almacenar semilla seleccionada por método
semilla_seleccionada_cuadrados = None
semilla_seleccionada_lineal = None
semilla_seleccionada_multiplicativo = None

# Variable global para rastrear el último método de generación usado
ultimo_metodo_generacion = None

# Variable global para cachear resultados de pruebas estadísticas
ultimos_resultados_pruebas_raw = None
ultimos_resultados_pruebas_procesados = None

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
    global semilla_seleccionada_cuadrados
    data = None
    semilla = ""
    n = ""
    min_val = ""
    max_val = ""
    resultados_pruebas = None

    # Si hay una semilla pre-cargada y es GET, usar esa semilla
    if request.method == "GET" and semilla_seleccionada_cuadrados:
        semilla = str(semilla_seleccionada_cuadrados)
        # Limpiar la semilla después de usarla
        semilla_seleccionada_cuadrados = None

    if request.method == "POST":
        semilla = request.form["semilla"]
        n = request.form["iteraciones"]
        n_int = int(float(n))
        df = generar_mc(int(semilla), n_int)
        
        # Verificar si el DataFrame tiene datos y la columna Ri existe
        if df.empty or 'Ri' not in df.columns:
            return render_template("cuadrados.html", 
                                 error=f"Error: No se pudieron generar números con la semilla {semilla}. La secuencia se degeneró. Intenta con una semilla diferente.",
                                 xo=semilla, 
                                 n=n)
        
        # Mapear los valores Ri a variable global
        global ri_cuadrados, ultimo_metodo_generacion
        ri_cuadrados = df['Ri'].tolist()
        ultimo_metodo_generacion = "cuadrados"
        
        # Formatear la columna Ri para eliminar ceros innecesarios
        df['Ri'] = df['Ri'].apply(lambda x: f"{x:g}")
        
        tabla_mensaje = ""
        if n_int > 10000:
            # Mostrar solo los primeros 500, algunos del medio y los últimos 500
            df_muestra = df.head(500).copy()
            
            # Agregar algunos del medio
            if n_int > 2000:
                medio_inicio = n_int // 2 - 250
                medio_fin = n_int // 2 + 250
                df_medio = df.iloc[medio_inicio:medio_fin].copy()
                df_muestra = pd.concat([df_muestra, df_medio])
            
            # Agregar los últimos
            df_final = df.tail(500).copy()
            df_muestra = pd.concat([df_muestra, df_final])
            
            # Remover duplicados y ordenar
            df_muestra = df_muestra.drop_duplicates().sort_values('i')
            
            data = df_muestra.to_html(classes="table table-bordered table-striped", index=False)
            tabla_mensaje = f'''
            <div class="alert alert-info mb-3">
                <h5><i class="fas fa-info-circle"></i> Conjunto grande detectado</h5>
                <p><strong>Total generado:</strong> {n_int:,} números</p>
                <p><strong>Mostrando:</strong> {len(df_muestra):,} valores de muestra (primeros 500 + algunos del medio + últimos 500)</p>
                <p><small>Los {n_int:,} números completos están disponibles para exportar y se usaron para las pruebas estadísticas.</small></p>
            </div>
            '''
        else:
            # Para conjuntos pequeños, mostrar todo
            data = df.to_html(classes="table table-bordered table-striped", index=False)
        
        # Agregar el mensaje antes de la tabla
        if tabla_mensaje:
            data = tabla_mensaje + data
        
        # Si hay datos, ejecutar pruebas automáticamente para mantener consistencia
        if ri_cuadrados:
            global ultimos_resultados_pruebas_raw, ultimos_resultados_pruebas_procesados
            resultados_pruebas_raw = ejecutar_pruebas_internas(ri_cuadrados)
            resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
            
            # Guardar en cache para uso posterior en distribuciones
            ultimos_resultados_pruebas_raw = resultados_pruebas_raw
            ultimos_resultados_pruebas_procesados = resultados_pruebas

    return render_template("cuadrados.html", 
                           table=data, 
                           semilla=semilla, 
                           n=n, 
                           min_val=min_val, 
                           max_val=max_val,
                           resultados_pruebas=resultados_pruebas)

@app.route("/lineal", methods=["GET", "POST"])
def lineal():
    global semilla_seleccionada_lineal
    data = None
    xo = ""
    k = ""
    c = ""
    g = ""
    n = ""
    resultados_pruebas = None
    
    if request.method == "GET" and semilla_seleccionada_lineal:
        xo = str(semilla_seleccionada_lineal)
        # Limpiar la semilla después de usarla
        semilla_seleccionada_lineal = None

    if request.method == "POST":
        xo = request.form["xo"]
        k = request.form["k"]
        c = request.form["c"]
        g = request.form["g"]
        n = request.form["iteraciones"]

        n_int = int(float(n))
        
        # Aquí llamamos al generador de congruencia lineal
        df = generar_cl(int(xo), int(k), int(c), int(g), n_int)
        
        # Mapear los valores Ri a variable global
        global ri_lineal, ultimo_metodo_generacion
        ri_lineal = df['Ri'].tolist()
        ultimo_metodo_generacion = "lineal"
        
        # Formatear la columna Ri para eliminar ceros innecesarios
        df['Ri'] = df['Ri'].apply(lambda x: f"{x:g}")

        # OPTIMIZACIÓN: Para conjuntos grandes, mostrar solo una muestra
        tabla_mensaje = ""
        if n_int > 10000:
            # Mostrar solo los primeros 500, algunos del medio y los últimos 500
            df_muestra = df.head(500).copy()
            
            # Agregar algunos del medio
            if n_int > 2000:
                medio_inicio = n_int // 2 - 250
                medio_fin = n_int // 2 + 250
                df_medio = df.iloc[medio_inicio:medio_fin].copy()
                df_muestra = pd.concat([df_muestra, df_medio])
            
            # Agregar los últimos
            df_final = df.tail(500).copy()
            df_muestra = pd.concat([df_muestra, df_final])
            
            # Remover duplicados y ordenar
            df_muestra = df_muestra.drop_duplicates().sort_values('i')
            
            data = df_muestra.to_html(classes="table table-bordered table-striped text-center", index=False)
            tabla_mensaje = f'''
            <div class="alert alert-info mb-3">
                <h5><i class="fas fa-info-circle"></i> Conjunto grande detectado</h5>
                <p><strong>Total generado:</strong> {n_int:,} números</p>
                <p><strong>Mostrando:</strong> {len(df_muestra):,} valores de muestra (primeros 500 + algunos del medio + últimos 500)</p>
                <p><small>Los {n_int:,} números completos están disponibles para exportar y se usaron para las pruebas estadísticas.</small></p>
            </div>
            '''
        else:
            # Para conjuntos pequeños, mostrar todo
            data = df.to_html(classes="table table-bordered table-striped text-center", index=False)
        
        # Agregar el mensaje antes de la tabla
        if tabla_mensaje:
            data = tabla_mensaje + data
        
        # Si hay datos, ejecutar pruebas automáticamente para mantener consistencia
        if ri_lineal:
            global ultimos_resultados_pruebas_raw, ultimos_resultados_pruebas_procesados
            resultados_pruebas_raw = ejecutar_pruebas_internas(ri_lineal)
            resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
            
            # Guardar en cache para uso posterior en distribuciones
            ultimos_resultados_pruebas_raw = resultados_pruebas_raw
            ultimos_resultados_pruebas_procesados = resultados_pruebas

    return render_template("lineal.html", 
                           table=data, 
                           xo=xo, 
                           k=k, 
                           c=c, 
                           g=g, 
                           n=n,
                           resultados_pruebas=resultados_pruebas)

@app.route("/multiplicativo", methods=["GET", "POST"])
def multiplicativo():
    global semilla_seleccionada_multiplicativo
    data = None
    xo = ""
    k = ""
    t = ""
    g = ""
    n = ""
    resultados_pruebas = None

    # Si hay una semilla pre-cargada y es GET, usar esa semilla
    if request.method == "GET" and semilla_seleccionada_multiplicativo:
        xo = str(semilla_seleccionada_multiplicativo)
        # Limpiar la semilla después de usarla
        semilla_seleccionada_multiplicativo = None

    if request.method == "POST":
        xo = request.form["xo"]
        t = request.form["t"]
        g = request.form["g"]
        n = request.form["iteraciones"]

        n_int = int(float(n))
        
        # Llamamos al generador de congruencia multiplicativa
        df = generar_cm(int(xo), int(t), int(g), n_int)
        # Mapear los valores Ri a variable global
        global ri_multiplicativo, ultimo_metodo_generacion
        ri_multiplicativo = df['Ri'].tolist()
        ultimo_metodo_generacion = "multiplicativo"
        
        # Formatear la columna Ri para eliminar ceros innecesarios
        df['Ri'] = df['Ri'].apply(lambda x: f"{x:g}")
        
        # ⚡ OPTIMIZACIÓN: Para conjuntos grandes, mostrar solo una muestra
        tabla_mensaje = ""
        if n_int > 10000:
            # Mostrar solo los primeros 500, algunos del medio y los últimos 500
            df_muestra = df.head(500).copy()
            
            # Agregar algunos del medio
            if n_int > 2000:
                medio_inicio = n_int // 2 - 250
                medio_fin = n_int // 2 + 250
                df_medio = df.iloc[medio_inicio:medio_fin].copy()
                df_muestra = pd.concat([df_muestra, df_medio])
            
            # Agregar los últimos
            df_final = df.tail(500).copy()
            df_muestra = pd.concat([df_muestra, df_final])
            
            # Remover duplicados y ordenar
            df_muestra = df_muestra.drop_duplicates().sort_values('i')
            
            data = df_muestra.to_html(classes="table table-bordered table-striped text-center", index=False)
            tabla_mensaje = f'''
            <div class="alert alert-info mb-3">
                <h5><i class="fas fa-info-circle"></i> Conjunto grande detectado</h5>
                <p><strong>Total generado:</strong> {n_int:,} números</p>
                <p><strong>Mostrando:</strong> {len(df_muestra):,} valores de muestra (primeros 500 + algunos del medio + últimos 500)</p>
                <p><small>Los {n_int:,} números completos están disponibles para exportar y se usaron para las pruebas estadísticas.</small></p>
            </div>
            '''
        else:
            # Para conjuntos pequeños, mostrar todo
            data = df.to_html(classes="table table-bordered table-striped text-center", index=False)
        
        # Agregar el mensaje antes de la tabla
        if tabla_mensaje:
            data = tabla_mensaje + data
        
        # Si hay datos, ejecutar pruebas automáticamente para mantener consistencia
        if ri_multiplicativo:
            global ultimos_resultados_pruebas_raw, ultimos_resultados_pruebas_procesados
            resultados_pruebas_raw = ejecutar_pruebas_internas(ri_multiplicativo)
            resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
            
            # Guardar en cache para uso posterior en distribuciones
            ultimos_resultados_pruebas_raw = resultados_pruebas_raw
            ultimos_resultados_pruebas_procesados = resultados_pruebas

    return render_template("multiplicativo.html",
                           table=data,
                           xo=xo,
                           k=k,
                           t=t,
                           g=g,
                           n=n,
                           resultados_pruebas=resultados_pruebas)


# Exportar CSV
@app.route("/export_cuadrados_csv", methods=["POST"])
def exportar_csv():
    semilla = int(request.form["semilla"])
    n = int(request.form["iteraciones"])

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

    df = generar_cm(int(xo), int(t), int(g), int(float(n)), 0,0)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="congruencial_multiplicativa.csv")

# Métodos para exportar únicamente los Ri generados
@app.route("/export_ri_cuadrados", methods=["POST"])
def exportar_ri_cuadrados():
    """Exportar solo los valores Ri de cuadrados medios previamente generados"""
    global ri_cuadrados
    
    if not ri_cuadrados:
        # Si no hay datos, mostrar mensaje de error
        return render_template("cuadrados.html", 
                             error="No hay datos de cuadrados medios disponibles para exportar.")
    
    # Crear DataFrame solo con los Ri
    df_ri = pd.DataFrame({'Ri': ri_cuadrados})
    
    buffer = io.StringIO()
    df_ri.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="ri_cuadrados_medios.csv")

@app.route("/export_ri_lineal", methods=["POST"])
def exportar_ri_lineal():
    """Exportar solo los valores Ri de congruencia lineal previamente generados"""
    global ri_lineal
    
    if not ri_lineal:
        # Si no hay datos, mostrar mensaje de error
        return render_template("lineal.html", 
                             error="No hay datos de congruencia lineal disponibles para exportar.")
    
    # Crear DataFrame solo con los Ri
    df_ri = pd.DataFrame({'Ri': ri_lineal})
    
    buffer = io.StringIO()
    df_ri.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="ri_congruencia_lineal.csv")

@app.route("/export_ri_multiplicativo", methods=["POST"])
def exportar_ri_multiplicativo():
    """Exportar solo los valores Ri de congruencia multiplicativa previamente generados"""
    global ri_multiplicativo
    
    if not ri_multiplicativo:
        # Si no hay datos, mostrar mensaje de error
        return render_template("multiplicativo.html", 
                             error="No hay datos de congruencia multiplicativa disponibles para exportar.")
    
    # Crear DataFrame solo con los Ri
    df_ri = pd.DataFrame({'Ri': ri_multiplicativo})
    
    buffer = io.StringIO()
    df_ri.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="ri_congruencia_multiplicativa.csv")

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
        
        # 🚀 OPTIMIZACIÓN: Reutilizar resultados de pruebas si están disponibles
        global ultimos_resultados_pruebas_raw, ultimos_resultados_pruebas_procesados
        
        if ultimos_resultados_pruebas_raw is not None and ultimos_resultados_pruebas_procesados is not None:
            # Usar resultados cacheados (sin volver a ejecutar pruebas)
            resultados_pruebas_raw = ultimos_resultados_pruebas_raw
            resultados_pruebas = ultimos_resultados_pruebas_procesados
            print("✅ Reutilizando resultados de pruebas cacheados en distribución normal")
        else:
            # Fallback: ejecutar pruebas si no hay cache disponible
            resultados_pruebas_raw = ejecutar_pruebas_internas(ri_disponibles)
            resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
            print("⚠️ Ejecutando pruebas desde cero en distribución normal (no hay cache)")
        
        # Verificar si alguna prueba pasó
        if "error" not in resultados_pruebas_raw:
            # Validar que al menos una prueba haya pasado
            pruebas_pasaron = False
            for nombre_prueba, resultado_json in resultados_pruebas_raw.items():
                try:
                    # Parsear el JSON string para obtener el diccionario
                    resultado_dict = json.loads(resultado_json)
                    print("calculado prueba")

                    # Verificar si la prueba fue aprobada
                    if resultado_dict.get("isApproved") == "True":
                        print("pruebas pasaron")
                        pruebas_pasaron = True
                        break
                except (json.JSONDecodeError, AttributeError):
                    # Si hay error al parsear, continuar con la siguiente prueba
                    continue
            
            if pruebas_pasaron:
                # Al menos una prueba pasó, proceder con el cálculo
                df_normal = distribucion_normal_inversa(ri_disponibles, desviacion, media)
                print("distribucion calculada")
                
                # ⚡ OPTIMIZACIÓN: Para conjuntos grandes, mostrar solo una muestra
                tabla_mensaje = ""
                n_total = len(df_normal)
                if n_total > 10000:
                    # Mostrar solo los primeros 500, algunos del medio y los últimos 500
                    df_muestra = df_normal.head(500).copy()
                    
                    # Agregar algunos del medio
                    if n_total > 2000:
                        medio_inicio = n_total // 2 - 250
                        medio_fin = n_total // 2 + 250
                        df_medio = df_normal.iloc[medio_inicio:medio_fin].copy()
                        df_muestra = pd.concat([df_muestra, df_medio])
                    
                    # Agregar los últimos
                    df_final = df_normal.tail(500).copy()
                    df_muestra = pd.concat([df_muestra, df_final])
                    
                    # Remover duplicados y ordenar por índice
                    df_muestra = df_muestra.drop_duplicates().sort_index()
                    
                    table = df_muestra.to_html(classes="table table-bordered table-striped text-center", index=False)
                    tabla_mensaje = f'''
                    <div class="alert alert-info mb-3">
                        <h5><i class="fas fa-info-circle"></i> Conjunto grande detectado</h5>
                        <p><strong>Total de valores transformados:</strong> {n_total:,} números</p>
                        <p><strong>Mostrando:</strong> {len(df_muestra):,} valores de muestra (primeros 500 + algunos del medio + últimos 500)</p>
                        <p><small>La distribución completa se basó en todos los {n_total:,} valores.</small></p>
                    </div>
                    '''
                else:
                    # Para conjuntos pequeños, mostrar todo
                    table = df_normal.to_html(classes="table table-bordered table-striped text-center", index=False)
                
                # Agregar el mensaje antes de la tabla
                if tabla_mensaje:
                    table = tabla_mensaje + table
                
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
        
        # 🚀 OPTIMIZACIÓN: Reutilizar resultados de pruebas si están disponibles
        global ultimos_resultados_pruebas_raw, ultimos_resultados_pruebas_procesados
        
        if ultimos_resultados_pruebas_raw is not None and ultimos_resultados_pruebas_procesados is not None:
            # Usar resultados cacheados (sin volver a ejecutar pruebas)
            resultados_pruebas_raw = ultimos_resultados_pruebas_raw
            resultados_pruebas = ultimos_resultados_pruebas_procesados
            print("✅ Reutilizando resultados de pruebas cacheados en distribución uniforme")
        else:
            # Fallback: ejecutar pruebas si no hay cache disponible
            resultados_pruebas_raw = ejecutar_pruebas_internas(ri_disponibles)
            resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
            print("⚠️ Ejecutando pruebas desde cero en distribución uniforme (no hay cache)")
        
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
                
                # ⚡ OPTIMIZACIÓN: Para conjuntos grandes, mostrar solo una muestra
                tabla_mensaje = ""
                n_total = len(df_uniforme)
                if n_total > 10000:
                    # Mostrar solo los primeros 500, algunos del medio y los últimos 500
                    df_muestra = df_uniforme.head(500).copy()
                    
                    # Agregar algunos del medio
                    if n_total > 2000:
                        medio_inicio = n_total // 2 - 250
                        medio_fin = n_total // 2 + 250
                        df_medio = df_uniforme.iloc[medio_inicio:medio_fin].copy()
                        df_muestra = pd.concat([df_muestra, df_medio])
                    
                    # Agregar los últimos
                    df_final = df_uniforme.tail(500).copy()
                    df_muestra = pd.concat([df_muestra, df_final])
                    
                    # Remover duplicados y ordenar por índice
                    df_muestra = df_muestra.drop_duplicates().sort_index()
                    
                    table = df_muestra.to_html(classes="table table-bordered table-striped text-center", index=False)
                    tabla_mensaje = f'''
                    <div class="alert alert-info mb-3">
                        <h5><i class="fas fa-info-circle"></i> Conjunto grande detectado</h5>
                        <p><strong>Total de valores transformados:</strong> {n_total:,} números</p>
                        <p><strong>Mostrando:</strong> {len(df_muestra):,} valores de muestra (primeros 500 + algunos del medio + últimos 500)</p>
                        <p><small>La distribución completa se basó en todos los {n_total:,} valores.</small></p>
                    </div>
                    '''
                else:
                    # Para conjuntos pequeños, mostrar todo
                    table = df_uniforme.to_html(classes="table table-bordered table-striped text-center", index=False)
                
                # Agregar el mensaje antes de la tabla
                if tabla_mensaje:
                    table = tabla_mensaje + table
                
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


# Rutas para cargar semillas desde archivo
@app.route("/cargar_semillas_cuadrados", methods=["GET", "POST"])
def cargar_semillas_cuadrados():
    """Cargar semillas para cuadrados medios desde archivo CSV"""
    return cargar_semillas_proceso("cuadrados", "Cargar Semillas - Cuadrados Medios")

@app.route("/usar_semilla_cuadrados", methods=["POST"])
def usar_semilla_cuadrados():
    """Usar semilla seleccionada para cuadrados medios"""
    from flask import redirect
    global semilla_seleccionada_cuadrados
    semilla = request.form.get('semilla')
    if semilla:
        semilla_seleccionada_cuadrados = int(semilla)
    return redirect('/cuadrados')

@app.route("/cargar_semillas_lineal", methods=["GET", "POST"])
def cargar_semillas_lineal():
    """Cargar valores X0 para congruencia lineal desde archivo CSV"""
    return cargar_semillas_proceso("lineal", "Cargar Valores X0 - Congruencia Lineal")

@app.route("/usar_semilla_lineal", methods=["POST"])
def usar_semilla_lineal():
    """Usar X0 seleccionado para congruencia lineal"""
    from flask import redirect
    global semilla_seleccionada_lineal
    semilla = request.form.get('semilla')
    if semilla:
        semilla_seleccionada_lineal = int(semilla)
    return redirect('/lineal')

@app.route("/cargar_semillas_multiplicativo", methods=["GET", "POST"])
def cargar_semillas_multiplicativo():
    """Cargar valores X0 para congruencia multiplicativa desde archivo CSV"""
    return cargar_semillas_proceso("multiplicativo", "Cargar Valores X0 - Congruencia Multiplicativa")

@app.route("/usar_semilla_multiplicativo", methods=["POST"])
def usar_semilla_multiplicativo():
    """Usar X0 seleccionado para congruencia multiplicativa"""
    from flask import redirect
    global semilla_seleccionada_multiplicativo
    semilla = request.form.get('semilla')
    if semilla:
        semilla_seleccionada_multiplicativo = int(semilla)
    return redirect('/multiplicativo')

def cargar_semillas_proceso(metodo, titulo):
    """Función auxiliar para procesar la carga de semillas"""
    if request.method == "GET":
        return render_template("cargar_semillas.html", 
                             metodo=metodo,
                             titulo=titulo)
    
    if 'archivo' not in request.files:
        return render_template("cargar_semillas.html", 
                             metodo=metodo,
                             titulo=titulo,
                             error="No se seleccionó ningún archivo.")
    
    archivo = request.files['archivo']
    if archivo.filename == '':
        return render_template("cargar_semillas.html", 
                             metodo=metodo,
                             titulo=titulo,
                             error="No se seleccionó ningún archivo.")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo)
        
        # Buscar columna con semillas/x0
        columna_semilla = None
        for col in df.columns:
            if col.lower() in ['semilla', 'semillas', 'seed', 'seeds', 'x0', 'xo']:
                columna_semilla = col
                break
        
        if columna_semilla is None:
            return render_template("cargar_semillas.html", 
                                 metodo=metodo,
                                 titulo=titulo,
                                 error="No se encontró columna de semillas. Asegúrate de que el archivo tenga una columna llamada 'semilla', 'seed', 'x0' o 'xo'.")
        
        semillas = df[columna_semilla].tolist()
        
        # Validar que todas las semillas sean números válidos
        semillas_validas = []
        for semilla in semillas:
            try:
                semilla_int = int(float(semilla))
                if semilla_int > 0:
                    semillas_validas.append(semilla_int)
            except (ValueError, TypeError):
                continue
        
        if not semillas_validas:
            return render_template("cargar_semillas.html", 
                                 metodo=metodo,
                                 titulo=titulo,
                                 error="No se encontraron semillas válidas en el archivo.")
        
        return render_template("cargar_semillas.html", 
                             metodo=metodo,
                             titulo=titulo,
                             semillas=semillas_validas,
                             success=f"Se cargaron {len(semillas_validas)} semillas exitosamente.")
    
    except Exception as e:
        return render_template("cargar_semillas.html", 
                             metodo=metodo,
                             titulo=titulo,
                             error=f"Error al procesar el archivo: {str(e)}")


@app.route("/pruebas_cuadrados", methods=["POST"])
def pruebas_cuadrados():
    """Ejecutar pruebas estadísticas sobre los números Ri de cuadrados medios"""
    global ri_cuadrados
    
    if not ri_cuadrados:
        return render_template("cuadrados.html", 
                             error="No hay datos de cuadrados medios disponibles para realizar pruebas.")
    
    # Ejecutar pruebas estadísticas
    resultados_pruebas_raw = ejecutar_pruebas_internas(ri_cuadrados)
    resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
    
    # Obtener parámetros actuales para el template
    semilla = request.form.get("semilla", 1234)
    n = request.form.get("iteraciones", 10)
    
    return render_template("cuadrados.html", 
                         semilla=semilla,
                         n=n,
                         resultados_pruebas=resultados_pruebas)


@app.route("/pruebas_lineal", methods=["POST"])
def pruebas_lineal():
    """Ejecutar pruebas estadísticas sobre los números Ri de congruencia lineal"""
    global ri_lineal
    
    if not ri_lineal:
        return render_template("lineal.html", 
                             error="No hay datos de congruencia lineal disponibles para realizar pruebas.")
    
    # Ejecutar pruebas estadísticas
    resultados_pruebas_raw = ejecutar_pruebas_internas(ri_lineal)
    resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
    
    # Obtener parámetros actuales para el template
    xo = request.form.get("xo", 17)
    k = request.form.get("k", 5)
    c = request.form.get("c", 3)
    g = request.form.get("g", 11)
    n = request.form.get("iteraciones", 10)
    
    return render_template("lineal.html", 
                         xo=xo, k=k, c=c, g=g, n=n,
                         resultados_pruebas=resultados_pruebas)


@app.route("/pruebas_multiplicativo", methods=["POST"])
def pruebas_multiplicativo():
    """Ejecutar pruebas estadísticas sobre los números Ri de congruencia multiplicativa"""
    global ri_multiplicativo
    
    if not ri_multiplicativo:
        return render_template("multiplicativo.html", 
                             error="No hay datos de congruencia multiplicativa disponibles para realizar pruebas.")
    
    # Ejecutar pruebas estadísticas
    resultados_pruebas_raw = ejecutar_pruebas_internas(ri_multiplicativo)
    resultados_pruebas = procesar_resultados_para_template(resultados_pruebas_raw)
    
    # Obtener parámetros actuales para el template
    xo = request.form.get("xo", 17)
    t = request.form.get("t", 3)
    g = request.form.get("g", 5)
    n = request.form.get("iteraciones", 10)
    
    return render_template("multiplicativo.html", 
                         xo=xo, t=t, g=g, n=n,
                         resultados_pruebas=resultados_pruebas)


@app.route("/exportar_normal_csv", methods=["POST"])
def exportar_normal_csv():
    """Exportar datos de distribución normal a CSV"""
    try:
        # Obtener datos disponibles
        ri_disponibles = obtener_ri()
        if not ri_disponibles:
            return jsonify({"error": "No hay datos disponibles para exportar"}), 400
        
        # Obtener parámetros del formulario
        media = float(request.form.get("media", 0.0))
        desviacion = float(request.form.get("desviacion", 1.0))
        
        # Generar distribución normal
        df_normal = distribucion_normal_inversa(ri_disponibles, desviacion, media)
        
        # Crear archivo CSV en memoria
        output = io.StringIO()
        df_normal.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)
        
        # Crear un objeto de bytes
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        
        # Generar nombre de archivo con parámetros
        filename = f"distribucion_normal_media_{media}_desv_{desviacion}.csv"
        
        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({"error": f"Error al exportar: {str(e)}"}), 500


@app.route("/exportar_uniforme_csv", methods=["POST"])
def exportar_uniforme_csv():
    """Exportar datos de distribución uniforme a CSV"""
    try:
        # Obtener datos disponibles
        ri_disponibles = obtener_ri()
        if not ri_disponibles:
            return jsonify({"error": "No hay datos disponibles para exportar"}), 400
        
        # Obtener parámetros del formulario
        min_val = float(request.form.get("min_val", 0.0))
        max_val = float(request.form.get("max_val", 1.0))
        
        # Generar distribución uniforme
        df_uniforme, ni_values = distribucion_uniforme(ri_disponibles, min_val, max_val)
        
        # Crear archivo CSV en memoria
        output = io.StringIO()
        df_uniforme.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)
        
        # Crear un objeto de bytes
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        
        # Generar nombre de archivo con parámetros
        filename = f"distribucion_uniforme_min_{min_val}_max_{max_val}.csv"
        
        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({"error": f"Error al exportar: {str(e)}"}), 500


@app.route("/grafico_uniforme", methods=["POST"])
def grafico_uniforme():
    """Generar solo el gráfico de distribución uniforme"""
    try:
        # Obtener datos disponibles
        ri_disponibles = obtener_ri()
        if not ri_disponibles:
            mensaje_error = "No hay datos de números aleatorios disponibles. Genera números primero usando algún método."
            return render_template("distribucion_uniforme.html", 
                                 error=mensaje_error,
                                 min_val=0.0,
                                 max_val=1.0,
                                 metodo_usado=ultimo_metodo_generacion)
        
        # Obtener parámetros del formulario
        min_val = float(request.form.get("min_val", 0.0))
        max_val = float(request.form.get("max_val", 1.0))
        
        # Generar distribución uniforme
        df_uniforme, ni_values = distribucion_uniforme(ri_disponibles, min_val, max_val)
        
        # Generar solo el gráfico
        grafico = graficar_distribucion_uniforme(ri_disponibles, ni_values, min_val, max_val)
        
        return render_template("distribucion_uniforme.html", 
                             grafico=grafico,
                             table=None,  # Solo mostrar gráfico
                             min_val=min_val,
                             max_val=max_val,
                             metodo_usado=ultimo_metodo_generacion)
    
    except Exception as e:
        return render_template("distribucion_uniforme.html", 
                             error=f"Error al generar gráfico: {str(e)}",
                             min_val=request.form.get("min_val", 0.0),
                             max_val=request.form.get("max_val", 1.0),
                             metodo_usado=ultimo_metodo_generacion)


@app.route("/grafico_serie_cuadrados", methods=["POST"])
def grafico_serie_cuadrados():
    """Generar gráfico de serie temporal para cuadrados medios"""
    try:
        from modules.generadores.minimos_cuadrados import graficar_serie_temporal
        
        # Verificar que hay datos disponibles
        if not ri_cuadrados:
            return render_template("grafico_serie.html", 
                                 error="No hay datos de cuadrados medios disponibles. Genera números primero.",
                                 metodo="Cuadrados Medios",
                                 volver_url="/cuadrados")
        
        # Obtener parámetros del formulario si están disponibles
        semilla = request.form.get("semilla", "N/A")
        iteraciones = len(ri_cuadrados)
        
        titulo_adicional = f"Semilla: {semilla} | Números generados: {iteraciones}"
        
        # Generar gráfico
        grafico = graficar_serie_temporal(ri_cuadrados, "Cuadrados Medios", titulo_adicional)
        
        return render_template("grafico_serie.html", 
                             grafico=grafico,
                             metodo="Cuadrados Medios",
                             titulo_adicional=titulo_adicional,
                             volver_url="/cuadrados",
                             total_numeros=iteraciones)
    
    except Exception as e:
        return render_template("grafico_serie.html", 
                             error=f"Error al generar gráfico: {str(e)}",
                             metodo="Cuadrados Medios",
                             volver_url="/cuadrados")


@app.route("/grafico_serie_lineal", methods=["POST"])
def grafico_serie_lineal():
    """Generar gráfico de serie temporal para congruencia lineal"""
    try:
        from modules.generadores.congruencia_lineal import graficar_serie_temporal
        
        # Verificar que hay datos disponibles
        if not ri_lineal:
            return render_template("grafico_serie.html", 
                                 error="No hay datos de congruencia lineal disponibles. Genera números primero.",
                                 metodo="Congruencia Lineal",
                                 volver_url="/lineal")
        
        # Obtener parámetros del formulario
        xo = request.form.get("xo", "N/A")
        k = request.form.get("k", "N/A")
        c = request.form.get("c", "N/A")
        g = request.form.get("g", "N/A")
        iteraciones = len(ri_lineal)
        
        parametros_info = f"x₀={xo}, k={k}, c={c}, g={g}"
        titulo_adicional = f"Números generados: {iteraciones}"
        
        # Generar gráfico
        grafico = graficar_serie_temporal(ri_lineal, parametros_info, titulo_adicional)
        
        return render_template("grafico_serie.html", 
                             grafico=grafico,
                             metodo="Congruencia Lineal",
                             titulo_adicional=f"{parametros_info} | {titulo_adicional}",
                             volver_url="/lineal",
                             total_numeros=iteraciones)
    
    except Exception as e:
        return render_template("grafico_serie.html", 
                             error=f"Error al generar gráfico: {str(e)}",
                             metodo="Congruencia Lineal",
                             volver_url="/lineal")


@app.route("/grafico_serie_multiplicativo", methods=["POST"])
def grafico_serie_multiplicativo():
    """Generar gráfico de serie temporal para congruencia multiplicativa"""
    try:
        from modules.generadores.congruencia_multi import graficar_serie_temporal
        
        # Verificar que hay datos disponibles
        if not ri_multiplicativo:
            return render_template("grafico_serie.html", 
                                 error="No hay datos de congruencia multiplicativa disponibles. Genera números primero.",
                                 metodo="Congruencia Multiplicativa",
                                 volver_url="/multiplicativo")
        
        # Obtener parámetros del formulario
        xo = request.form.get("xo", "N/A")
        t = request.form.get("t", "N/A")
        g = request.form.get("g", "N/A")
        iteraciones = len(ri_multiplicativo)
        
        parametros_info = f"x₀={xo}, t={t}, g={g}"
        titulo_adicional = f"Números generados: {iteraciones}"
        
        # Generar gráfico
        grafico = graficar_serie_temporal(ri_multiplicativo, parametros_info, titulo_adicional)
        
        return render_template("grafico_serie.html", 
                             grafico=grafico,
                             metodo="Congruencia Multiplicativa",
                             titulo_adicional=f"{parametros_info} | {titulo_adicional}",
                             volver_url="/multiplicativo",
                             total_numeros=iteraciones)
    
    except Exception as e:
        return render_template("grafico_serie.html", 
                             error=f"Error al generar gráfico: {str(e)}",
                             metodo="Congruencia Multiplicativa",
                             volver_url="/multiplicativo")


if __name__ == "__main__":
    app.run(debug=True)

