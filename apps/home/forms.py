"""
Copyright (c) 2023 - present, Daniel Escalona
"""
from django import forms
from django.core.validators import *
from django.forms.models import inlineformset_factory, modelform_factory, modelformset_factory, formset_factory#, BaseFormSet

from django.forms import *
from .models import *

class BaseInlineFormset(BaseInlineFormSet):#Builder para los formsets
    def get_deletion_widget(self):
        return CheckboxInput(attrs={'class': 'form-check-input justify-content-center'}),

class MateriaForm(ModelForm):
    class Meta:
        model = Materia
        fields = (
            'nombre',
            )
        widgets ={
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}),
        }

class CargaForm(ModelForm):
    class Meta:
        model = Carga
        fields = (
            'titulo',
            'materias',
            )
        widgets ={
            'titulo': TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}),
            'materias': SelectMultiple(attrs={'class': 'form-control'}),
        }

class EstudianteForm(ModelForm):
    class Meta:
        model = Estudiante
        fields = (
            'ci',
            'ci_tipo',
            'nombre',
            'apellido',
            'entidad_federal',
            'periodo',
            )
        widgets ={
            'ci': TextInput(attrs={'class': 'form-control'}),
            'ci_tipo': Select(attrs={'class': 'form-control'}),
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'apellido': TextInput(attrs={'class': 'form-control'}),
            'entidad_federal': TextInput(attrs={'class': 'form-control'}),
            'periodo': Select(attrs={'class': 'form-control'}),
        }

class NotasForm(ModelForm):
    class Meta:
        model = Nota
        fields = (
            'lapso_1',
            'lapso_2',
            'lapso_3',
            'reparacion',
        )
        widgets = {
            'lapso_1': TextInput(attrs={'class':'form-control', 'placeholder':'Lapso 1'}),
            'lapso_2': TextInput(attrs={'class':'form-control', 'placeholder':'Lapso 2'}),
            'lapso_3': TextInput(attrs={'class':'form-control', 'placeholder':'Lapso 3'}),
            'reparacion': TextInput(attrs={'class':'form-control', 'placeholder':'Resparación'}),
        }
   

'''Forms de ejemplo que saqué de otro proyecto
class TestRequestForm(ModelForm):
    class Meta:
        model = TestRequest
        fields = (
            'format', 
            'number', 
            'date',
            'company', 
            'origin', 
            'check_test_client', 
            'test_client', 
            'client', 
            #art
            'art_number', 
            'art_date', 
            'product', 
            'design', 
            'layers', 
            #TestStructure
            'plan', 
            'print_selector',
            'printer', 
            'surface_selector',
            'surface_over',
            'reverse_selector',
            'reverse_over',
            'colors',
            #Lamination
            'lamination_selector',
            #dimendiosns
            'dist_boder_cell_material',
            'repetition',
            'width_photo',
            'lenght_photo',
            #bobbin
            'check_bobbin',
            'width_bobbin',
            'exterior_dia_bobbin',
            'core_dia_bobbin',
            'winding',
            #ream
            'check_ream',
            'width_ream',
            'lenght_ream',
            'weight_ream',
            #production
            'quantity', 
            'unit', 
            'tolerance',
            'observation', 
            #production
            'applicant', 
            'elaborator', 
            'reviewer',
            #checks 
            'pre_print', 
            'colorimetry', 
            'plan_crx', 
            'plan_mcl', 
            'logistics', 
            'quality'
            )
            
        widgets ={
            'format': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Formato', 'id':'format'}),
            'number': TextInput(attrs={'class':'form-control align-items-center myform-focus text-center', 'style':'text-transform: uppercase !important;', 'placeholder':'00000000', 'id':'number'}),
            'date': DateInput(attrs={'class':'form-control align-items-center myform-focus text-center', 'autocomplete':'off', 'placeholder':'DD/MM/AAAA', 'id':'date'}),
            'company': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Empresa', 'id':'company'}),
            'origin': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Origen', 'id':'origin'}),
            'check_test_client': CheckboxInput(attrs={'aria-label':'Cliente de Prueba', 'id':'check_test_client', 'style':'display: none'}),
            'test_client':TextInput(attrs={'class':'form-control align-items-center myform-focus text-center', 'placeholder':'Nombre...', 'id':'test_client'}),
            'client': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Cliente', 'id':'client'}),
            #art
            'art_number': TextInput(attrs={'class':'form-control align-items-center myform-focus text-center', 'style':'text-transform: uppercase !important;', 'placeholder':'00000000', 'id':'art_number'}),
            'art_date': DateInput(attrs={'class':'form-control align-items-center myform-focus text-center', 'autocomplete':'off', 'placeholder':'DD/MM/AAAA', 'id':'art_date'}),
            'product': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'Nombre completo del Producto', 'id':'product' }),
            'design': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Diseño', 'placeholder':'', 'id':'design' }),
            'layers': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Origen', 'id':'layers'}),
            #_TestStructure
            #'plan':
            'print_selector': CheckboxInput(attrs={'class':'form-check-input justify-content-center', 'aria-label':'Sobre superficie', 'id':'print_selector'}),
            'printer': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Impresora', 'id':'printer'}),
            'surface_selector': CheckboxInput(attrs={'class':'form-check-input justify-content-center', 'aria-label':'Sobre superficie', 'id':'surface_selector'}),
            'surface_over': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Sustrato', 'placeholder':'Sobre', 'id':'surface_over', 'disabled':'' }),
            'reverse_selector': CheckboxInput(attrs={'class':'form-check-input justify-content-center', 'aria-label':'Sobre reverso', 'id':'reverse_selector'}),
            'reverse_over': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Sustrato', 'placeholder':'Sobre', 'id':'reverse_over', 'disabled':'' }),
            'colors': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'Colores', 'id':'colors' }),
            #_Lamination
            'lamination_selector': CheckboxInput(attrs={'class':'form-check-input justify-content-center', 'aria-label':'Sobre superficie', 'id':'lamination_selector'}),
            #dimensions
            'dist_boder_cell_material': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'dist_boder_cell_material'}),
            'repetition': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'repetition', 'style':'padding-right: 1.3em !important'}),
            'width_photo': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'width_photo'}),
            'lenght_photo': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'lenght_photo'}),
            #bobbin
            'check_bobbin': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Bobina', 'id':'check_bobbin'}),
            'width_bobbin': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'width_bobbin', 'style':'padding-right: 1.3em !important'}),
            'exterior_dia_bobbin': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'exterior_dia_bobbin'}),
            'core_dia_bobbin': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Diámetro de corte bobina', 'id':'core_dia_bobbin'}),
            'winding': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Nombre completo del Producto', 'placeholder':'Sentido de embobinado', 'id':'winding' }),
            #ream
            'check_ream': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Resma', 'id':'check_ream'}),
            'width_ream': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'width_ream'}),
            'lenght_ream': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'lenght_ream'}),
            'weight_ream': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'Nombre completo del Producto', 'placeholder':'0', 'id':'weight_ream'}),
            'quantity': NumberInput(attrs={'class': 'form-control myform-focus text-center justify-content-center', 'min':'0', 'aria-label':'Cantidad', 'placeholder':'0', 'id':'quantity'}),
            'unit': Select(attrs={'class': 'form-control myform-focus text-center', 'aria-label':'Unidad', 'id':'unit'}),
            'tolerance': NumberInput(attrs={'class': 'form-control myform-focus text-center justify-content-center', 'min':'0', 'aria-label':'Tolerancia', 'placeholder':'0', 'id':'tolerance'}),
            #'observation':
            #evaluators
            'applicant': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'', 'placeholder':'Nombre/Departamento', 'id':'applicant'}),
            'elaborator': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'', 'placeholder':'Nombre, Apellido y/o Cargo', 'id':'elaborator'}),
            'reviewer': TextInput(attrs={'class':'form-control align-items-center myform-focus', 'aria-label':'', 'placeholder':'Nombre, Apellido y/o Cargo', 'id':'reviewer'}),
            #checks
            'pre_print': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Seleccionar Pre-Prensa', 'id':'pre_print'}),
            'colorimetry': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Seleccionar Colorimetría', 'id':'colorimetry'}),
            'plan_crx': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Seleccionar Planif. Curex', 'id':'plan_crx'}),
            'plan_mcl': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Seleccionar Planif. Morrocel', 'id':'plan_mcl'}),
            'logistics': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Seleccionar Logística', 'id':'logistics'}),
            'quality': CheckboxInput(attrs={'class': 'form-check-input justify-content-center', 'aria-label':'Seleccionar Calidad', 'id':'quality'}),
        }

      
class PrinterForm(ModelForm):
    class Meta:
        model = Printer
        fields = (
            'name',
            )
        widgets ={
            'name': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'Nombre'})
        },
        can_delete=True

class LaminatorBootForm(ModelForm):    
    class Meta:
        model = LaminatorBoot
        fields = (            
            'production_order',
            'laminator',
            'date_time',
            'turn',
            'code',
            'machine_speed',
            'check_crown_treatment',
            'step',
            'st_1',
            'st_2',
            'st_3',
            'st_4',
            'adhesive',
            'batch',
            'formula',
            #Essay Formset
            'time',
            'temp',
            'observation',
            'quality_analist',
            'production_operator',
        )
        widgets = {
            'production_order': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'production_order'}),
            'laminator': Select(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'laminator'}),
            'date_time': DateTimeInput(attrs={'class': 'form-control myform-focus', 'autocomplete':'off', 'placeholder':'', 'id':'date_time'}),
            'turn': Select(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'turn'}),
            'code': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'code'}),
            'machine_speed': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'machine_speed'}),
            'check_crown_treatment': CheckboxInput(attrs={'class':'form-check-input justify-content-center', 'id':'check_crown_treatment'}),
            'step': Select(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'step'}),
            'st_1': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'st_1'}),
            'st_2': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'st_2'}),
            'st_3': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'st_3'}),
            'st_4': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'st_4'}),
            'adhesive': Select(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'adhesive'}),
            'batch': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'batch'}),
            'formula': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'formula'}),
            #Essay Formset
            'time': NumberInput(attrs={'class': 'form-control myform-focus text-center', 'min':'0', 'placeholder':'0', 'id':'time'}),
            'temp': NumberInput(attrs={'class': 'form-control myform-focus text-center', 'min':'0', 'placeholder':'0', 'id':'temp'}),
            #observation
            'quality_analist': Select(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'quality_analist'}),
            'production_operator': Select(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'id':'production_operator'}),
        }

LaminationEssayFormset = inlineformset_factory(LaminatorBoot, LaminationEssay,
        fields = (
            'essay',
            'result_t',
            'result_a',
            'result_b',
            'result_c',
        ),
        formset=BaseInlineFormset,
        widgets = { 
            'essay': Select(attrs={'class': 'form-control myform-focus text-center'}),
            'result_t': TextInput(attrs={'class': 'form-control myform-focus', 'placeholder':'', 'style':'padding-right: 1.3em !important'}),
            'result_a': NumberInput(attrs={'class': 'form-control myform-focus text-center', 'min':'0', 'placeholder':'A'}),
            'result_b': NumberInput(attrs={'class': 'form-control myform-focus text-center', 'min':'0', 'placeholder':'B'}),
            'result_c': NumberInput(attrs={'class': 'form-control myform-focus text-center', 'min':'0', 'placeholder':'C'}),
        }, 
        extra=2,
        )
        '''