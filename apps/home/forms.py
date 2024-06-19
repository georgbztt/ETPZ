"""
Copyright (c) 2023 - present, Daniel Escalona
"""
from django import forms
from django.core.validators import *
from .models import *

class PlantelForm(forms.Form):
    codigo = forms.CharField(label="Código del plantel", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label="Nombre", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label="Dirección", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.IntegerField(label="Teléfono", required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    municipio = forms.CharField(label="Municipio", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    entidad_federal = forms.CharField(label="Entidad federal", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zona_educativa = forms.CharField(label="Zona educativa", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    distrito_escolar = forms.CharField(label="Distrito escolar", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    director = forms.CharField(label="Director", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ci_tipo = forms.ChoiceField(choices=[("V", "V"), ("E", "E")], required=True, widget=forms.Select(attrs={'class': 'form-control bg-light border-0 br-start'}))
    ci = forms.IntegerField(label="Cédula", required=True, widget=forms.NumberInput(attrs={'class': 'form-control padding-left-10px'}))


class ProfesorForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(label="Apellido", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ci_tipo = forms.ChoiceField(choices=[("V", "V"), ("E", "E")], required=True, widget=forms.Select(attrs={'class': 'form-control bg-light border-0 br-start'}))
    ci = forms.IntegerField(label="Cédula", required=True, widget=forms.NumberInput(attrs={'class': 'form-control padding-left-10px'}))

class SeccionesForm(forms.Form):
    nombre = forms.CharField(label="Sección", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PeriodosForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class AniosForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class MencionesForm(forms.Form):
    nombre = forms.CharField(label="Ingrese el nombre mención", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_abrev = forms.CharField(label="Ingrese la abreviatura de la mención", max_length=5, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
class EstudiantesForm(forms.Form):
    ci = forms.IntegerField(label="Cédula", required=True, widget=forms.NumberInput(attrs={'class': 'form-control padding-left-10px'}))
    ci_tipo = forms.ChoiceField(choices=[("V", "V"), ("E", "E")], required=True, widget=forms.Select(attrs={'class': 'form-control bg-light border-0 br-start'}))
    nombres = forms.CharField(label="Nombres", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(label="Apellidos", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexo = forms.ChoiceField(choices=[("M", "M"), ("F", "F")], required=True, widget=forms.Select(attrs={'class': 'form-control text-center p-2'}))
    fecha_de_nacimiento = forms.DateField(label="Fecha de nacimiento", required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date', 'id':'fecha'}))
    anio_id = forms.ChoiceField(label="Año", required=True, widget=forms.Select(attrs={'class': 'form-control text-center p-2'}))
    mencion_id = forms.ChoiceField(label="Mención", required=True, widget=forms.Select(attrs={'class': 'form-control text-center p-2'}))
    seccion_id = forms.ChoiceField(label="Sección", required=True, widget=forms.Select(attrs={'class': 'form-control text-center p-2'}))
    entidad_federal = forms.CharField(label="Entidad federal", max_length=3, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lugar_de_nacimiento =  forms.CharField(label="Lugar de nacimiento", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        
    def __init__(self, *args, **kwargs):
        super(EstudiantesForm, self).__init__(*args, **kwargs)
        self.fields['anio_id'].choices = [('', '')] + [(anio.id, anio.nombre) for anio in Anios.objects.all()]
        self.fields['mencion_id'].choices = [('', '')] + [(mencion.id, mencion.nombre_abrev) for mencion in Menciones.objects.all()]
        self.fields['seccion_id'].choices = [('', '')] + [(seccion.id, seccion.nombre) for seccion in Secciones.objects.all()]

        

        


