from django.contrib import admin
from apps.inventario.models import *
from tools.admin.actions_custom import *


# Define the admin class
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'impresora', 'estado', 'ubicacion', 'departamento', 'usuario')
    actions = ['asignacion_change_impresora_estadoStock']

    # def impresora_estado(self, ):
    def asignacion_change_impresora_estadoStock(modeladmin, request, queryset):
        for obj in queryset:
            print(obj.impresora.modelo)
        # queryset.update(estado=1)

    asignacion_change_impresora_estadoStock.short_description = "Marcar Impresora/s como en Stock"


class ImpresoraAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'serial', 'empresa_propietario', 'estado', 'ultima_asignacion']


# Register your models here.
admin.site.register(TipoImpresion)
admin.site.register(FabricanteImpresora)
admin.site.register(Edificio)
admin.site.register(Ubicacion)
admin.site.register(Empresa)
admin.site.register(Departamento)
admin.site.register(Usuario)
admin.site.register(ModeloImpresora)
admin.site.register(Impresora, ImpresoraAdmin)
admin.site.register(Asignacion)



