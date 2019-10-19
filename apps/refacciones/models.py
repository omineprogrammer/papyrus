from django.db import models
from django.utils import timezone
from apps.core.inventory.models import Vendor, TypeItem
from apps.inventario.models import Usuario


# Create your models here.
class Modelo(models.Model):
    nombre = models.CharField(max_length=64)
    fabricante = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    tipo_item = models.ForeignKey(TypeItem, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=256, null=True, blank=True)

class Refaccion(models.Model):
    estados = (
        (0, 'En Stock'),
        (1, 'Asignado'),
        (2, 'Averiado'),
        (3, 'En Reparacion'),
        (4, 'De Baja'),
    )
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT)
    serial = models.CharField(max_length=24, unique=True)
    estado = models.IntegerField(choices=estados, default=0)
    descripcion = models.CharField(max_length=256, null=True, blank=True)

class Asignacion(models.Model):
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Asignaciones"

    def __str__(self):
        if self.usuario:
            asigned = self.usuario.__str__()
        elif self.departamento:
            asigned = self.departamento.__str__()
        return self.impresora.modelo.__str__() + " de " + asigned

    def save(self, *args, **kwargs):
        impresora = self.impresora
        impresora.estado = 1
        impresora.save()
        super(Asignacion, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        impresora = self.impresora
        # marcar impresora como en stock
        impresora.estado = 0
        impresora.save()
        super(Asignacion, self).delete(*args, **kwargs)
