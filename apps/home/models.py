from email.policy import default
from pyexpat import model
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
    periodo = models.ForeignKey('home.Periodo', on_delete=models.SET_NULL, null=True)
    periodo_completo = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Estudiante")
        verbose_name_plural = ("Estudiantes")

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Boleta(models.Model):

    estudiante = models.ForeignKey('home.Estudiante', on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(null=True)

    class Meta:
        verbose_name = ("Boleta")
        verbose_name_plural = ("Boletas")

    def __str__(self):
        return f'{self.estudiante.nombre} {self.estudiante.apellido} - {self.periodo}'

class Materia(models.Model):

    nombre = models.CharField(max_length=30, unique=True, null=True)

    class Meta:
        verbose_name = ("Materia")
        verbose_name_plural = ("Materias")

    def __str__(self):
        return self.nombre

class Carga(models.Model):

    titulo = models.CharField(max_length=30, null=True)
    materias = models.ManyToManyField(Materia)

    class Meta:
        verbose_name = ("Carga ")
        verbose_name_plural = ("Cargas")

    def __str__(self):
        return self.titulo 

class Periodo(models.Model):

    fecha = models.DateField(null=True)
    carga = models.ForeignKey('home.Carga', on_delete=models.RESTRICT, null=True)

    class Meta:
        verbose_name = ("Periodo")
        verbose_name_plural = ("Periodos")

    def __str__(self):
        return f'{self.fecha} {self.carga.titulo}'

class Nota(models.Model):

    estudiante = models.ForeignKey('home.Estudiante', on_delete=models.SET_NULL, null=True)
    materia = models.ForeignKey('home.Materia', on_delete=models.RESTRICT, null=True)
    lapso_1 = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|NA)$')], null=True)
    lapso_2 = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|NA)$')], null=True)
    lapso_3 = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|NA)$')], null=True)
    promedio = models.CharField(max_length=2, blank=True, null=True)
    reparacion = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|NA)$')], blank=True, null=True)

    class Meta:
        verbose_name = ("Nota")
        verbose_name_plural = ("Notas")

    def __str__(self):
        return self.estudiante.ci
