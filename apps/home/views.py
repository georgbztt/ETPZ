# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime, decimal
from itertools import count
from urllib import request
from django import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms import modelformset_factory
from django.template import loader
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required

from .models import *
from .forms import *

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    return render(request, 'home/index.html', context)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

#----------------------------------------------------------------------------------
@login_required(login_url="/login/")
def periodos(request):
    periodos = Periodo.objects.all().annotate(num_estudiantes=Count('estudiante'))

    context={
        'periodos':periodos,
        'segment':'periodo',
        'title':'Periodos',
        'table':'home/table-content/periodos.html',
    }

    return render(request, 'home/table.html', context)


@login_required(login_url="/login/")
def carga_notas(request, pd):
    
    periodo = get_object_or_404(Periodo, pk=pd)
    carga = periodo.carga
    materias = carga.materias.all().order_by("nombre")
    estudiantes = Estudiante.objects.filter(periodo=periodo).order_by("ci")

    cantidad_materias = materias.count()
    total_forms = cantidad_materias * estudiantes.count()
    
    NotasFormSet = modelformset_factory(Nota, fields='__all__', extra=total_forms)
    formset = NotasFormSet(request.POST or None)
    
    if request.POST:
        notas = formset.save(commit=False)
        print(notas)
        for nota in notas:#Co digo spagueti, pendiente por optimizar ``
            lapsos = []
            if nota.lapso_1 != 'NA':
                lapsos.append(int(nota.lapso_1))
            if nota.lapso_2 != 'NA':
                lapsos.append(int(nota.lapso_2))
            if nota.lapso_3 != 'NA':
                lapsos.append(int(nota.lapso_3))
            suma = sum(lapsos) / len(lapsos)
            promedio = str(decimal.Decimal(suma).quantize(decimal.Decimal('0'),rounding=decimal.ROUND_HALF_UP))
            nota.promedio = promedio.zfill(2)
            print(f'{nota.estudiante.nombre} {nota.estudiante.apellido} {nota.materia.nombre} = {nota.promedio}')

    context = {
        'periodo': periodo,
        'carga': carga,
        'materias': materias,
        'cantidad_materias': cantidad_materias,
        'estudiantes': estudiantes,
        'formset': formset,
        'segment': 'carga'
        }

    return render(request, 'home/carga_de_notas.html', context)

