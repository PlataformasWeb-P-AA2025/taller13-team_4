from django.db import models

# Create your models here.


class Edificio(models.Model):
    TIPOS = (
        ("residencial", "Residencial"),
        ("comercial", "Comercial"),
    )
    nombre = models.CharField(max_length=80)
    direccion = models.CharField(max_length=120)
    ciudad = models.CharField(max_length=60)
    tipo = models.CharField(max_length=12, choices=TIPOS)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"


class Departamento(models.Model):
    nombre_propietario = models.CharField(max_length=120)
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    numero_cuartos = models.PositiveSmallIntegerField()
    edificio = models.ForeignKey(
        Edificio, on_delete=models.CASCADE, related_name="departamentos"
    )

    def __str__(self):
        return f"{self.nombre_propietario} – {self.edificio.nombre}"