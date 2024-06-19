#import datetime, decimal
from urllib import request
from django import template
from django.db import IntegrityError, transaction 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms import formset_factory
from django.template import loader
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import PlantelForm, PeriodosForm, AniosForm, MencionesForm, ProfesorForm
from .models import DatosPlantel, PeriodosAcademicos, Menciones, Secciones, AniosMencionSec
from .models import *
from .forms import *
from .forms import PlantelForm, PeriodosForm, AniosForm, MencionesForm, EstudiantesForm
from .models import Anios, DatosPlantel, Materias, PeriodosAcademicos, Menciones, Secciones, AniosMencionSec, MateriasAniosMenciones

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

    table = 'home/form-content/planillas_form.html'
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planilla Registro de Titulos',
        'buscar':True,
        'table':table,
    }
    
    return render(request, 'home/table.html', context)

@login_required(login_url="/login/")
def finales(request):

    table = 'home/form-content/planillas_form.html'
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planilla Finales',
        'buscar':True,
        'table':table,
    }
    
    return render(request, 'home/planillas/finales.html', context)

def revision(request):

    table = 'home/form-content/planillas_form.html'
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planilla Revisión',
        'buscar':True,
        'table':table,
    }
    
    return render(request, 'home/table.html', context)

def materiaPendientes(request):

    table = 'home/form-content/planillas_form.html'
    context={
        'planillas':planillas,
        'segment':'planilla',
        'title':'Planilla Materia Pendientes',
        'buscar':True,
        'table':table,
    }
    
    return render(request, 'home/table.html', context)


### Seccion de Carga de Notas ###

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




### Seccion de profesores ###

@login_required(login_url="/login/")
def profesores(request):
    table = 'home/table-content/profesores.html'
    context= {  
        'profesores': profesores,
        'segment':'profesores',
        'title': 'Profesores',
        'buscar': True,
        'table': table,
    }

    return render(request, 'home/table.html', context)


@login_required(login_url="/login/")
def crearProfesores(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():

            Profesores.objects.create(**form.cleaned_data)
            
            print("")
            print(form.cleaned_data)
            print("")

    form = ProfesorForm()

    content = 'home/form-content/crear_profesor_form.html'
    context = {
        'form':form,
        'segment':'profesores',
        'title':'Crear Profesor',
        'table':content
    }

    return render(request, 'home/table.html', context)


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

    form = PeriodosForm()

    data_table = list(PeriodosAcademicos.objects.values('nombre'))

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

        datos = request.POST.copy()
        datos.pop('seccion')
        datos.pop('csrfmiddlewaretoken')

        for id_anio in datos:

            list_menciones = datos.getlist(str(id_anio))

            inst_anio = Anios.objects.get(id=id_anio)

            for id_mencion in list_menciones:

                inst_mencion = Menciones.objects.get(id=id_mencion)

                AniosMencionSec.objects.create(anio=inst_anio, mencion=inst_mencion, seccion=inst_seccion)

    anios = list(Anios.objects.values('id', 'nombre'))
    menciones = list(Menciones.objects.values('id', 'nombre', 'nombre_abrev'))

    form = ''

    form += f"""
    <div class="col-1">
        <div class="form-group">
            <label for="seccion">Seccion</label>
            <input type="text" name="seccion" class="form-control" id="seccion" required>
        </div>
    </div>
    <div class="w-100"></div>
    <p>Seleccione las menciones a las cuales pertenece la seccion a crear</p>
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
def editar_seccion(request):

    if request.method == 'POST':

        seccion = request.POST.get('seccion')

        inst_seccion = Secciones.objects.create(nombre=seccion)

        datos = request.POST.copy()
        datos.pop('seccion')
        datos.pop('csrfmiddlewaretoken')

        for id_anio in datos:

            list_menciones = datos.getlist(str(id_anio))

            inst_anio = Anios.objects.get(id=id_anio)

            for id_mencion in list_menciones:

                inst_mencion = Menciones.objects.get(id=id_mencion)

                AniosMencionSec.objects.create(anio=inst_anio, mencion=inst_mencion, seccion=inst_seccion)

    anios = list(Anios.objects.values('id', 'nombre'))
    menciones = list(Menciones.objects.values('id', 'nombre', 'nombre_abrev'))

    form = ''

    form += f"""
    <div class="col-1">
        <div class="form-group">
            <label for="seccion">Seccion</label>
            <input type="text" name="seccion" class="form-control" id="seccion" required>
        </div>
    </div>
    <div class="w-100"></div>
    <p>Seleccione las menciones a las cuales pertenece la seccion a crear</p>
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

    content = 'home/configuracion/editar-seccion.html'
    context = {
        'form':form,
        'segment':'configuracion',
        'title':'Editar seccion',
        'table':content,
        'url_back': '/configuracion/secciones'
    }

    return render(request, 'home/table.html', context)

### Crear Años ###
@login_required(login_url="/login/")
def crearAnios(request):
    
    if request.method == 'POST':
        form = AniosForm(request.POST)
        if form.is_valid():
            
            Anios.objects.create(**form.cleaned_data)

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


### Crear Menciones ###
@login_required(login_url="/login/")
def crearMenciones(request):
    
    if request.method == 'POST':
        form = MencionesForm(request.POST)
        if form.is_valid():
            
            try:
                Menciones.objects.create(**form.cleaned_data)
            except IntegrityError as e:
                if 'unique constraint' in str(e.args):
                    return HttpResponse("Esta mención ya existe. Inténtalo de nuevo.", status=400)

    form = MencionesForm()

    data_table = Menciones.objects.values('nombre', 'nombre_abrev')

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

@login_required(login_url="/login/")
def Estudiante(request):
    
    form = EstudiantesForm()

    content = 'home/estudiantes/estudiante_crear.html'
    context = {
        'form':form,
        'segment':'Estudiantes',
        'title':'Crear Estudiante',
        'table':content,
    }

    return render(request, 'home/table.html', context)

@login_required
def materiaCrear(request):

    if request.method == 'POST':

        materia = request.POST.get('materia')
        abrev = request.POST.get('abrev')

        inst_materia = Materias.objects.create(nombre=materia, nombre_abrev=abrev)

        datos = request.POST.copy()
        datos.pop('materia')
        datos.pop('abrev')
        datos.pop('csrfmiddlewaretoken')

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
        'table':content
    }
    
    return render(request, 'home/table.html', context)
      
@login_required(login_url="/login/")
def Cargar_Notas(request):

    table = 'home/form-content/planillas_form.html'
    context={
        'Cargar_Notas':Cargar_Notas,
        'segment':'Cargar_Notas',
        'title':'',
        'buscar':True,
        'table':table,
    }
    
    return render(request, 'home/Cargar_Notas/notas.html', context)

@login_required(login_url="/login/")
def notas(request):
    
    content = 'home/Cargar_Notas/index.html'
    context = {
        'segment':'notas',
        'title':'Notas',
        'table':content
    }
    
    return render(request, 'home/table.html', context)


@login_required(login_url="/login/")
def materiaEditar(request, pk):

    try:

        materia = Materias.objects.get(id=pk)

        if request.method == 'POST':

            nombre_materia = request.POST.get('materia')
            abrev = request.POST.get('abrev')

            setattr(materia, "nombre", nombre_materia)
            setattr(materia, "nombre_abrev", abrev)

            materia.save()

            datos = request.POST.copy()
            datos.pop('materia')
            datos.pop('abrev')
            datos.pop('csrfmiddlewaretoken')

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
            'table':content
        }
        
        return render(request, 'home/table.html', context)
    except ObjectDoesNotExist:
        print("El objeto con el ID dado no existe en la base de datos.")
        return render(request, 'home/page-404.html')

    