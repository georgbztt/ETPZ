from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *

class Estudiante(models.Model):
    CI_OPT=(
        ('V', 'V'),
        ('E', 'E')
    )

    ci = models.CharField(max_length=10, validators=[MinLengthValidator(7), RegexValidator(r'^[0-9]{1,2}[.]?[0-9]{3}[.]?[0-9]{3}$')], unique=True, null=True)
    ci_tipo = models.CharField(max_length=1, choices=CI_OPT, null=True)
    nombre = models.CharField(max_length=30, null=True)
    apellido = models.CharField(max_length=30, null=True)
    entidad_federal = models.CharField(max_length=30, null=True)
    # periodo = models.OneToOneField("home.Estudiante", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = ("Estudiante")
        verbose_name_plural = ("Estudiantes")

    def __str__(self):
        return f'{self.nombre} {self.apellido}'



class Boleta(models.Model):

    carga = models.ForeignKey('home.Carga', on_delete=models.CASCADE, null=True)
    sección = models.CharField(max_length=1, null=True)
    estudiante = models.ForeignKey('home.Estudiante', on_delete=models.CASCADE, null=True)
    periodo = models.CharField(max_length=30, null=True)
    fecha = models.DateField(null=True)

    class Meta:
        verbose_name = ("Boleta")
        verbose_name_plural = ("Boletas")

    def __str__(self):
        return f'{self.estudiante.nombre} {self.estudiante.apellido} - {self.periodo}'

class Materia(models.Model):

    nombre = models.CharField(max_length=30, null=True)

    class Meta:
        verbose_name = ("Materia")
        verbose_name_plural = ("Materias")

    def __str__(self):
        return self.nombre

class Carga(models.Model):

    titulo = models.CharField(max_length=30, null=True)
    materias = models.ManyToManyField(Materia)

    class Meta:
        verbose_name = ("Periodo")
        verbose_name_plural = ("Periodos")

    def __str__(self):
        return self.titulo 

class Nota(models.Model):

    boleta = models.ForeignKey('home.Boleta', on_delete=models.CASCADE, null=True)
    lapso_1 = models.CharField(max_length=2, blank=True, null=True)
    lapso_2 = models.CharField(max_length=2, blank=True, null=True)
    lapso_3 = models.CharField(max_length=2, blank=True, null=True)
    reparacion = models.CharField(max_length=2, blank=True, null=True)
    promedio = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = ("Nota")
        verbose_name_plural = ("Notas")

    def __str__(self):
        return str(self.boleta)

