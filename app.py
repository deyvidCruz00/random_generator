from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
from modules.generadores.minimos_cuadrados import generar as generar_mc
from modules.generadores.congruencia_lineal import generar as generar_cl
from modules.generadores.congruencia_multi import generar as generar_cm
#from modules.pruebas import media as prueba_media_mod

app = Flask(__name__)
# variables globales temporales (puedes sustituir por almacenamiento en DB o archivos)
secuencia_df = None
secuencia_ri = None

# carpeta outputs
os.makedirs("outputs", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        metodo = request.form["metodo"]
        semilla = int(request.form["semilla"])
        n = int(request.form["n"])
        # selección de generador
        if metodo == "cuadrados":
            df = generar_mc(semilla, n, 0, 10)
            ri_list = df["Ri"].tolist()
        else:
            return "Método no implementado", 400
        

        # guardar en variables globales para usar en pruebas y para exportar
        global secuencia_df, secuencia_ri
        secuencia_df = df
        secuencia_ri = ri_list

        # guardar CSV de salida para permitir descarga
        out_path = "outputs/secuencia.csv"
        df.to_csv(out_path, index=False)

        # renderizar resultado (pasa el HTML de la tabla)
        table_html = df.to_html(classes="table table-striped", index=False, justify="center")
        return render_template("resultado.html", table_html=table_html)

    return render_template("index.html")


# @app.route("/pruebas", methods=["GET", "POST"])
# def pruebas():
#     global secuencia_ri
#     if secuencia_ri is None:
#         return redirect(url_for("index"))

#     # Por simplicidad, ejecutamos la prueba de medias si se accede:
#     resultados_media = prueba_media_mod.prueba_media(secuencia_ri, alpha=0.05)
#     return render_template("pruebas.html", resultados=resultados_media)


@app.route("/descargar")
def descargar():
    path = "outputs/secuencia.csv"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
