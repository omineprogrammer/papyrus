from django.contrib import admin
from apps.consumibles.models import *


# Define the admin class
class MovimientosAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo_movimiento', 'cantidad', 'consumible')

# Register your models here.
admin.site.register(Color)
admin.site.register(Proveedor)
admin.site.register(Consumible)
admin.site.register(Movimiento, MovimientosAdmin)

