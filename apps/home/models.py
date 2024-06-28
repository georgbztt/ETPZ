
from django.db import models

class PeriodosAcademicos(models.Model):
    id = models.AutoField(primary_key=True)  # Llave primaria autoincremental
    nombre = models.CharField(max_length=255, null=False)  # String de 255 de longitud

    def __str__(self):
        return self.nombre  # Representación en cadena del objeto

    class Meta:
        verbose_name_plural = "Periodos Académicos"  # Nombre en plural para el panel de administración


class DatosPlantel(models.Model):
    id = models.AutoField(primary_key=True)  # Llave primaria autoincremental
    codigo = models.CharField(max_length=255)  # Cadena de texto no nula
    nombre = models.CharField(max_length=255)  # Cadena de texto no nula
    direccion = models.CharField(max_length=255)  # Cadena de texto no nula
    telefono = models.PositiveIntegerField()  # Número no nulo
    municipio = models.CharField(max_length=255)  # Cadena de texto no nula
    entidad_federal = models.CharField(max_length=255)  # Cadena de texto no nula
    zona_educativa = models.CharField(max_length=255)  # Cadena de texto no nula
    distrito_escolar = models.CharField(max_length=255)  # Cadena de texto no nula
    ci_tipo = models.CharField(max_length=1, null=False)  # String de un solo carácter no nulo
    ci = models.PositiveIntegerField(null=False)  # Número no nulo
    director = models.CharField(max_length=255)
    periodo = models.ForeignKey(PeriodosAcademicos, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre  # Representación en cadena del objeto

    class Meta:
        verbose_name_plural = "Datos Plantel"  # Nombre en plural para el panel de administración

class Anios(models.Model):
    id = models.AutoField(primary_key=True)  # Llave primaria autoincremental
    nombre = models.CharField(max_length=255, null=False)  # Cadena de texto no nula

    def __str__(self):
        return self.nombre  # Representación en cadena del objeto

    class Meta:
        verbose_name_plural = "Años"  # Nombre en plural para el panel de administración

class Menciones(models.Model):
    id = models.AutoField(primary_key=True)  # Llave primaria autoincremental
    nombre = models.CharField(max_length=255, null=False, unique=True)  # String de 255 de longitud
    nombre_abrev = models.CharField(max_length=5, null=False, unique=True)  # String de 255 de longitud

    def __str__(self):
        return self.nombre  # Representación en cadena del objeto

    class Meta:
        verbose_name_plural = "Menciones"  # Nombre en plural para el panel de administración

class Secciones(models.Model):
    id = models.AutoField(primary_key=True)  # Llave primaria autoincremental
    nombre = models.CharField(max_length=3, null=False, unique=True)  # String de 3 de longitud

    def __str__(self):
        return self.nombre  # Representación en cadena del objeto

    class Meta:
        verbose_name_plural = "Secciones"  # Nombre en plural para el panel de administración

class AniosMencionSec(models.Model):
    anio = models.ForeignKey(Anios, on_delete=models.CASCADE)
    mencion = models.ForeignKey(Menciones, on_delete=models.CASCADE)
    seccion= models.ForeignKey(Secciones, on_delete=models.CASCADE) # Representación en cadena del objeto

    class Meta:
        verbose_name_plural = "Años Menciones Secciones"
        constraints = [
            models.UniqueConstraint(fields=['anio', 'mencion', 'seccion'], name='unique_anio_mencion_seccion')
        ]

class Materias(models.Model):
    nombre = models.CharField(max_length=255, null=False, unique=True)  # String de 255 de longitud
    nombre_abrev = models.CharField(max_length=4, null=False, unique=True)  # String de 4 de longitud

    def __str__(self):
        return self.nombre  # Representación en cadena del objeto

    class Meta:
        verbose_name_plural = "Materias"  # Nombre en plural para el panel de administración

class MateriasAniosMenciones(models.Model):
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    anio = models.ForeignKey(Anios, on_delete=models.CASCADE)
    mencion = models.ForeignKey(Menciones, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.materia.nombre} - {self.anio.nombre} - {self.mencion.nombre}"

    class Meta:
        verbose_name_plural = "Materias Años Menciones"
        constraints = [
            models.UniqueConstraint(fields=['materia', 'anio', 'mencion'], name='unique_materia_anio_mencion')
        ]

class Estudiantes(models.Model):
    id = models.AutoField(primary_key=True)  # Llave primaria autoincremental
    ci_tipo = models.CharField(max_length=1, null=False)  # String de un solo carácter no nulo
    ci = models.PositiveIntegerField(null=False)  # Número no nulo
    nombres = models.CharField(max_length=255)  # Cadena de texto no nula
    apellidos = models.CharField(max_length=255)  # Cadena de texto no nula
    sexo = models.CharField(max_length=255)
    fecha_de_nacimiento = models.DateField()
    anio = models.ForeignKey(Anios, on_delete=models.CASCADE)
    mencion = models.ForeignKey(Menciones, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Secciones, on_delete=models.CASCADE)  
    entidad_federal = models.CharField(max_length=3)  # Cadena de texto no nula
    lugar_de_nacimiento = models.CharField(max_length=255)  # Cadena de texto no nula
    estado = models.PositiveIntegerField(null=True)
    
    def __str__(self):
        return f'{self.nombres}'
    
    class Meta:
        verbose_name_plural = "Estudiantes"  # Nombre en plural para el panel de administración


class Profesor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    ci_tipo = models.CharField(max_length=1, null=False)
    ci = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.nombre
    

class EstudiantesMaterias(models.Model):
    materia = models.ForeignKey(MateriasAniosMenciones, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE)

    def __str__(self):
        return self.materia.materia.nombre
    

class Notas(models.Model):
    estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE)
    materia = models.ForeignKey(MateriasAniosMenciones, on_delete=models.CASCADE)
    lapso1 = models.PositiveIntegerField(default=0, null=True)
    lapso2 = models.PositiveIntegerField(default=0, null=True)
    lapso3 = models.PositiveIntegerField(default=0, null=True)
    definitiva = models.PositiveIntegerField(default=0, null=True)
    revision = models.PositiveIntegerField(default=0, null=True)
    periodo = models.ForeignKey(PeriodosAcademicos, on_delete=models.CASCADE, null=True)
    anio = models.ForeignKey(Anios, on_delete=models.CASCADE, null=True)
    mencion = models.ForeignKey(Menciones, on_delete=models.CASCADE, null=True)
    seccion= models.ForeignKey(Secciones, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.estudiante.nombres