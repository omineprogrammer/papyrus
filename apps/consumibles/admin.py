from django.contrib import admin
from apps.consumibles.models import *


# Define the admin class
class MovimientosAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo_movimiento', 'cantidad', 'consumible')

class ConsumibleAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'cantidad_existente', 'color', 'compatible_con', 'proveedor'
    ]


# Register your models here.
admin.site.register(Color)
admin.site.register(Proveedor)
admin.site.register(Consumible, ConsumibleAdmin)
admin.site.register(Movimiento, MovimientosAdmin)

