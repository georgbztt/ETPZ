from django.contrib import admin
from django.template.loader import get_template
from django.contrib.admin.options import TabularInline
from .models import DatosPlantel, Secciones, AniosMencionSec, Anios, Menciones, PeriodosAcademicos, Materias, MateriasAniosMenciones, Estudiantes, EstudiantesMaterias, Notas

class EstudiantesMateriasAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia')

class MateriasAniosMencionesAdmin(admin.ModelAdmin):
    list_display = ('materia', 'anio', 'mencion')

class AniosMencionSecAdmin(admin.ModelAdmin):
    list_display = ('anio', 'mencion', 'seccion')

admin.site.register(DatosPlantel)
admin.site.register(Secciones)
admin.site.register(AniosMencionSec, AniosMencionSecAdmin)
admin.site.register(Anios)
admin.site.register(Menciones)
admin.site.register(PeriodosAcademicos)
admin.site.register(Materias)
admin.site.register(MateriasAniosMenciones, MateriasAniosMencionesAdmin)
admin.site.register(Estudiantes)
admin.site.register(Notas)

admin.site.register(EstudiantesMaterias, EstudiantesMateriasAdmin)
