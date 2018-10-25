from django.contrib import admin
from apps.inventario.models import *

# Register your models here.
admin.site.register(TipoImpresion)
admin.site.register(FabricanteImpresora)
admin.site.register(ModeloImpresora)
admin.site.register(Edificio)
admin.site.register(Ubicacion)
admin.site.register(Empresa)
admin.site.register(Departamento)
admin.site.register(Usuario)
admin.site.register(Impresora)
admin.site.register(Asignacion)