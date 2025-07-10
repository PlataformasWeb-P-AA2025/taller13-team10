from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
from config import token

app = Flask(__name__, template_folder='templates')

# Headers para autenticación por token
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/los/edificios")
def los_edificios():
    r = requests.get("http://127.0.0.1:8000/api/edificios/", headers=headers)
    if r.status_code == 200:
        try:
            edificios = r.json()
        except Exception:
            edificios = []
    else:
        edificios = []
    numero_edificios = len(edificios)
    return render_template("edificios.html", edificios=edificios, numero_edificios=numero_edificios)

@app.route("/los/departamentos")
def los_departamentos():
    """
    """
    r = requests.get("http://localhost:8000/api/departamentos/", headers=headers)
    print("---------------------")
    print(r.content)
    print("---------------------")
    departamentos = json.loads(r.content)
    numero_departamentos = len(departamentos)
    return render_template("departamentos.html", departamentos=departamentos,
    numero_departamentos=numero_departamentos)

    """
    """
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        tipo = request.form['tipo']
        edificio_data = {
            'nombre': nombre,
            'direccion': direccion,
            'ciudad': ciudad,
            'tipo': tipo
        }
        r = requests.post("http://localhost:8000/api/edificios/",
                          json=edificio_data,
                          headers=headers)
        print(f"Status Code (Crear Edificio): {r.status_code}")
        nuevo_edificio = json.loads(r.content)
        flash(f"Edificio '{nuevo_edificio['nombre']}' creado exitosamente!", 'success')
        return redirect(url_for('los_edificios'))
    return render_template("crear_edificio.html")

# Función auxiliar para mostrar el nombre del edificio en el template de departamentos
def obtener_edificio(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get('nombre', 'Sin nombre')
    return "Sin nombre"

app.jinja_env.globals.update(obtener_edificio=obtener_edificio)

if __name__ == "__main__":
    app.run(debug=True)