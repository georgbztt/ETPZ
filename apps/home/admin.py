from django.contrib import admin
from django.template.loader import get_template
from django.contrib.admin.options import TabularInline

from .models import DatosPlantel

admin.site.register(DatosPlantel)