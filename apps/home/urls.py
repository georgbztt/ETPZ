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
    path('materias/crear', views.materiaCrear, name='materia_crear'),
    path('materias/<str:pk>/editar', views.materiaEditar, name='materia_editar'),
    path('materias/<str:pk>/eliminar', views.materiaEliminar, name='materia_eliminar'),

    path('cargas', views.cargas, name='carga'),
    path('cargas/crear', views.cargaCrear, name='carga_crear'),
    path('cargas/<str:pk>/editar', views.cargaEditar, name='carga_editar'),
    path('cargas/<str:pk>/eliminar', views.cargaEliminar, name='carga_eliminar'),

    path('estudiantes', views.estudiantes, name='estudiante'),
    path('estudiantes/<str:pk>', views.estudianteVer, name='estudiante_ver'),
    path('estudiantes/crear', views.estudianteCrear, name='estudiante_crear'),
    path('estudiantes/<str:pk>/editar', views.estudianteEditar, name='estudiante_editar'),
    path('estudiantes/<str:pk>/eliminar', views.estudianteEliminar, name='estudiante_eliminar'),

    path('notas/<str:pd>/carga', views.carga_notas, name='carga_notas'),
    path('periodos', views.periodos, name='periodo'),
    path('periodos/crear', views.periodoCrear, name='periodo_crear'),
    path('periodos/<str:pk>/editar', views.periodoEditar, name='periodo_editar'),
    path('periodos/<str:pk>/eliminar', views.periodoEliminar, name='periodo_eliminar'),


    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),

]
