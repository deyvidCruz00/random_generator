from flask import Flask, request, jsonify, render_template, send_file
from modules.pruebas.dispatcher import ejecutar_pruebas
from modules.generadores.minimos_cuadrados import generar as generar_mc
from modules.generadores.congruencia_lineal import generar as generar_cl
from modules.generadores.congruencia_multi import generar as generar_cm
#from modules.pruebas import media as prueba_media_mod

import pandas as pd
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import base64
import io

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

if __name__ == "__main__":
    app.run(debug=True)
