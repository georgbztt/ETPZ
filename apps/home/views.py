# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime, decimal
from email import message
from itertools import count
from multiprocessing import context
from re import T
from urllib import request
from django import template
from django.db import transaction 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms import formset_factory
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
def estudianteVer(request, pk, dir, periodo_sel):
    estudiante = get_object_or_404(Estudiante, id=pk)#Obtener el estudiante a eliminar
    notas = Nota.objects.filter(Q(estudiante_id=pk), Q(periodo=estudiante.periodo))
    otro_p, otro_p_id = None, None
    otros_periodos = estudiante.otros_periodos
    if dir == 'imp':
        plantilla = 'layouts/imprimir_notas.html'
    elif dir == 'ver':
        plantilla = 'home/perfil_estudiante.html'
    if periodo_sel:
        try:
            int(periodo_sel)
            otro_p = get_object_or_404(Periodo, id=periodo_sel)
            notas = Nota.objects.filter(Q(estudiante_id=pk), Q(periodo=otro_p))
            otro_p_id = otro_p.id 
        except:
            print('f')
    context = {
        'estudiante':estudiante,
        'notas':notas,
        'otros_periodos':otros_periodos,
        'segment':'estudiante',
        'otro_p':otro_p,
        'otro_p_id':otro_p_id
        }
    return render(request, plantilla, context)#Redireccionar normalmente

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
            e = form.save(commit=False)
            #validación
            e.seccion = e.seccion.upper()
            e.save()
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
            e = form.save(commit=False)
            #validación
            e.seccion = e.seccion.upper()
            e.save()
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
@permission_required('home.change_estudiante', raise_exception=True)#Validar permiso
def editarNotas(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)#Obtener el estudiante
    notas = Nota.objects.filter(Q(estudiante_id=pk),Q(periodo=estudiante.periodo))

    formset = NotasFormSet(request.POST or None, queryset=notas)

    content = 'home/form-content/notas_form.html'
    objects = zip(notas, formset)

    context = {
        'estudiante':estudiante,
        'formset':formset,
        'objects':objects,
        'segment':'estudiante',
        'title':'Editar Notas',
        'content':content
    }

    if request.POST:
        if formset.is_valid():
            formset.save()
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
            return redirect('estudiante_ver', pk)#Redireccionar normalmente
        else:
            print(formset.errors)

    return render(request, 'layouts/form.html', context)

@login_required(login_url="/login/")
@permission_required('home.change_estudiante', raise_exception=True)#Validar permiso
def estudianteInasistencias(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)#Obtener el estudiante
    notas = Nota.objects.filter(Q(estudiante_id=pk),Q(periodo=estudiante.periodo))

    formset = InasistenciaFormSet(request.POST or None, queryset=notas)

    content = 'home/form-content/inacistencia_form.html'
    objects = zip(notas, formset)

    context = {
        'estudiante':estudiante,
        'formset':formset,
        'objects':objects,
        'segment':'estudiante',
        'title':'Cargar Inasistencias',
        'content':content
    }

    if request.POST:
        if formset.is_valid():
            formset.save()
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
            return redirect('estudiante_ver', pk)#Redireccionar normalmente
        else:
            print(formset.errors)

    return render(request, 'layouts/form.html', context)

@login_required(login_url="/login/")
def carga_notas(request, pd):
    
    periodo = get_object_or_404(Periodo, pk=pd)
    carga = periodo.carga
    estudiantes = Estudiante.objects.filter(periodo_id=pd).order_by("ci").exclude(periodo_completo=True)[:10]
    if not estudiantes:
        return render(request, 'home/carga_de_notas.html', {'fail_message':'No hay estudiantes pendientes por cargas en este periodo'})
    
    materias = carga.materias.all().order_by("nombre")
    
    cantidad_materias = materias.count()
    total_forms = cantidad_materias * estudiantes.count()
    NotasFormSet = formset_factory(form=NotaForm, extra=total_forms)
    formset = NotasFormSet(request.POST or None, )
    
    if request.POST:
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data['estudiante'])
                print(form.cleaned_data['periodo'])
                estudiante = form.cleaned_data['estudiante']
                periodo = form.cleaned_data['periodo']
                Nota.objects.create(
                    
                    estudiante = estudiante,
                    periodo = periodo,
                    materia = form.cleaned_data['materia'],
                    lapso_1 = form.cleaned_data['lapso_1'],
                    lapso_2 = form.cleaned_data['lapso_2'],
                    lapso_3 = form.cleaned_data['lapso_3'],
                    reparacion = form.cleaned_data['reparacion'],
                    
                )

            for estudiante in estudiantes:
                estudiante.periodo_completo = True
                estudiante.save()
                return redirect('periodo')
        else:
            print(formset.errors)

    context = {
        'periodo': periodo,
        'carga': carga,
        'materias': materias,
        'cantidad_materias': cantidad_materias,
        'total_forms': total_forms,
        'estudiantes': estudiantes,
        'formset': formset,
        'segment': 'periodo'
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

@login_required(login_url="/login/")
@permission_required('home.change_periodo', raise_exception=True)#Validar permiso
@transaction.atomic
def cambiar_periodo(request, periodo_actual):
    if request.method == 'POST':
        # Obtén el periodo al que se moverán los estudiantes
        nuevo_periodo = get_object_or_404(Periodo, pk=request.POST['periodo_nuevo'])

        # Obtén el periodo actual de los estudiantes
        periodo = get_object_or_404(Periodo, pk=periodo_actual)

        # Verifica que el nuevo periodo esté vacío
        if not Estudiante.objects.filter(periodo=nuevo_periodo).exists():
            # Obtén todos los estudiantes del periodo actual
            estudiantes = Estudiante.objects.filter(periodo=periodo)

            # Cambia el periodo de cada estudiante y establece periodo_completo en False
            for estudiante in estudiantes:
                estudiante.periodo = nuevo_periodo
                estudiante.periodo_completo = False
                estudiante.save()

            return HttpResponse('<script>alert("Cambio de periodo realizado con éxito."); window.location.href="/periodos";</script>')

        else:
            return HttpResponse('<script>alert("Hubo un error, por favor contacte con soporte."); window.location.href="/periodos";</script>')

    else:
        # Si el método es GET, renderiza la plantilla con los periodos disponibles
        periodos = Periodo.objects.exclude(id=periodo_actual).filter(estudiante__isnull=True)
        content = 'home/form-content/cambiar_periodo.html'
        context = {
            'periodos': periodos,
            'segment':'periodo',
            'title':'Cambiar Periodo académico',
            'content':content,
            'periodo_actual':periodo_actual
            }
        return render(request, 'layouts/form.html', context)

