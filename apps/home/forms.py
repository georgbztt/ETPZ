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
