#import datetime, decimal
from urllib import request
from django import template
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms import formset_factory
from django.template import loader
from django.db.models import Q, Count, F
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from .forms import PlantelForm, PeriodosForm, AniosForm, MencionesForm, ProfesorForm
from .models import DatosPlantel, PeriodosAcademicos, Menciones, Secciones, AniosMencionSec
from .models import *
from .forms import *
from .forms import PlantelForm, PeriodosForm, AniosForm, MencionesForm, EstudiantesForm, CargarNotas, Boletas, MateriasForm, MateriaProfesorForm
import json
from .models import Anios, DatosPlantel, Materias, PeriodosAcademicos, Menciones, Secciones, AniosMencionSec, MateriasAniosMenciones, Estudiantes, Notas, Profesores, MateriasProfesores

from .utils import getInputsMenciones

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

#----------------------------------------------------------------------------------#



### Seccion de Materias ###

@login_required(login_url="/login/")
@permission_required('home.delete_materia', raise_exception=True)#Validar permiso
def materiaEliminar(request, pk):
    materia = get_object_or_404(Materia, pk=pk)#Obtener el materia a eliminar
    materia.delete()#Eliminar

    if 'next' in request.GET:
        return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
    return redirect('materia')#Redireccionar normalmente


### Seccion de planillas ###

@login_required(login_url="/login/")
def planillas(request):

    table = 'home/table-content/planillas.html'
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planillas',
        'buscar':True,
        'table':table,
        
    }
    
    return render(request, 'home/table.html', context)


@login_required(login_url="/login/")
def registroTitulos(request):

    table = 'home/planillas/registro-titulos.html'
    rows = range(25)
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Registro Titulos',
        'buscar':True,
        'table':table,
        'rows':rows,
        'url_back': '/planillas'
    }

    return render(request, 'home/planillas/registro-titulos.html', context)

@login_required(login_url="/login/")
def finales(request):

    table = 'home/form-content/planillas_form.html'
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planilla Finales',
        'buscar':True,
        'table':table,
        'url_back': '/planillas'
    }
    
    return render(request, 'home/planillas/finales.html', context)

def revision(request):

    table = 'home/form-content/planillas_form.html'
    rows = range(33)
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planilla Revisión',
        'buscar':True,
        'table':table,
        'rows':rows,
        'url_back': '/planillas'
    }
    
    return render(request, 'home/planillas/revision.html', context)

def materiaPendientes(request):

    table = 'home/form-content/planillas_form.html'
    rows = range(13)
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planilla Materia Pendientes',
        'buscar':True,
        'table':table,
        'rows':rows,
        'url_back': '/planillas'
    }

    return render(request, 'home/planillas/materia-pendiente.html', context)


### Seccion de Carga de Notas ###

# @login_required(login_url="/login/")
# def cargas(request):
#     cargas = Carga.objects.all()

#     buscar = request.GET.get('buscar')#Tomar texto del buscador
#     if buscar:#Si exste, filtrar
#         cargas = cargas.filter(Q(titulo__icontains=buscar))

#     table = 'home/table-content/cargas.html'
#     context={
#         'cargas':cargas,
#         'segment':'carga',
#         'title':'Cargas académicas',
#         'buscar':True,
#         'table':table,
#         'url_crear':'/cargas/crear'
#     }

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':#Evaluar si es una petición AJAX
#         table_html = render_to_string(table, context, request)#Rendereziar los datos en una plantilla de tabla reducida
#         return JsonResponse({'table_html': table_html, })#JsonResponse para manejar con JavaScript y recargar un segmento de la página

#     return render(request, 'home/table.html', context)

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

### Seccion de profesores ###
@login_required(login_url="/login/")
def profesores(request):
    profesores = Profesores.objects.values('id', 'ci_tipo', 'ci', 'nombre', 'apellido')
    profesores = Profesores.objects.all().order_by('-ci')
    content = 'home/profesores/profesores.html'
    context = {
        'segment':'profesores',
        'title':'Profesores',
        'table':content,
        'profesores':profesores
    }

    return render(request, 'home/table.html', context)


### Crear Profesores ###
@login_required(login_url="/login/")
def crearProfesores(request):
    if request.method == 'POST':
        ci = request.POST.get('ci')
        ci_tipo = request.POST.get('ci_tipo')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        Profesores.objects.create(ci=ci, ci_tipo=ci_tipo, nombre=nombre, apellido=apellido)
        messages.success(request, 'Profesor creado correctamente')
        return redirect('profesores')
        
    form = ProfesorForm()

    content = 'home/profesores/crear_profesores.html'
    context = {
        'form':form,
        'segment':'profesores',
        'title':'Crear Profesor',
        'table':content,
        'url_back': '/profesores'
    }

    return render(request, 'home/table.html', context)

### Editar Profesores ###
@login_required(login_url="/login/")
def editarProfesores(request, id):
    if request.POST:
        profesor = ProfesorForm(request.POST)
        if profesor.is_valid():
            profesor = profesor.cleaned_data
            profesor['materias']  = Materias.objects.get(id = profesor['materias'])
            Profesores.objects.filter(id=id).update(**profesor)
            messages.success(request, 'Los datos del profesor se han actualizado correctamente')
            return redirect('profesores')
        else:
            print(profesor.errors)

    else:
        profesor = Profesores.objects.values().get(id=id)
        form = ProfesorForm(initial=profesor)
        
    content = 'home/profesores/editar_profesores.html'
    context = {
    'form':form,
    'segment':'profesores',
    'title':'Editar profesores',
    'table':content,
    'url_back': '/profesores'
    }
    
    return render(request, 'home/table.html', context)

@login_required(login_url="/login/")
def agergar_materia_profesor(request, pk):

    mensaje_error = None

    if request.POST:
        seccion = request.POST.get('seccion')
        seccion = Secciones.objects.get(id=seccion)
        materia = request.POST.get('materia')
        materia = MateriasAniosMenciones.objects.get(id=materia)
        profesor = Profesores.objects.get(id=pk)

        materia_profesor = MateriasProfesores.objects.filter(seccion=seccion, materia=materia).all().first()

        if materia_profesor:

            mensaje_error = f"No puede realizar esta accion porque el profesor o profesora {materia_profesor.profesor.nombre} ya imparte esta materia."

        else: 

            MateriasProfesores.objects.create(seccion=seccion, materia=materia, profesor=profesor)

    form = MateriaProfesorForm()

    materias = MateriasProfesores.objects.values('id', 'seccion__nombre', 'materia__materia__nombre', 'materia__anio__nombre', 'materia__mencion__nombre').filter(profesor=pk)

    content = 'home/profesores/agregar_materia.html'
    context = {
        'segment':'profesores',
        'title':'Materias',
        'table':content,
        'form':form,
        'materias': materias,
        'mensaje_error': mensaje_error
    }

    return render(request, 'home/table.html', context)

@login_required(login_url="/login/")
def eliminar_materia_profesor(request, pk):

    materia = MateriasProfesores.objects.get(id=pk)
    materia.delete()

    return JsonResponse({"message": "Los datos se actualizaron correctamente."}, status=200)

### Seccion de Estudiantes ###

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
            print('F')#Respuesta de respaldo
    context = {
        'estudiante':estudiante,
        'notas':notas,
        'otros_periodos':otros_periodos,
        'segment':'estudiante',
        'otro_p':otro_p,
        'otro_p_id':otro_p_id
        }
    return render(request, plantilla, context)#Redireccionar normalmente

# @login_required
# @permission_required('home.add_estudiante', raise_exception=True)#type:ignore
# def estudianteCrear(request):
#     form = estudianteForm(request.POST or None)
#     content = 'home/form-content/estudiante_form.html'
#     context = {
#         'form':form,
#         'segment':'estudiante',
#         'title':'Registrar Estudiante',
#         'content':content
#     }
#     if request.POST:
#         if form.is_valid():
#             e = form.save(commit=False)
#             #validación
#             e.seccion = e.seccion.upper()
#             e.save()
#             return redirect('estudiante')
#         else:
#             print(form.errors)
    
#     return render(request, 'layouts/form.html', context)

# @login_required
# @permission_required('home.change_estudiante', raise_exception=True)#type:ignore
# def estudianteEditar(request, pk):
#     obj = get_object_or_404(Estudiante, pk=pk)
#     form = estudianteForm(request.POST or None, instance=obj)
#     content = 'home/form-content/estudiante_form.html'
#     context = {
#         'form':form,
#         'segment':'estudiante',
#         'title':'Editar Estudiante',
#         'content':content
#     }
#     if request.POST:
#         if form.is_valid():
#             e = form.save(commit=False)
#             #validación
#             e.seccion = e.seccion.upper()
#             e.save()
#             return redirect('estudiante')
#         else:
#             print(form.errors)
    
#     return render(request, 'layouts/form.html', context)

# @login_required(login_url="/login/")
# @permission_required('home.delete_estudiante', raise_exception=True)#Validar permiso
# def estudianteEliminar(request, pk):
#     estudiante = get_object_or_404(Estudiante, pk=pk)#Obtener el estudiante a eliminar
#     estudiante.delete()#Eliminar

#     if 'next' in request.GET:
#         return redirect(request.GET.get('next'))#Evaluar si existe una página a la que redireccionar y redireccionar
#     return redirect('estudiante')#Redireccionar normalmente

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
    
    # Obtenemos el objeto Periodo correspondiente al id proporcionado o lanzamos un error 404 si no existe
    periodo = get_object_or_404(Periodo, pk=pd)
    # Obtenemos la carga asociada al periodo
    carga = periodo.carga
    # Obtenemos los primeros 10 estudiantes asociados al periodo que aún no han completado el periodo
    estudiantes = Estudiante.objects.filter(periodo_id=pd).order_by("ci").exclude(periodo_completo=True)[:10]
    # Si no hay estudiantes pendientes, renderizamos la plantilla con un mensaje de error
    if not estudiantes:
        return render(request, 'home/carga_de_notas.html', {'fail_message':'No hay estudiantes pendientes por cargas en este periodo'})
    
    # Obtenemos todas las materias asociadas a la carga, ordenadas por nombre
    materias = carga.materias.all().order_by("nombre")
    
    # Contamos el número de materias
    cantidad_materias = materias.count()
    # Calculamos el número total de formularios que necesitamos, que es el número de estudiantes por el número de materias
    total_forms = cantidad_materias * estudiantes.count()
    # Creamos un conjunto de formularios para el modelo Nota, con el número total de formularios que hemos calculado
    NotasFormSet = formset_factory(form=NotaForm, extra=total_forms)
    # Inicializamos el conjunto de formularios con los datos POST si los hay, o vacío si no los hay
    formset = NotasFormSet(request.POST or None, )
    
    # Si se ha enviado el formulario
    if request.POST:
        # Si el conjunto de formularios es válido
        if formset.is_valid():
            # Recorremos cada formulario en el conjunto
            for form in formset:
                # Imprimimos los datos del estudiante y del periodo
                print(form.cleaned_data['estudiante'])
                print(form.cleaned_data['periodo'])
                # Obtenemos el estudiante y el periodo del formulario
                estudiante = form.cleaned_data['estudiante']
                periodo = form.cleaned_data['periodo']
                # Creamos un nuevo objeto Nota con los datos del formulario
                Nota.objects.create(
                    estudiante = estudiante,
                    periodo = periodo,
                    materia = form.cleaned_data['materia'],
                    lapso_1 = form.cleaned_data['lapso_1'],
                    lapso_2 = form.cleaned_data['lapso_2'],
                    lapso_3 = form.cleaned_data['lapso_3'],
                    reparacion = form.cleaned_data['reparacion'],
                )

            # Marcamos el periodo como completo para cada estudiante y guardamos el estudiante
            for estudiante in estudiantes:
                estudiante.periodo_completo = True
                estudiante.save()
                # Redirigimos al usuario a la vista del periodo
                return redirect('periodo')
        else:
            # Si el conjunto de formularios no es válido, imprimimos los errores
            print(formset.errors)

    # Preparamos el contexto para la plantilla
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

    # Renderizamos la plantilla con el contexto
    return render(request, 'home/carga_de_notas.html', context)


### Seccion de Periodos ###

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
    # Obtenemos el objeto Periodo correspondiente al id proporcionado o lanzamos un error 404 si no existe
    obj = get_object_or_404(Periodo, pk=pk)
    # Creamos un formulario para el objeto Periodo, inicializado con los datos POST si los hay, o con los datos del objeto si no los hay
    form = periodoForm(request.POST or None, instance=obj)
    # Definimos el contenido de la plantilla
    content = 'home/form-content/periodo_form.html'
    # Preparamos el contexto para la plantilla
    context = {
        'form': form,
        'segment': 'periodo',
        'title': 'Editar Periodo académico',
        'content': content
    }
    # Si se ha enviado el formulario
    if request.POST:
        # Si el formulario es válido
        if form.is_valid():
            # Guardamos el formulario pero no confirmamos los cambios en la base de datos todavía (commit=False)
            form.save(commit=False)
            # Aquí es donde iría cualquier validación adicional
            # Confirmamos los cambios en la base de datos
            form.save()
            # Redirigimos al usuario a la vista del periodo
            return redirect('periodo')
        else:
            # Si el formulario no es válido, imprimimos los errores
            print(form.errors)
    
    # Renderizamos la plantilla con el contexto
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
@permission_required('home.change_periodo', raise_exception=True)  # Validar permiso
@transaction.atomic  # Aseguramos que todas las operaciones en la base de datos se realicen de forma atómica // que todas las operaciones se ejecutan con éxito, si falla una, se revierten los cambios
def cambiar_periodo(request, periodo_actual):
    if request.method == 'POST':  # Si el método de la petición es POST
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

            # Si todo ha ido bien, redirige al usuario a la página de periodos con un mensaje de éxito
            return HttpResponse('<script>alert("Cambio de periodo realizado con éxito."); window.location.href="/periodos";</script>')

        else:
            # Si ha habido algún problema, redirige al usuario a la página de periodos con un mensaje de error
            return HttpResponse('<script>alert("Hubo un error, por favor contacte con soporte."); window.location.href="/periodos";</script>')

    else:  # Si el método de la petición es GET
        # Obtenemos todos los periodos disponibles que no sean el actual y que no tengan estudiantes asignados
        periodos = Periodo.objects.exclude(id=periodo_actual).filter(estudiante__isnull=True)
        # Definimos el contenido de la plantilla
        content = 'home/form-content/cambiar_periodo.html'
        # Preparamos el contexto para la plantilla
        context = {
            'periodos': periodos,
            'segment':'periodo',
            'title':'Cambiar Periodo académico',
            'content':content,
            'periodo_actual':periodo_actual
            }
        # Renderizamos la plantilla con el contexto
        return render(request, 'layouts/form.html', context)
    
@login_required(login_url="/login/")
def configuracion(request):
    
    if request.method == 'POST':
        form = PlantelForm(request.POST)
        if form.is_valid():
            datos_plantel = DatosPlantel.objects.first()

            save_data = form.cleaned_data

            periodo = PeriodosAcademicos.objects.get(id=save_data['periodo_id'])

            save_data['periodo'] = periodo

            if datos_plantel:
                DatosPlantel.objects.update(**save_data)
                datos_plantel = form.cleaned_data
            else:
                DatosPlantel.objects.create(**save_data)
                datos_plantel = form.cleaned_data
    else:

        datos_plantel = DatosPlantel.objects.values().first()

        if not datos_plantel:
            datos_plantel= {
                'codigo': '', 
                'nombre': '', 
                'direccion': '', 
                'telefono': None, 
                'municipio': '', 
                'entidad_federal': '', 
                'zona_educativa': '', 
                'distrito_escolar': '', 
                'director': '', 
                'ci_tipo': '', 
                'ci': None,
                'periodo_id': ''
            }

    form = PlantelForm(initial=datos_plantel)

    content = 'home/configuracion/index.html'
    context = {
        'form':form,
        'segment':'configuracion',
        'title':'Configuración',
        'table':content
    }

    return render(request, 'home/table.html', context)


@login_required(login_url="/login/")
def crearPeriodoAcademico(request):
    
    if request.method == 'POST':
        form = PeriodosForm(request.POST)
        if form.is_valid():

            PeriodosAcademicos.objects.create(**form.cleaned_data)
            messages.success(request, 'Periodo académico creado correctamente')

    form = PeriodosForm()

    data_table = list(PeriodosAcademicos.objects.values('id', 'nombre'))

    content = 'home/configuracion/periodos-academicos.html'
    context = {
        'form':form,
        'segment':'configuracion',
        'title':'Años Escolares',
        'table':content,
        'data_table':data_table,
        'url_back': '/configuracion'
    }

    return render(request, 'home/table.html', context)

@require_POST
def periodoAcademico_editar(request, pk):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    periodoA = PeriodosAcademicos.objects.filter(id=pk).first()

    if periodoA:

        nombre = data.get('nombre')

        if nombre:
            setattr(periodoA, 'nombre', nombre)


        # Guarda los cambios en la base de datos
        periodoA.save()

        return JsonResponse({"message": "Los datos se actualizaron correctamente."}, status=200)
    else:
        return JsonResponse({"error": "Periodo no encontrado."}, status=404)

@login_required(login_url="/login/")
def secciones(request):

    data_table = Secciones.objects.values('id', 'nombre')

    print("")
    print(data_table)
    print("")

    content = 'home/configuracion/secciones.html'
    context = {
        'segment':'configuracion',
        'title':'Secciones',
        'table':content,
        'data_table':data_table,
        'url_back': '/configuracion'
    }

    return render(request, 'home/table.html', context)

### Crear Secciones ###
@login_required(login_url="/login/")
def crear_seccion(request):

    if request.method == 'POST':

        seccion = request.POST.get('seccion')

        inst_seccion = Secciones.objects.create(nombre=seccion)
        messages.success(request, 'La sección se ha creado correctamente')

        datos = request.POST.copy()
        datos.pop('seccion')
        datos.pop('csrfmiddlewaretoken')
        
        for id_anio in datos:

            list_menciones = datos.getlist(str(id_anio))

            inst_anio = Anios.objects.get(id=id_anio)

            for id_mencion in list_menciones:

                inst_mencion = Menciones.objects.get(id=id_mencion)

                AniosMencionSec.objects.create(anio=inst_anio, mencion=inst_mencion, seccion=inst_seccion)
            return redirect('secciones')
    anios = list(Anios.objects.values('id', 'nombre'))
    menciones = list(Menciones.objects.values('id', 'nombre', 'nombre_abrev'))

    form = ''

    form += f"""
    <div class="col-1">
        <div class="form-group">
            <label for="seccion">Sección</label>
            <input type="text" name="seccion" class="form-control" id="seccion" required>
        </div>
    </div>
    <div class="w-100"></div>
    <p>Seleccione las menciones a las cuales pertenece la sección a crear</p>
    """

    for index, anio in enumerate(anios):
        form += f"""
        <div class="col">
            <div class="card">
                <div class="card-body">
                    <h6>{anio['nombre']}</h6>
                    <div class="px-4">
                        <p>Menciones</p>
                        {getInputsMenciones(anio['id'], menciones)}
                    </div>
                </div>
            </div>
        </div>
        """
        if index == 2:
            form += """
            <div class="w-100 pb-4"></div>
            """

    content = 'home/configuracion/crear-seccion.html'
    context = {
        'form':form,
        'segment':'configuracion',
        'title':'Crear seccion',
        'table':content,
        'url_back': '/configuracion/secciones'
    }

    return render(request, 'home/table.html', context)

### Editar Secciones ###
@login_required(login_url="/login/")
def editar_seccion(request, pk):

    try:
        inst_seccion = Secciones.objects.get(id=pk)

        if request.method == 'POST':

            seccion = request.POST.get('seccion')

            setattr(inst_seccion, 'nombre', seccion)

            inst_seccion.save()
            messages.success(request, 'La sección se ha actualizado correctamente')
            datos = request.POST.copy()
            datos.pop('seccion')
            datos.pop('csrfmiddlewaretoken')

            datos = dict(datos)

            for anio, menciones in datos.items():

                for mencion in menciones:

                    inst_anios_men_sec = AniosMencionSec.objects.filter(seccion=pk, anio=anio, mencion=mencion)

                    if not inst_anios_men_sec:

                        inst_anio = Anios.objects.get(id=anio)
                        inst_mencion = Menciones.objects.get(id=mencion)
                        inst_anios_men_sec = Secciones.objects.get(id=pk)

                        AniosMencionSec.objects.create(anio=inst_anio, mencion=inst_mencion, seccion=inst_anios_men_sec)

            inst_secciones = AniosMencionSec.objects.values("id", "anio", "mencion").filter(seccion=pk)

            for i in inst_secciones:

                if str(i['anio']) in datos:
                    
                    if not str(i['mencion']) in datos[str(i['anio'])]:

                        AniosMencionSec.objects.get(id=i['id']).delete()
                    return redirect('secciones')
        anios = list(Anios.objects.values('id', 'nombre'))
        menciones = list(Menciones.objects.values('id', 'nombre', 'nombre_abrev'))

        data = AniosMencionSec.objects.filter(seccion=pk)

        form = ''

        form += f"""
        <div class="col-1">
            <div class="form-group">
                <label for="seccion">Sección</label>
                <input type="text" name="seccion" class="form-control" id="seccion" value="{inst_seccion.nombre}" required>
            </div>
        </div>
        <div class="w-100"></div>
        <p>Seleccione las menciones a las cuales pertenece la sección a crear</p>
        """

        for index, anio in enumerate(anios):
            form += f"""
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <h6>{anio['nombre']}</h6>
                        <div class="px-4">
                            <p>Menciones</p>
                            {getInputsMenciones(anio['id'], menciones, data)}
                        </div>
                    </div>
                </div>
            </div>
            """
            if index == 2:
                form += """
                <div class="w-100 pb-4"></div>
                """

        content = 'home/configuracion/editar-seccion.html'
        context = {
            'form':form,
            'segment':'configuracion',
            'title':'Editar seccion',
            'table':content,
            'url_back': '/configuracion/secciones'
        }

        return render(request, 'home/table.html', context)
    except ObjectDoesNotExist:
        print("El objeto con el ID dado no existe en la base de datos.")
        return render(request, 'home/page-404.html')

### Crear Años ###
@login_required(login_url="/login/")
def crearAnios(request):
    
    if request.method == 'POST':
        form = AniosForm(request.POST)
        if form.is_valid():
            
            Anios.objects.create(**form.cleaned_data)
            messages.success(request, 'Año creado correctamente')

    form = AniosForm()

    data_table = list(Anios.objects.values('id', 'nombre'))

    content = 'home/configuracion/anios.html'
    context = {
        'form':form,
        'segment':'configuracion',
        'title':'Años',
        'table':content,
        'data_table':data_table,
        'url_back': '/configuracion'
    }

    return render(request, 'home/table.html', context)

@require_POST
def anio_editar(request, pk):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    anio = Anios.objects.filter(id=pk).first()

    if anio:

        nombre = data.get('nombre')

        if nombre:
            setattr(anio, 'nombre', nombre)


        # Guarda los cambios en la base de datos
        anio.save()

        return JsonResponse({"message": "Los datos se actualizaron correctamente."}, status=200)
    else:
        return JsonResponse({"error": "Año no encontrado."}, status=404)


### Crear Menciones ###
@login_required(login_url="/login/")
def crearMenciones(request):
    
    if request.method == 'POST':
        form = MencionesForm(request.POST)
        if form.is_valid():
            
            try:
                Menciones.objects.create(**form.cleaned_data)
                messages.success(request, 'La mención se ha creado correctamente')
            except IntegrityError as e:
                if 'unique constraint' in str(e.args):
                    return HttpResponse("Esta mención ya existe. Inténtalo de nuevo.", status=400)

    form = MencionesForm()

    data_table = Menciones.objects.values('id', 'nombre', 'nombre_abrev')

    content = 'home/configuracion/menciones.html'
    context = {
        'form':form,
        'segment':'configuracion',
        'title':'Menciones',
        'table':content,
        'data_table':data_table,
        'url_back': '/configuracion'
    }

    return render(request, 'home/table.html', context)

@login_required(login_url="/login/")
def materias(request):

    data_table = Materias.objects.values('id', 'nombre', 'nombre_abrev')

    content = 'home/materias/index.html'
    context={
        'segment':'materia',
        'title':'Materias',
        'table':content,
        'data_table': data_table
    }
      
    return render(request, 'home/table.html', context)

@login_required
def materiaCrear(request):

    if request.method == 'POST':

        materia = request.POST.get('materia')
        abrev = request.POST.get('abrev')
        literal = request.POST.get('literal')

        inst_materia = Materias.objects.create(nombre=materia, nombre_abrev=abrev, literal=literal)
        messages.success(request, 'La materia se ha creado correctamente')

        datos = request.POST.copy()
        datos.pop('materia')
        datos.pop('abrev')
        datos.pop('csrfmiddlewaretoken')
        datos.pop('literal')

        for id_anio in datos:

            list_menciones = datos.getlist(str(id_anio))

            inst_anio = Anios.objects.get(id=id_anio)

            for id_mencion in list_menciones:

                inst_mencion = Menciones.objects.get(id=id_mencion)

                MateriasAniosMenciones.objects.create(anio=inst_anio, mencion=inst_mencion, materia=inst_materia)

    anios = list(Anios.objects.values('id', 'nombre'))
    menciones = list(Menciones.objects.values('id', 'nombre', 'nombre_abrev'))

    form = ''

    form += f"""
    <div class="col-4">
        <div class="form-group">
            <label for="seccion">Ingrese el nombre de la materia</label>
            <input type="text" name="materia" class="form-control" id="materia" required>
            <label for="seccion">Ingrese la abreviatura de la materia</label>
            <input type="text" name="abrev" class="form-control w-15" id="abrev" required>
            <label for="seccion">¿La materia es literal?</label>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="literal" id="flexRadioDefault1" value="f" checked>
                <label class="form-check-label" for="flexRadioDefault1">
                    No
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="literal" id="flexRadioDefault2" value="t">
                <label class="form-check-label" for="flexRadioDefault2">
                    Si
                </label>
            </div>
        </div>
    </div>
    <div class="w-100"></div>
    <p>Seleccione las menciones a las cuales pertenece la materia a crear</p>
    """

    for index, anio in enumerate(anios):
        form += f"""
        <div class="col">
            <div class="card">
                <div class="card-body">
                    <h6>{anio['nombre']}</h6>
                    <div class="px-4">
                        <p>Menciones</p>
                        {getInputsMenciones(anio['id'], menciones)}
                    </div>
                </div>
            </div>
        </div>
        """
        if index == 2:
            form += """
            <div class="w-100 pb-4"></div>
            """

    content = 'home/materias/crear.html'
    context = {
        'form': form,
        'segment':'materia',
        'title':'Crear Materia',
        'table':content,
        'url_back': '/materias'
    }
    
    return render(request, 'home/table.html', context)


@login_required(login_url="/login/")
def materiaEditar(request, pk):

    try:

        materia = Materias.objects.get(id=pk)

        if request.method == 'POST':

            nombre_materia = request.POST.get('materia')
            abrev = request.POST.get('abrev')
            literal = request.POST.get('literal')

            setattr(materia, "nombre", nombre_materia)
            setattr(materia, "nombre_abrev", abrev)
            setattr(materia, "literal", literal)

            materia.save()
            messages.success(request, 'La materia se ha actualizado correctamente')

            datos = request.POST.copy()
            datos.pop('materia')
            datos.pop('abrev')
            datos.pop('csrfmiddlewaretoken')
            datos.pop('literal')

            datos = dict(datos)

            for anio, menciones in datos.items():

                for mencion in menciones:

                    inst_materia = MateriasAniosMenciones.objects.filter(materia=pk, anio=anio, mencion=mencion)

                    if not inst_materia:

                        inst_anio = Anios.objects.get(id=anio)
                        inst_mencion = Menciones.objects.get(id=mencion)
                        inst_materia = Materias.objects.get(id=pk)

                        MateriasAniosMenciones.objects.create(anio=inst_anio, mencion=inst_mencion, materia=inst_materia)

            inst_materias = MateriasAniosMenciones.objects.values("id", "anio", "mencion").filter(materia=pk)

            for i in inst_materias:

                if str(i['anio']) in datos:

                    if not str(i['mencion']) in datos[str(i['anio'])]:

                        MateriasAniosMenciones.objects.get(id=i['id']).delete()
                        
                else:

                    MateriasAniosMenciones.objects.get(id=i['id']).delete()

        anios = list(Anios.objects.values('id', 'nombre'))
        menciones = list(Menciones.objects.values('id', 'nombre', 'nombre_abrev'))

        data = MateriasAniosMenciones.objects.filter(materia=materia)

        form = ''

        form += f"""
        <div class="col-4">
            <div class="form-group">
                <label for="seccion">Ingrese el nombre de la materia</label>
                <input type="text" name="materia" class="form-control" id="materia" value="{materia.nombre}" required>
                <label for="seccion">Ingrese la abreviatura de la materia</label>
                <input type="text" name="abrev" class="form-control w-15" id="abrev" value="{materia.nombre_abrev}" required>
                <label for="seccion">¿La materia es literal?</label>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="literal" id="flexRadioDefault1" value="f" {'checked' if not materia.literal else ''}>
                    <label class="form-check-label" for="flexRadioDefault1">
                        No
                    </label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="literal" id="flexRadioDefault2" value="t" {'checked' if materia.literal else ''}>
                    <label class="form-check-label" for="flexRadioDefault2">
                        Si
                    </label>
                </div>
            </div>
        </div>
        <div class="w-100"></div>
        <p>Seleccione las menciones a las cuales pertenece la materia a crear</p>
        """

        for index, anio in enumerate(anios):
            form += f"""
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <h6>{anio['nombre']}</h6>
                        <div class="px-4">
                            <p>Menciones</p>
                            {getInputsMenciones(anio['id'], menciones, data)}
                        </div>
                    </div>
                </div>
            </div>
            """
            if index == 2:
                form += """
                <div class="w-100 pb-4"></div>
                """

        content = 'home/materias/crear.html'
        context = {
            'form': form,
            'segment':'materia',
            'title':'Crear Materia',
            'table':content,
            'url_back': '/materias'
        }

        return render(request, 'home/table.html', context)
    except ObjectDoesNotExist:
        print("El objeto con el ID dado no existe en la base de datos.")
        return render(request, 'home/page-404.html')
    
@login_required(login_url="/login/")
def obtener_materias(request):
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    anio = data.get('anio')
    mencion = data.get('mencion')

    materias = list(MateriasAniosMenciones.objects.values('id', 'materia__nombre').filter(anio=anio, mencion=mencion).all())

    return JsonResponse({"message": "Datos obtenidos correctamente.", 'materias': materias}, status=200) 


def obtener_estudiantes_notas(anio, mencion, seccion, periodo):

    estudiantes = Notas.objects.values(
        'estudiante__id',
        'ci_tipo',
        'ci',
        'estudiante__nombres',
        'estudiante__apellidos'
        ).filter(
            anio=anio, 
            mencion=mencion, 
            seccion=seccion,
            periodo=periodo
        ).order_by('-ci').distinct()
    
    resultado = []

    for estudiante in estudiantes:
        notas = list(Notas.objects.filter(estudiante_id=estudiante['estudiante__id'], tipo='n').values(
            'lapso1', 'lapso2', 'lapso3', 'definitiva', 'revision', 'materia', 'materia__materia__literal'
        ))

        for nota in notas:
            nota['materia__materia__literal'] = str(nota['materia__materia__literal']).lower()

        estudiante['notas'] = notas

        resultado.append(estudiante)

    return resultado

@login_required(login_url="/login/")
def Cargar_Notas(request):

    anio = request.GET.get('anio')
    mencion = request.GET.get('mencion')
    seccion = request.GET.get('seccion')
    periodo = request.GET.get('periodo')

    estudiantes = obtener_estudiantes_notas(anio, mencion, seccion, periodo)

    materias = MateriasAniosMenciones.objects.values('id', 'materia__nombre', 'materia__literal').filter(anio=anio, mencion=mencion).order_by('id').all()

    col_span = (len(materias) - 3)

    anio = Anios.objects.values('nombre').filter(id=anio).first()
    seccion = Secciones.objects.values('nombre').filter(id=seccion).first()
    escolaridad = DatosPlantel.objects.values('periodo__nombre').first()

    table = 'home/form-content/planillas_form.html'
    context={
        'Cargar_Notas':Cargar_Notas,
        'segment':'notas',
        'title':'',
        'buscar':True,
        'table':table,
        'estudiantes': estudiantes,
        'materias': materias,
        'col_span': col_span,
        'anio': anio,
        'seccion': seccion,
        'escolaridad': escolaridad
    }

    return render(request, 'home/Cargar_Notas/notas.html', context)

@login_required(login_url="/login/")
def notas(request):

    if request.method == 'POST':

        anio = request.POST.get('anio')
        mencion = request.POST.get('mencion')
        seccion = request.POST.get('seccion')
        periodo = request.POST.get('periodo')

        return redirect(f'notas/cargar?anio={anio}&mencion={mencion}&seccion={seccion}&periodo={periodo}')

    form = CargarNotas()

    content = 'home/Cargar_Notas/index.html'
    context = {
        'segment':'notas',
        'title':'Notas',
        'table':content,
        'form':form
    }

    return render(request, 'home/table.html', context)


### Estudiantes ###
@login_required(login_url="/login/")
def estudiantes(request):
    busqueda = request.POST.get('buscar')
    data_table = Estudiantes.objects.values('id', 'ci_tipo', 'ci', 'nombres', 'apellidos', 'sexo', 'anio', 'mencion', 'seccion',  'lugar_de_nacimiento', 'estado')
    data_table = Estudiantes.objects.all().order_by('-ci')
    if busqueda:
        data_table = Estudiantes.objects.filter(
            Q(ci_tipo__icontains = busqueda) |
            Q(ci__icontains = busqueda) |
            Q(nombres__icontains = busqueda) |
            Q(apellidos__icontains = busqueda) |
            Q(anio__nombre__icontains = busqueda) |
            Q(mencion__nombre__icontains = busqueda) |
            Q(seccion__nombre__icontains = busqueda)
        ).distinct()

    content = 'home/estudiantes/estudiantes.html'
    context = {
        'segment':'estudiantes',
        'title':'Estudiantes',
        'table':content,
        'data_table':data_table
    }

    return render(request, 'home/table.html', context)

### Crear Estudiantes ###
@login_required(login_url="/login/")
def estudianteCrear(request):

    if request.method == 'POST':
        
        ci = request.POST.get('ci')
        ci_tipo = request.POST.get('ci_tipo')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        sexo = request.POST.get('sexo')
        fecha_de_nacimiento = request.POST.get('fecha_de_nacimiento')
        anio = request.POST.get('anio_id')
        anio = Anios.objects.get(id = anio)
        mencion = request.POST.get('mencion_id')
        mencion = Menciones.objects.get (id = mencion)
        seccion = request.POST.get('seccion_id')
        seccion = Secciones.objects.get(id = seccion )
        entidad_federal = request.POST.get('entidad_federal')
        lugar_de_nacimiento = request.POST.get('lugar_de_nacimiento')
        estado = request.POST.get('estado')

        estudiante = Estudiantes.objects.create(ci=ci, ci_tipo=ci_tipo, nombres=nombres, apellidos=apellidos, sexo=sexo, fecha_de_nacimiento=fecha_de_nacimiento, anio=anio, mencion=mencion, seccion=seccion, entidad_federal=entidad_federal, lugar_de_nacimiento=lugar_de_nacimiento, estado=estado)
        messages.success(request, 'El estudiante se ha creado correctamente')
        
        if estado == "1" or estado == "2":
            materias = MateriasAniosMenciones.objects.filter(anio=anio, mencion=mencion).all()

            datos = DatosPlantel.objects.all().first()
            periodo = PeriodosAcademicos.objects.get(id=datos.periodo.id)

            for materia in materias:
                Notas.objects.create(materia=materia, estudiante=estudiante, periodo=periodo, anio=anio, mencion=mencion, seccion=seccion, ci_tipo=ci_tipo, ci=ci)

        return redirect('estudiantes')

    form = EstudiantesForm()

    content = 'home/estudiantes/estudiantes_crear.html'
    context = {
        'form':form,
        'segment':'estudiantes',
        'title':'Crear estudiantes',
        'table':content,
        'url_back': '/estudiantes'
    }

    return render(request, 'home/table.html', context)

### Editar Estudiantes ###
@login_required(login_url="/login/")
def estudianteEditar(request, id):

    if request.POST:
        estudiante = EstudiantesForm(request.POST)
        if estudiante.is_valid():
            estudiante = estudiante.cleaned_data
            estudiante['anio']  = Anios.objects.get(id = estudiante['anio_id'])
            estudiante['mencion']  = Menciones.objects.get(id = estudiante['mencion_id'])
            estudiante['seccion']  = Secciones.objects.get(id = estudiante['seccion_id'])
            Estudiantes.objects.filter(id=id).update(**estudiante)
            messages.success(request, 'Los datos del estudiante se han actualizado correctamente')
            return redirect('estudiantes')
        else:
            print(estudiante.errors)

    else:
        estudiante = Estudiantes.objects.values().get(id=id)
        form = EstudiantesForm(initial=estudiante)
        estudiante['fecha_de_nacimiento'] = estudiante['fecha_de_nacimiento'].strftime("%Y-%m-%d")

    content = 'home/estudiantes/estudiantes_editar.html'
    context = {
    'form':form,
    'segment':'estudiantes',
    'title':'Editar estudiantes',
    'table':content,
    'url_back': '/estudiantes'
    }

    return render(request, 'home/table.html', context)

@require_POST
def mencion_editar(request, pk):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    mencion = Menciones.objects.filter(id=pk).first()

    if mencion:

        nombre = data.get('nombre')
        abrev = data.get('abrev')

        if nombre:
            setattr(mencion, 'nombre', nombre)

        if abrev:
            setattr(mencion, 'nombre_abrev', abrev)

        # Guarda los cambios en la base de datos
        mencion.save()

        return JsonResponse({"message": "Los datos se actualizaron correctamente."}, status=200)
    else:
        return JsonResponse({"error": "Mención no encontrada."}, status=404)

@login_required(login_url="/login/")
def actualizar_notas(request, pk):

    anio = request.GET.get('anio')
    mencion = request.GET.get('mencion')
    seccion = request.GET.get('seccion')
    periodo = request.GET.get('periodo')

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    tiempo = data.get('tiempo')
    materia = data.get('materia')
    # materia = MateriasAniosMenciones.objects.get(id=materia)
    nota = data.get('nota')
    if nota == '': nota = 0

    inst_nota = Notas.objects.get(estudiante = pk, materia = materia)

    notas_lapsos = Notas.objects.values('lapso1', 'lapso2', 'lapso3').filter(estudiante = pk, materia = materia).first()
    
    dividir_por = 0
    if tiempo == 'lapso1':
        if int(nota) != 0:
            dividir_por += 1
            if notas_lapsos['lapso2'] != 0:
                dividir_por += 1
            if notas_lapsos['lapso3'] != 0:
                dividir_por += 1
        if dividir_por != 0:                    
            setattr(inst_nota, 'lapso1', nota)
            definitiva = (int(nota) + notas_lapsos['lapso2'] + notas_lapsos['lapso3'])/dividir_por
    elif tiempo == 'lapso2':
        if int(nota) != 0:
            dividir_por += 1
            if notas_lapsos['lapso1'] != 0:
                dividir_por += 1
            if notas_lapsos['lapso3'] != 0:
                dividir_por += 1
        if dividir_por != 0:
            setattr(inst_nota, 'lapso2', nota)
            definitiva = (notas_lapsos['lapso1'] + int(nota) + notas_lapsos['lapso3'])/dividir_por
    elif tiempo == 'lapso3':
        if int(nota) != 0:
            dividir_por += 1
            if notas_lapsos['lapso1'] != 0:
                dividir_por += 1
            if notas_lapsos['lapso2'] != 0:
                dividir_por += 1
        if dividir_por != 0:
            setattr(inst_nota, 'lapso3', nota)
            definitiva = (notas_lapsos['lapso1'] + notas_lapsos['lapso2'] + int(nota))/dividir_por
    elif tiempo == 'revision':
        setattr(inst_nota, 'revision', nota)

    if tiempo == 'lapso1' or tiempo == 'lapso2' or tiempo == 'lapso3':
        if dividir_por != 0:
            definitiva = int(round(definitiva, 0))
            setattr(inst_nota, 'definitiva', definitiva)

    inst_nota.save()

    estudiantes = obtener_estudiantes_notas(anio, mencion, seccion, periodo)

    return JsonResponse({"message": "Los datos se actualizaron correctamente.", "estudiantes": estudiantes}, status=200)


@login_required(login_url="/login/")
def boletas(request):

    if request.method == 'POST':

        pass

        anio = request.POST.get('anio')
        mencion = request.POST.get('mencion')
        seccion = request.POST.get('seccion')
        periodo = request.POST.get('periodo')

        return redirect(f'boletas/lista?anio={anio}&mencion={mencion}&seccion={seccion}&periodo={periodo}')

    form = Boletas()

    content = 'home/boletas/index.html'
    context = {
        'segment':'boletas',
        'title':'Generar Boletas',
        'table':content,
        'form':form
    }

    return render(request, 'home/table.html', context)

@login_required(login_url="/login/")
def boletas_lista_estudiantes(request):

    anio = request.GET.get('anio')
    mencion = request.GET.get('mencion')
    seccion = request.GET.get('seccion')
    periodo = request.GET.get('periodo')

    estudiantes = Notas.objects.values('estudiante__id', 'estudiante__ci_tipo', 'estudiante__ci', 'estudiante__nombres', 'estudiante__apellidos').filter(anio=anio, mencion=mencion, seccion=seccion, periodo=periodo).distinct()

    anio = Anios.objects.values('nombre').filter(id=anio).first()
    mencion = Menciones.objects.values('nombre').filter(id=mencion).first()
    seccion = Secciones.objects.values('nombre').filter(id=seccion).first()
    escolaridad = DatosPlantel.objects.values('nombre').filter(id = periodo).first()

    table = 'home/form-content/planillas_form.html'
    context={
        'segment':'boletas',
        'title':'Cargar boletas',
        'buscar':True,
        'table':table,
        'estudiantes': estudiantes,
        'anio': anio['nombre'],
        'mencion': mencion['nombre'],
        'seccion': seccion['nombre'],
        'escolaridad': escolaridad,
        'periodo': periodo
    }

    return render(request, 'home/boletas/lista_boletas.html', context)

def obtener_datos_boleta(pk, periodo):

    estudiante = Notas.objects.values(
        'estudiante__id',
        'ci_tipo',
        'ci',
        'estudiante__nombres',
        'estudiante__apellidos',
        'anio__nombre',
        'mencion__nombre',
        'seccion__nombre'
        ).filter(
            estudiante=pk,
            periodo=periodo
        ).first()

    notas = list(Notas.objects.filter(estudiante_id=estudiante['estudiante__id'], periodo=periodo).values(
        'lapso1', 'lapso2', 'lapso3', 'definitiva', 'materia__materia__nombre', 'materia__materia__literal', 'id', 'i_lapso1', 'i_lapso2', 'i_lapso3', 'total_i'
    ))

    for nota in notas:
        nota['materia__materia__literal'] = str(nota['materia__materia__literal']).lower()
    
    p_lapso1 = 0
    p_lapso2 = 0
    p_lapso3 = 0
    p_definitiva = 0
    pi_lapso1 = 0
    pi_lapso2 = 0
    pi_lapso3 = 0
    pi_total = 0
    d_lapso1 = 0
    d_lapso2 = 0
    d_lapso3 = 0
    d_definitiva = 0
    for nota in notas:
        p_lapso1 += nota['lapso1']
        p_lapso2 += nota['lapso2']
        p_lapso3 += nota['lapso3']
        d_lapso1 += 1 if nota['lapso1'] != 0 else 0
        d_lapso2 += 1 if nota['lapso2'] != 0 else 0
        d_lapso3 += 1 if nota['lapso3'] != 0 else 0
        d_definitiva += 1 if nota['definitiva'] != 0 else 0
        p_definitiva += nota['definitiva']
        pi_lapso1 += 0 if nota['i_lapso1'] == -1 else nota['i_lapso1']
        pi_lapso2 += 0 if nota['i_lapso2'] == -1 else nota['i_lapso2']
        pi_lapso3 += 0 if nota['i_lapso3'] == -1 else nota['i_lapso3']
        pi_total += nota['total_i']
    p_lapso1 = str(round(p_lapso1 / d_lapso1, 2)).replace('.', ',') if d_lapso1 != 0 else ''
    p_lapso2 = str(round(p_lapso2 / d_lapso2, 2)).replace('.', ',') if d_lapso2 != 0 else ''
    p_lapso3 = str(round(p_lapso3 / d_lapso3, 2)).replace('.', ',') if d_lapso3 != 0 else ''
    p_definitiva = str(round(p_definitiva / d_definitiva, 2)).replace('.', ',') if d_definitiva != 0 else ''

    promedios = {
        '1': p_lapso1,
        '2': p_lapso2,
        '3': p_lapso3,
        '4': p_definitiva
    }

    inasistencias = {
        '1': pi_lapso1,
        '2': pi_lapso2,
        '3': pi_lapso3,
        '4': pi_total,
    }

    return notas, promedios, inasistencias, estudiante

@login_required(login_url="/login/")
def generar_boleta(request, pk):

    periodo = request.GET.get('periodo')
    periodo_nombre = PeriodosAcademicos.objects.values('nombre').filter(id=periodo).first()

    notas, promedios, inasistencias, estudiante = obtener_datos_boleta(pk, periodo)

    table = 'home/form-content/planillas_form.html'
    context={
        'segment':'boleta',
        'title':'Generar boletas',
        'buscar':True,
        'table':table,
        'estudiante': estudiante,
        'periodo': periodo_nombre['nombre'],
        'promedios': promedios,
        'inasistencias': inasistencias,
        'notas': notas
    }

    return render(request, 'home/boletas/boleta.html', context)

@login_required(login_url="/login/")
def actualizar_inasistencias(request, pk):
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    tiempo = data.get('tiempo')
    materia = data.get('id_materia')
    periodo = data.get('periodo')
    inasistencia = data.get('inasistencia')
    if str(inasistencia).lower() == 'in':
        inasistencia = -1
    elif inasistencia == '':
        inasistencia = 0

    materia = Notas.objects.get(id=materia)

    setattr(materia, f'i_{tiempo}', inasistencia)

    if inasistencia != -1:
        i_lapso1 = 0 if materia.i_lapso1 == -1 else materia.i_lapso1
        i_lapso2 = 0 if materia.i_lapso2 == -1 else materia.i_lapso2
        i_lapso3 = 0 if materia.i_lapso3 == -1 else materia.i_lapso3
        if tiempo == 'lapso1':
            total_ins = int(inasistencia) + i_lapso2 + i_lapso3
        elif tiempo == 'lapso2':
            total_ins = int(inasistencia) + i_lapso1 + i_lapso3
        elif tiempo == 'lapso3':
            total_ins = int(inasistencia) + i_lapso1 + i_lapso2     
        setattr(materia, 'total_i', total_ins)

    materia.save()

    notas, promedios, inasistencias, estudiante = obtener_datos_boleta(pk, periodo)

    return JsonResponse({"message": "Los datos se actualizaron correctamente.", "notas": notas, "promedios": promedios, "inasistencias": inasistencias, "estudiante": estudiante}, status=200)

@login_required(login_url="/login/")
def agregar_materia_pendiente(request, pk):

    periodo_id = DatosPlantel.objects.values('periodo').all().first()
    periodo = PeriodosAcademicos.objects.get(id=periodo_id['periodo'])
    estudiante = Estudiantes.objects.get(id=pk)
    anio = Anios.objects.get(posicion=(estudiante.anio.posicion-1))

    if request.POST:
        materia = request.POST.get('materia')
        materia = MateriasAniosMenciones.objects.get(id=materia)

        Notas.objects.create(materia=materia, estudiante=estudiante, periodo=periodo, anio=anio, mencion=estudiante.mencion, seccion=estudiante.seccion, ci_tipo=estudiante.ci_tipo, ci=estudiante.ci, tipo='p')

    form_materias = MateriasForm(anio=anio.id,mencion=estudiante.mencion)

    data_table = Notas.objects.values('id', 'materia__materia__nombre').filter(estudiante=pk, periodo=periodo_id['periodo'], tipo='p')

    content = 'home/materias/formu_agregar_pendientes.html'
    context = {
        'segment':'estudiantes',
        'title':'Materias Pendientes',
        'table':content,
        'form':form_materias,
        'data_table':data_table
    }

    return render(request, 'home/table.html', context)

@login_required(login_url="/login/")
def eliminar_materia_pendiente(request, pk):
    materia = Notas.objects.get(id=pk)
    materia.delete()

    return JsonResponse({"message": "Los datos se actualizaron correctamente."}, status=200)
