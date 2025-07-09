from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from administrativo.models import Edificio, Departamento

class EdificioForm(ModelForm):
    class Meta:
        model = Edificio
        fields = "__all__"
        labels = {
            "nombre": _("Nombre del edificio"),
            "direccion": _("Dirección"),
            "ciudad": _("Ciudad"),
            "tipo": _("Tipo"),
        }

class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        fields = "__all__"

class DepartamentoEdificioForm(ModelForm):
    """Formulario que oculta el edificio y lo fija al que recibimos"""
    def __init__(self, edificio, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["edificio"] = edificio
        self.fields["edificio"].widget = forms.widgets.HiddenInput()

    class Meta:
        model = Departamento
        fields = "__all__"
