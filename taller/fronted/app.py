from flask import Flask, render_template, request, redirect, url_for, flash
import requests, json
from config import usuario, clave

app = Flask(__name__, template_folder="templates")
app.secret_key = "flask-demo-secret"

# ───────────────────────
#  LISTADOS
# ───────────────────────
@app.route("/")
def root():
    return redirect(url_for("losedificios"))

@app.route("/losedificios")
def losedificios():
    r = requests.get(
        "http://127.0.0.1:8000/api/edificios/",
        auth=(usuario, clave)
    )
    edificios   = json.loads(r.content)["results"]
    total_edifs = json.loads(r.content)["count"]
    return render_template(
        "losedificios.html",
        edificios=edificios,
        numero_edificios=total_edifs,
    )

def obtener_nombre_edificio(url):
    r = requests.get(url, auth=(usuario, clave))
    return json.loads(r.content)["nombre"]

@app.route("/losdepartamentos")
def losdepartamentos():
    r = requests.get(
        "http://127.0.0.1:8000/api/departamentos/",
        auth=(usuario, clave)
    )
    departamentos_raw = json.loads(r.content)["results"]
    total_deps        = json.loads(r.content)["count"]

    departamentos = [
        {
            "nombre_propietario": d["nombre_propietario"],
            "costo": d["costo"],
            "numero_cuartos": d["numero_cuartos"],
            "edificio": obtener_nombre_edificio(d["edificio"]),
        }
        for d in departamentos_raw
    ]
    return render_template(
        "losdepartamentos.html",
        departamentos=departamentos,
        numero_departamentos=total_deps,
    )

# ───────────────────────
#  CREAR REGISTROS
# ───────────────────────
@app.route("/crear_edificio", methods=["GET", "POST"])
def crear_edificio():
    if request.method == "POST":
        payload = {
            "nombre":    request.form["nombre"],
            "direccion": request.form["direccion"],
            "ciudad":    request.form["ciudad"],
            "tipo":      request.form["tipo"],
        }
        r = requests.post(
            "http://127.0.0.1:8000/api/edificios/",
            json=payload,
            auth=(usuario, clave),
        )
        flash("Edificio creado ✔" if r.status_code == 201 else "Error ❌")
        return redirect(url_for("losedificios"))
    return render_template("crear_edificio.html")

@app.route("/crear_departamento", methods=["GET", "POST"])
def crear_departamento():
    # Traer edificios para el <select>
    edifs = requests.get(
        "http://127.0.0.1:8000/api/edificios/",
        auth=(usuario, clave)
    ).json()["results"]

    if request.method == "POST":
        payload = {
            "nombre_propietario": request.form["nombre_propietario"],
            "costo":              request.form["costo"],
            "numero_cuartos":     request.form["numero_cuartos"],
            "edificio":           request.form["edificio"],  # URL completa
        }
        r = requests.post(
            "http://127.0.0.1:8000/api/departamentos/",
            json=payload,
            auth=(usuario, clave),
        )
        flash("Departamento creado ✔" if r.status_code == 201 else "Error ❌")
        return redirect(url_for("losdepartamentos"))
    return render_template("crear_departamento.html", edificios=edifs)

# ───────────────────────
if __name__ == "__main__":
    app.run(debug=True)
