from flask import Flask, render_template, request, redirect, url_for, flash, abort
import requests
from config import token

app = Flask(__name__, template_folder="templates")
app.secret_key = "flask-demo-secret"

HEADERS = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json",
}

# ───────── helpers ─────────
def get_json(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    abort(r.status_code)

def id_from_url(url):
    return int(url.rstrip("/").split("/")[-1])

# ───────── LISTAR ─────────
@app.route("/")
def lista_edificios():
    data = get_json("http://127.0.0.1:8000/api/edificios/")
    edificios = [{**e, "id": id_from_url(e["url"])} for e in data["results"]]
    return render_template(
        "losedificios.html",
        edificios=edificios,
        numero_edificios=data["count"],
    )

@app.route("/departamentos")
def lista_departamentos():
    raw = get_json("http://127.0.0.1:8000/api/departamentos/")["results"]
    departamentos = [
        {
            **d,
            "id": id_from_url(d["url"]),
            "edificio": get_json(d["edificio"])["nombre"],
        }
        for d in raw
    ]
    return render_template(
        "losdepartamentos.html",
        departamentos=departamentos,
        numero_departamentos=len(departamentos),
    )

# ───────── CREAR ─────────
@app.route("/crear_edificio", methods=["GET", "POST"])
def crear_edificio():
    if request.method == "POST":
        payload = {
            "nombre": request.form["nombre"],
            "direccion": request.form["direccion"],
            "ciudad": request.form["ciudad"],
            "tipo": request.form["tipo"],
        }
        r = requests.post("http://127.0.0.1:8000/api/edificios/", json=payload, headers=HEADERS)
        flash("Edificio creado" if r.status_code == 201 else "Error")
        return redirect(url_for("lista_edificios"))
    return render_template("crear_edificio.html")

@app.route("/crear_departamento", methods=["GET", "POST"])
def crear_departamento():
    edificios = get_json("http://127.0.0.1:8000/api/edificios/")["results"]
    if request.method == "POST":
        payload = {
            "nombre_propietario": request.form["nombre_propietario"],
            "costo": request.form["costo"],
            "numero_cuartos": request.form["numero_cuartos"],
            "edificio": request.form["edificio"],
        }
        r = requests.post("http://127.0.0.1:8000/api/departamentos/", json=payload, headers=HEADERS)
        flash("Departamento creado" if r.status_code == 201 else "Error")
        return redirect(url_for("lista_departamentos"))
    return render_template("crear_departamento.html", edificios=edificios)

# ───────── EDITAR ─────────
@app.route("/editar_edificio/<int:id>", methods=["GET", "POST"])
def editar_edificio(id):
    e = get_json(f"http://127.0.0.1:8000/api/edificios/{id}/")
    if request.method == "POST":
        payload = {
            "nombre": request.form["nombre"],
            "direccion": request.form["direccion"],
            "ciudad": request.form["ciudad"],
            "tipo": request.form["tipo"],
        }
        r = requests.put(f"http://127.0.0.1:8000/api/edificios/{id}/", json=payload, headers=HEADERS)
        flash("Actualizado" if r.status_code == 200 else "Error")
        return redirect(url_for("lista_edificios"))
    return render_template("editar_edificio.html", e=e)

@app.route("/editar_departamento/<int:id>", methods=["GET", "POST"])
def editar_departamento(id):
    d = get_json(f"http://127.0.0.1:8000/api/departamentos/{id}/")
    edificios = get_json("http://127.0.0.1:8000/api/edificios/")["results"]
    if request.method == "POST":
        payload = {
            "nombre_propietario": request.form["nombre_propietario"],
            "costo": request.form["costo"],
            "numero_cuartos": request.form["numero_cuartos"],
            "edificio": request.form["edificio"],
        }
        r = requests.put(
            f"http://127.0.0.1:8000/api/departamentos/{id}/", json=payload, headers=HEADERS
        )
        flash("Actualizado" if r.status_code == 200 else "Error")
        return redirect(url_for("lista_departamentos"))
    return render_template("editar_departamento.html", d=d, edificios=edificios)

# ───────── ELIMINAR ─────────
@app.route("/eliminar_edificio/<int:id>")
def eliminar_edificio(id):
    r = requests.delete(f"http://127.0.0.1:8000/api/edificios/{id}/", headers=HEADERS)
    flash("Eliminado" if r.status_code == 204 else "Error")
    return redirect(url_for("lista_edificios"))

@app.route("/eliminar_departamento/<int:id>")
def eliminar_departamento(id):
    r = requests.delete(f"http://127.0.0.1:8000/api/departamentos/{id}/", headers=HEADERS)
    flash("Eliminado" if r.status_code == 204 else "Error")
    return redirect(url_for("lista_departamentos"))

if __name__ == "__main__":
    app.run(debug=True)
