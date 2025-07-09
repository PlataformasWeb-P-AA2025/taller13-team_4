from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets, permissions
from administrativo.models import Edificio, Departamento
from administrativo.forms import (
    EdificioForm, DepartamentoForm, DepartamentoEdificioForm
)
from administrativo.serializers import (
    EdificioSerializer, DepartamentoSerializer
)

# ---------- Vistas HTML ----------

def index(request):
    edificios = Edificio.objects.all()
    return render(
        request,
        "index.html",
        {"edificios": edificios, "total": edificios.count()},
    )

def obtener_edificio(request, id):
    edificio = get_object_or_404(Edificio, pk=id)
    return render(request, "obtener_edificio.html", {"edificio": edificio})

@login_required(login_url="/entrando/login/")
@permission_required("administrativo.add_edificio", login_url="/entrando/login/")
def crear_edificio(request):
    form = EdificioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(index)
    return render(request, "crear_edificio.html", {"formulario": form})

@login_required(login_url="/entrando/login/")
def editar_edificio(request, id):
    edificio = get_object_or_404(Edificio, pk=id)
    form = EdificioForm(request.POST or None, instance=edificio)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(index)
    return render(request, "crear_edificio.html", {"formulario": form})

def eliminar_edificio(request, id):
    edificio = get_object_or_404(Edificio, pk=id)
    edificio.delete()
    return redirect(index)

# ------ Departamentos (idéntico patrón) ------

def lista_departamentos(request):
    departamentos = Departamento.objects.select_related("edificio")
    return render(request, "lista_departamentos.html", {"departamentos": departamentos})

@login_required(login_url="/entrando/login/")
def crear_departamento(request):
    form = DepartamentoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(lista_departamentos)
    return render(request, "crear_departamento.html", {"formulario": form})

def crear_departamento_edificio(request, id):
    edificio = get_object_or_404(Edificio, pk=id)
    form = DepartamentoEdificioForm(edificio, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(obtener_edificio, id=edificio.id)
    return render(
        request,
        "crear_departamento.html",
        {"formulario": form, "edificio": edificio},
    )

def editar_departamento(request, id):
    departamento = get_object_or_404(Departamento, pk=id)
    form = DepartamentoForm(request.POST or None, instance=departamento)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(lista_departamentos)
    return render(request, "crear_departamento.html", {"formulario": form})

def eliminar_departamento(request, id):
    get_object_or_404(Departamento, pk=id).delete()
    return redirect(lista_departamentos)

# ---------- API REST ----------

class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
