from flask import Flask, render_template, request, send_file
import pandas as pd
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from modules.generadores.minimos_cuadrados import generar as generar_mc
from modules.generadores.congruencia_lineal import generar as generar_cl
from modules.generadores.congruencia_multi import generar as generar_cm
#from modules.pruebas import media as prueba_media_mod



app = Flask(__name__)

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
        min_val = request.form["min"]
        max_val = request.form["max"]

        df = generar_mc(int(semilla), int(float(n)), float(min_val), float(max_val))
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
    min_val = ""
    max_val = ""

    if request.method == "POST":
        xo = request.form["xo"]
        k = request.form["k"]
        c = request.form["c"]
        g = request.form["g"]
        n = request.form["iteraciones"]
        min_val = request.form["min"]
        max_val = request.form["max"]

        # Aquí llamamos al generador de congruencia lineal
        df = generar_cl(int(xo), int(k), int(c), int(g), int(float(n)), float(min_val), float(max_val))
        data = df.to_html(classes="table table-bordered table-striped text-center", index=False)

    return render_template("lineal.html", 
                           table=data, 
                           xo=xo, 
                           k=k, 
                           c=c, 
                           g=g, 
                           n=n, 
                           min_val=min_val, 
                           max_val=max_val)

@app.route("/multiplicativo", methods=["GET", "POST"])
def multiplicativo():
    data = None
    xo = ""
    k = ""
    t = ""
    g = ""
    n = ""
    min_val = ""
    max_val = ""

    if request.method == "POST":
        xo = request.form["xo"]
        t = request.form["t"]
        g = request.form["g"]
        n = request.form["iteraciones"]
        min_val = request.form["min"]
        max_val = request.form["max"]

        # Llamamos al generador de congruencia multiplicativa
        df = generar_cm(int(xo), int(t), int(g), int(float(n)), float(min_val), float(max_val))
        data = df.to_html(classes="table table-bordered table-striped text-center", index=False)

    return render_template("multiplicativo.html",
                           table=data,
                           xo=xo,
                           k=k,
                           t=t,
                           g=g,
                           n=n,
                           min_val=min_val,
                           max_val=max_val)


# Exportar CSV
@app.route("/exportar_csv", methods=["POST"])
def exportar_csv():
    semilla = int(request.form["semilla"])
    n = int(request.form["iteraciones"])
    min_val = float(request.form["min"])
    max_val = float(request.form["max"])

    df = generar_mc(semilla, n, min_val, max_val)

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="numeros.csv")

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
