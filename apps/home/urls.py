from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    
    path('planillas', views.planillas, name='planilla'),
    path('planillas/registro-titulos',views.registroTitulos, name='registro_titulos'),
    path('planillas/materia-pendientes',views.materiaPendientes, name='materia_pendientes'),
    path('planillas/finales',views.finales, name='finales'),
    path('planillas/revision',views.revision, name='revision'),

    path('profesores', views.profesores, name='profesores'),
    
    path('materias', views.materias, name='materia'),
    path('materias/crear', views.materiaCrear, name='materia_crear'),
    path('materias/<str:pk>/editar', views.materiaEditar, name='materia_editar'),
    path('materias/<str:pk>/eliminar', views.materiaEliminar, name='materia_eliminar'),

    path('cargas', views.cargas, name='carga'),
    path('cargas/crear', views.cargaCrear, name='carga_crear'),
    path('cargas/<str:pk>/editar', views.cargaEditar, name='carga_editar'),
    path('cargas/<str:pk>/eliminar', views.cargaEliminar, name='carga_eliminar'),

    path('estudiantes', views.estudiantes, name='estudiante'),
    path('estudiantes/crear', views.estudianteCrear, name='estudiante_crear'),
    path('estudiantes/<str:pk>/editar', views.estudianteEditar, name='estudiante_editar'),
    path('estudiantes/<str:pk>/eliminar', views.estudianteEliminar, name='estudiante_eliminar'),
    path('estudiantes/<str:pk>/inasistencias', views.estudianteInasistencias, name='estudiante_inasistencias'),
    path('estudiantes/<str:pk>/<str:dir>/<str:periodo_sel>', views.estudianteVer, name='estudiante_ver'),

    path('notas/<str:pk>/editar', views.editarNotas, name='editar_notas'),
    path('notas/<str:pd>/carga', views.carga_notas, name='carga_notas'),
    path('notas/<str:pk>/<str:dir>/<str:periodo_sel>', views.estudianteVer, name='imprimir_notas'),

    path('periodos', views.periodos, name='periodo'),
    path('periodos/crear', views.periodoCrear, name='periodo_crear'),
    path('periodos/<str:pk>/editar', views.periodoEditar, name='periodo_editar'),
    path('periodos/<str:pk>/eliminar', views.periodoEliminar, name='periodo_eliminar'),
    path('periodos/cambiar/<str:periodo_actual>', views.cambiar_periodo, name='cambiar_periodo'),

    path('configuracion', views.configuracion, name='configuracion'),
    path('configuracion/periodos-academicos', views.crearPeriodoAcademico, name='crear_periodo'),
    path('configuracion/años', views.crearAnios, name='crear_anios'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
