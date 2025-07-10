from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
from config import token

app = Flask(__name__, template_folder='templates')
app.secret_key = "cambia_esto_por_algo_mas_secreto"  # <-- Agrega esta línea

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

@app.route("/edificio/editar/<int:edificio_id>", methods=["GET", "POST"])
def editar_edificio(edificio_id):
    edificio_url = f"http://127.0.0.1:8000/api/edificios/{edificio_id}/"
    if request.method == "POST":
        data = {
            "nombre": request.form["nombre"],
            "direccion": request.form["direccion"],
            "ciudad": request.form["ciudad"],
            "tipo": request.form["tipo"]
        }
        r = requests.put(edificio_url, json=data, headers=headers)
        if r.status_code in [200, 202]:
            flash("Edificio actualizado correctamente.", "success")
            return redirect(url_for("los_edificios"))
        else:
            flash("Error al actualizar el edificio.", "danger")
    r = requests.get(edificio_url, headers=headers)
    edificio = r.json() if r.status_code == 200 else {}
    return render_template("editar_edificio.html", edificio=edificio)

@app.route("/edificio/eliminar/<int:edificio_id>", methods=["POST"])
def eliminar_edificio(edificio_id):
    edificio_url = f"http://127.0.0.1:8000/api/edificios/{edificio_id}/"
    r = requests.delete(edificio_url, headers=headers)
    if r.status_code in [204, 200]:
        flash("Edificio eliminado correctamente.", "success")
    else:
        flash("Error al eliminar el edificio.", "danger")
    return redirect(url_for("los_edificios"))

@app.route("/departamento/editar/<int:departamento_id>", methods=["GET", "POST"])
def editar_departamento(departamento_id):
    departamento_url = f"http://127.0.0.1:8000/api/departamentos/{departamento_id}/"
    if request.method == "POST":
        data = {
            "nombre_propietario": request.form["nombre_propietario"],
            "costo": request.form["costo"],
            "numero_cuartos": request.form["numero_cuartos"],
            "edificio": request.form["edificio"]
        }
        r = requests.put(departamento_url, json=data, headers=headers)
        if r.status_code in [200, 202]:
            flash("Departamento actualizado correctamente.", "success")
            return redirect(url_for("los_departamentos"))
        else:
            flash("Error al actualizar el departamento.", "danger")
    r = requests.get(departamento_url, headers=headers)
    departamento = r.json() if r.status_code == 200 else {}
    # Obtener lista de edificios para el select
    edificios = requests.get("http://127.0.0.1:8000/api/edificios/", headers=headers).json()
    return render_template("editar_departamento.html", departamento=departamento, edificios=edificios)

@app.route("/departamento/eliminar/<int:departamento_id>", methods=["POST"])
def eliminar_departamento(departamento_id):
    departamento_url = f"http://127.0.0.1:8000/api/departamentos/{departamento_id}/"
    r = requests.delete(departamento_url, headers=headers)
    if r.status_code in [204, 200]:
        flash("Departamento eliminado correctamente.", "success")
    else:
        flash("Error al eliminar el departamento.", "danger")
    return redirect(url_for("los_departamentos"))

@app.route("/edificio/crear", methods=["GET", "POST"])
def crear_edificio():
    if request.method == "POST":
        data = {
            "nombre": request.form["nombre"],
            "direccion": request.form["direccion"],
            "ciudad": request.form["ciudad"],
            "tipo": request.form["tipo"]
        }
        r = requests.post("http://127.0.0.1:8000/api/edificios/", json=data, headers=headers)
        if r.status_code in [200, 201]:
            flash("Edificio creado correctamente.", "success")
            return redirect(url_for("los_edificios"))
        else:
            flash("Error al crear el edificio.", "danger")
    return render_template("editar_edificio.html", edificio={})

@app.route("/departamento/crear", methods=["GET", "POST"])
def crear_departamento():
    edificios = requests.get("http://127.0.0.1:8000/api/edificios/", headers=headers).json()
    if request.method == "POST":
        edificio_id = request.form["edificio"]
        # Busca la URL del edificio seleccionado
        edificio_url = ""
        for edificio in edificios:
            if str(edificio.get("id")) == str(edificio_id):
                edificio_url = edificio.get("url", "")
                break
        data = {
            "nombre_propietario": request.form["nombre_propietario"],
            "costo": request.form["costo"],
            "numero_cuartos": request.form["numero_cuartos"],
            "edificio": edificio_url if edificio_url else edificio_id  # Usa URL si existe, si no el ID
        }
        r = requests.post("http://127.0.0.1:8000/api/departamentos/", json=data, headers=headers)
        if r.status_code in [200, 201]:
            flash("Departamento creado correctamente.", "success")
            return redirect(url_for("los_departamentos"))
        else:
            flash("Error al crear el departamento.", "danger")
    return render_template("editar_departamento.html", departamento={}, edificios=edificios)

# Función auxiliar para mostrar el nombre del edificio en el template de departamentos
def obtener_edificio(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get('nombre', 'Sin nombre')
    return "Sin nombre"

app.jinja_env.globals.update(obtener_edificio=obtener_edificio)

if __name__ == "__main__":
    app.run(debug=True)