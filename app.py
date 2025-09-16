from flask import Flask, request, jsonify, render_template
from modules.pruebas.dispatcher import ejecutar_pruebas

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("pruebas.html")

@app.route("/pruebas", methods=["POST"])
def api_pruebas():
    data = request.get_json()
    datos = data.get("numeros", [])
    pruebas = data.get("pruebasSeleccionadas", {})
    alpha = data.get("alpha", 0.05)

    resultados = ejecutar_pruebas(datos, pruebas, alpha)
    return jsonify(resultados)

@app.route("/resultados")
def api_resultados():
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)