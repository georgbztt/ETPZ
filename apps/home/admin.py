from django.contrib import admin
from django.template.loader import get_template
from django.contrib.admin.options import TabularInline
from .models import DatosPlantel, Secciones, AniosMencionSec, Anios, Menciones, PeriodosAcademicos, Materias, MateriasAniosMenciones, Estudiantes

admin.site.register(DatosPlantel)
admin.site.register(Secciones)
admin.site.register(AniosMencionSec)
admin.site.register(Anios)
admin.site.register(Menciones)
admin.site.register(PeriodosAcademicos)
admin.site.register(Materias)
admin.site.register(MateriasAniosMenciones)
admin.site.register(Estudiantes)
