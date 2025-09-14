from flask import Flask, request, jsonify, render_template
from modules.pruebas.dispatcher import ejecutar_pruebas

app = Flask(__name__)

@app.route("/pruebas", methods=["POST"])
def api_pruebas():
    data = request.get_json()
    numeros = data.get("numeros", [])
    pruebas = data.get("pruebasSeleccionadas", {})
    alpha = data.get("alpha", 0.05)

    resultados = ejecutar_pruebas(numeros, pruebas, alpha)

    return jsonify({
        "n": len(numeros),
        "alpha": alpha,
        "resultados": resultados
    })
