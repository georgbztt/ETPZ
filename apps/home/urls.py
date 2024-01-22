# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('periodos', views.periodos, name='periodo'),
    path('notas/<str:pd>/carga', views.carga_notas, name='carga_notas'),
    path('estudiantes', views.estudiantes, name='estudiante'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
