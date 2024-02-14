# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('materias', views.materias, name='materia'),
    path('materias/crear', views.materiasCrear, name='materia_crear'),
    path('materias/<str:pk>/editar', views.materiasEditar, name='materia_editar'),
    path('cargas', views.cargas, name='carga'),
    path('cargas/crear', views.cargasCrear, name='carga_crear'),
    path('cargas/<str:pk>/editar', views.cargasEditar, name='carga_editar'),
    path('periodos', views.periodos, name='periodo'),
    path('notas/<str:pd>/carga', views.carga_notas, name='carga_notas'),
    path('estudiantes', views.estudiantes, name='estudiante'),
    path('estudiantes/crear', views.estudianteCrear, name='estudiante_crear'),
    path('estudiantes/<str:pk>/editar', views.estudianteEditar, name='estudiante_editar'),

    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),

]
