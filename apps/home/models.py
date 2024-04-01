from email.policy import default
from pyexpat import model
from tokenize import blank_re
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
    lugar_de_nacimiento = models.CharField(max_length=30, null=True)
    entidad_federal = models.CharField(max_length=30, null=True)
    periodo = models.ForeignKey('home.Periodo', on_delete=models.SET_NULL, blank=True, null=True)#Relación a periodo para asignar carga y tomar en cuenta en carga de notas
    periodo_completo = models.BooleanField(default=False)#Filtro para excluir de la carga de notas una vez fue cargada la nota
    seccion = models.CharField(max_length=1, null=True)

    class Meta:
        verbose_name = ("Estudiante")
        verbose_name_plural = ("Estudiantes")

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def otros_periodos(self):
        return Periodo.objects.filter(nota__estudiante=self).exclude(id=self.periodo_id).distinct()
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
    literales = models.BooleanField(default=False)

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

    fecha = models.CharField(max_length=30, null=True)
    carga = models.ForeignKey('home.Carga', on_delete=models.RESTRICT, null=True)

    class Meta:
        verbose_name = ("Periodo")
        verbose_name_plural = ("Periodos")

    def __str__(self):
        return f'{self.fecha} {self.carga.titulo}'

class Nota(models.Model):

    estudiante = models.ForeignKey('home.Estudiante', on_delete=models.CASCADE, null=True)
    periodo = models.ForeignKey('home.Periodo', on_delete=models.RESTRICT, null=True)#Relación a periodo para agrupar notas las notas y mantener un registro histórico
    materia = models.ForeignKey('home.Materia', on_delete=models.RESTRICT, null=True)
    lapso_1 = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|IN)$')], blank=True, null=True)
    lapso_2 = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|IN)$')], blank=True, null=True)
    lapso_3 = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|IN)$')], blank=True, null=True)
    inasistencia_1 = models.IntegerField(validators=[int_list_validator(allow_negative=False)], default=0, blank=True, null=True)
    inasistencia_2 = models.IntegerField(validators=[int_list_validator(allow_negative=False)], default=0, blank=True, null=True)
    inasistencia_3 = models.IntegerField(validators=[int_list_validator(allow_negative=False)], default=0, blank=True, null=True)
    reparacion = models.CharField(max_length=2, validators=[MinLengthValidator(2), RegexValidator(r'^([0-1][0-9]|20|IN)$')], blank=True, null=True)
    #promedio = models.CharField(max_length=2, blank=True, null=True)

    @property
    def promedio(self):
        lapsos = [self.lapso_1, self.lapso_2, self.lapso_3]
        lapsos_numericos = [int(lapso) for lapso in lapsos if lapso.isdigit()]
        if lapsos_numericos:
            promedio = sum(lapsos_numericos) / len(lapsos_numericos)
            return '{:02d}'.format(int(promedio))
        return None
    class Meta:
        verbose_name = ("Nota")
        verbose_name_plural = ("Notas")

    def __str__(self):
        return str(self.estudiante)
