from django.contrib import admin
from django.template.loader import get_template
from django.contrib.admin.options import TabularInline

from .models import *

class NotaInlineAdmin(admin.TabularInline):
    model = Nota

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'ci')
    fields = (
            ('nombre', 'apellido'),
            ('ci_tipo', 'ci')
    )

@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    inlines = [NotaInlineAdmin]
    list_display = ('estudiante','periodo')
    fields = (
            ('estudiante', 'periodo'),
            'nota_inline'
            )
    
    readonly_fields = ('nota_inline',)
    
    def nota_inline(self, *args, **kwargs):
        context = getattr(self.response, 'context_data', None) or {}
        if context['inline_admin_formsets']:
            inline = context['inline_admin_formset'] = context['inline_admin_formsets'].pop(0)
            print(inline)
            return get_template(inline.opts.template).render(context, self.request)#type:ignore
        else:
            print('inline is empty')
            return get_template(inline.opts.template).render(self.request)#type:ignore
    
    def render_change_form(self, request, *args, **kwargs):
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response
    
admin.site.register(Materia)
admin.site.register(Nota)