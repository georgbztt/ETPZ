# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime, decimal
from email import message
from itertools import count
from re import T
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
    return redirect('estudiante')
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
def materias(request):
    materias = Materia.objects.all()

    buscar = request.GET.get('buscar')#Tomar texto del buscador
    if buscar:#Si exste, filtrar
        materias = materias.filter(Q(nombre__icontains=buscar))

    table = 'home/table-content/materias.html'
    context={
        'materias':materias,
        'segment':'materia',
        'title':'Materias',
        'buscar':True,
        'table':table,
        'url_crear':'/materias/crear'
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':#Evaluar si es una petición AJAX
        table_html = render_to_string(table, context, request)#Rendereziar los datos en una plantilla de tabla reducida
        return JsonResponse({'table_html': table_html, })#JsonResponse para manejar con JavaScript y recargar un segmento de la página

    return render(request, 'home/table.html', context)

@login_required
@permission_required('home.add_estudiante', raise_exception=True)#type:ignore
def materiaCrear(request):
    form = materiaForm(request.POST or None)
    content = 'home/form-content/materia_form.html'
    context = {
        'form':form,
        'segment':'materia',
        'title':'Registrar Materia',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('materia')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required
@permission_required('home.change_materia', raise_exception=True)#type:ignore
def materiaEditar(request, pk):
    obj = get_object_or_404(Materia, pk=pk)
    form = materiaForm(request.POST or None, instance=obj)
    content = 'home/form-content/materia_form.html'
    context = {
        'form':form,
        'segment':'materia',
        'title':'Editar Materia',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('materia')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required(login_url="/login/")
@permission_required('home.delete_materia', raise_exception=True)#Validar permiso
def materiaEliminar(request, pk):
    materia = get_object_or_404(Materia, pk=pk)#Obtener el materia a eliminar
    materia.delete()#Eliminar

    if 'next' in request.GET:
        return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
    return redirect('materia')#Redireccionar normalmente

@login_required(login_url="/login/")
def cargas(request):
    cargas = Carga.objects.all()

    buscar = request.GET.get('buscar')#Tomar texto del buscador
    if buscar:#Si exste, filtrar
        cargas = cargas.filter(Q(titulo__icontains=buscar))

    table = 'home/table-content/cargas.html'
    context={
        'cargas':cargas,
        'segment':'carga',
        'title':'Cargas académicas',
        'buscar':True,
        'table':table,
        'url_crear':'/cargas/crear'
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':#Evaluar si es una petición AJAX
        table_html = render_to_string(table, context, request)#Rendereziar los datos en una plantilla de tabla reducida
        return JsonResponse({'table_html': table_html, })#JsonResponse para manejar con JavaScript y recargar un segmento de la página

    return render(request, 'home/table.html', context)

@login_required
@permission_required('home.add_carga', raise_exception=True)#type:ignore
def cargaCrear(request):
    form = cargaForm(request.POST or None)
    content = 'home/form-content/carga_form.html'
    context = {
        'form':form,
        'segment':'carga',
        'title':'Registrar Carga académica',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('carga')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required
@permission_required('home.change_carga', raise_exception=True)#type:ignore
def cargaEditar(request, pk):
    obj = get_object_or_404(Carga, pk=pk)
    form = cargaForm(request.POST or None, instance=obj)
    content = 'home/form-content/carga_form.html'
    context = {
        'form':form,
        'segment':'carga',
        'title':'Editar Carga académica',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('carga')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required(login_url="/login/")
@permission_required('home.delete_carga', raise_exception=True)#Validar permiso
def cargaEliminar(request, pk):
    carga = get_object_or_404(Carga, pk=pk)#Obtener la carga a eliminar
    carga.delete()#Eliminar

    if 'next' in request.GET:
        return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
    return redirect('carga')#Redireccionar normalmente

@login_required(login_url="/login/")
def estudiantes(request):
    estudiantes = Estudiante.objects.all().order_by('ci')

    buscar = request.GET.get('buscar')#Tomar texto del buscador
    if buscar:#Si exste, filtrar
        estudiantes = estudiantes.filter(Q(nombre__icontains=buscar)|Q(apellido__icontains=buscar)|Q(entidad_federal__icontains=buscar)|Q(periodo__carga__titulo__icontains=buscar)|Q(periodo__fecha__icontains=buscar)|Q(ci__icontains=buscar))#Filtros

    table = 'home/table-content/estudiantes.html'
    context={
        'estudiantes':estudiantes,
        'segment':'estudiante',
        'title':'Estudiantes',
        'buscar':True,
        'table':table,
        'url_crear':'/estudiantes/crear'
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':#Evaluar si es una petición AJAX
        table_html = render_to_string(table, context, request)#Rendereziar los datos en una plantilla de tabla reducida
        #paginator_html = render_to_string('home/paginator.html', context, request)#Rendereziar el paginador actualizado 'paginator_html': paginator_html
        return JsonResponse({'table_html': table_html, })#JsonResponse para manejar con JavaScript y recargar un segmento de la página

    return render(request, 'home/table.html', context)

@login_required(login_url="/login/")
@permission_required('home.view_estudiante', raise_exception=True)#Validar permiso
def estudianteVer(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)#Obtener el estudiante a eliminar
    notas = Nota.objects.filter(Q(estudiante_id=pk)|Q(periodo=estudiante.periodo))
    return render(request, 'home/perfil_estudiante.html', {'estudiante':estudiante, 'notas':notas, 'segment':'estudiante'})#Redireccionar normalmente

@login_required
@permission_required('home.add_estudiante', raise_exception=True)#type:ignore
def estudianteCrear(request):
    form = estudianteForm(request.POST or None)
    content = 'home/form-content/estudiante_form.html'
    context = {
        'form':form,
        'segment':'estudiante',
        'title':'Registrar Estudiante',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('estudiante')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required
@permission_required('home.change_estudiante', raise_exception=True)#type:ignore
def estudianteEditar(request, pk):
    obj = get_object_or_404(Estudiante, pk=pk)
    form = estudianteForm(request.POST or None, instance=obj)
    content = 'home/form-content/estudiante_form.html'
    context = {
        'form':form,
        'segment':'estudiante',
        'title':'Editar Estudiante',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('estudiante')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required(login_url="/login/")
@permission_required('home.delete_estudiante', raise_exception=True)#Validar permiso
def estudianteEliminar(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)#Obtener el estudiante a eliminar
    estudiante.delete()#Eliminar

    if 'next' in request.GET:
        return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
    return redirect('estudiante')#Redireccionar normalmente

@login_required(login_url="/login/")
def carga_notas(request, pd):
    
    periodo = get_object_or_404(Periodo, pk=pd)
    carga = periodo.carga
    estudiantes = Estudiante.objects.filter(periodo=periodo).order_by("ci").exclude(periodo_completo=True)[:10]
    if not estudiantes:
        return render(request, 'home/carga_de_notas.html', {'fail_message':'No hay estudiantes pendientes por cargas en este periodo'})
    
    materias = carga.materias.all().order_by("nombre")
    
    cantidad_materias = materias.count()
    total_forms = cantidad_materias * estudiantes.count()
    
    NotasFormSet = modelformset_factory(Nota, fields='__all__', extra=total_forms)
    formset = NotasFormSet(request.POST or None)
    
    if request.POST:
        notas = formset.save(commit=False)
        print(notas)
        for nota in notas:
            lapsos = [] 

            lapsos = [int(nota.lapso_1), int(nota.lapso_2), int(nota.lapso_3)]
            lapsos = [lapso for lapso in lapsos if lapso != 'IN']

            if lapsos:
                suma = sum(lapsos) / len(lapsos)
                promedio = "{:.1f}".format(suma)
                nota.promedio = promedio.zfill(2)
            nota.periodo = periodo
            nota.save()
            
            print(f'{nota.estudiante.nombre} {nota.estudiante.apellido} {nota.materia.nombre} = {nota.promedio}')
        
        for estudiante in estudiantes:
            estudiante.periodo_completo = True
            estudiante.save()

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

@login_required(login_url="/login/")
def periodos(request):
    periodos = Periodo.objects.all().annotate(num_estudiantes=Count('estudiante'))

    buscar = request.GET.get('buscar')#Tomar texto del buscador
    if buscar:#Si exste, filtrar
        periodos = periodos.filter(Q(fecha__icontains=buscar)|Q(carga__titulo__icontains=buscar))

    table = 'home/table-content/periodos.html'

    context={
        'periodos':periodos,
        'segment':'periodo',
        'title':'Periodos',
        'buscar':True,
        'table':table,
        'url_crear':'/periodos/crear'
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':#Evaluar si es una petición AJAX
        table_html = render_to_string(table, context, request)#Rendereziar los datos en una plantilla de tabla reducida
        return JsonResponse({'table_html': table_html, })#JsonResponse para manejar con JavaScript y recargar un segmento de la página
        
    return render(request, 'home/table.html', context)

@login_required
@permission_required('home.add_periodo', raise_exception=True)#type:ignore
def periodoCrear(request):
    form = periodoForm(request.POST or None)
    content = 'home/form-content/periodo_form.html'
    context = {
        'form':form,
        'segment':'periodo',
        'title':'Registrar Periodo académico',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('periodo')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required
@permission_required('home.change_periodo', raise_exception=True)#type:ignore
def periodoEditar(request, pk):
    obj = get_object_or_404(Periodo, pk=pk)
    form = periodoForm(request.POST or None, instance=obj)
    content = 'home/form-content/periodo_form.html'
    context = {
        'form':form,
        'segment':'periodo',
        'title':'Editar Periodo académico',
        'content':content
    }
    if request.POST:
        if form.is_valid():
            form.save(commit=False)
            #validación
            form.save()
            return redirect('periodo')
        else:
            print(form.errors)
    
    return render(request, 'layouts/form.html', context)

@login_required(login_url="/login/")
@permission_required('home.delete_periodo', raise_exception=True)#Validar permiso
def periodoEliminar(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)#Obtener la periodo a eliminar
    periodo.delete()#Eliminar

    if 'next' in request.GET:
        return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
    return redirect('periodo')#Redireccionar normalmente

