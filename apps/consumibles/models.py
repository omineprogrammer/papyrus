from django.db import models
from apps.inventario.models import Impresora
from django.utils import timezone
from tools.tools import getLastSubListRequesterTicket
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.consumibles.validators import noEqual0



class Color(models.Model):
    nombre = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "colores"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "proveedores"

    def __str__(self):
        return self.nombre


class Consumible(models.Model):
    codigo = models.CharField(max_length=16)
    cantidad_existente = models.PositiveIntegerField(default=0)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    descripcion = models.TextField(max_length=256, blank=True, verbose_name='Notaciones')

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper()
        super(Consumible, self).save(*args, **kwargs)

    def __str__(self):
        return self.codigo


class Movimiento(models.Model):
    tipos_movimiento = (
        (0, 'ingreso'),
        (1, 'salida'),
        # (2, 'ingreso de cuadre'),
        # (3, 'salida de cuadre'),
    )
    id_solicitudes = getLastSubListRequesterTicket()

    fecha = models.DateTimeField(default=timezone.datetime.now)
    tipo_movimiento = models.IntegerField(choices=tipos_movimiento, default=1)
    cantidad = models.PositiveIntegerField(default=1, validators=[noEqual0])
    consumible = models.ForeignKey(Consumible, on_delete=models.PROTECT, null=False)
    id_solicitud = models.BigIntegerField(choices=id_solicitudes, verbose_name='id de ticket en freshservice')
    impresora = models.ForeignKey(Impresora, on_delete=models.PROTECT, blank=True, null=True)
    descripcion = models.TextField(max_length=256, blank=True)

    def __str__(self):
        return datetime.strftime(self.fecha, '%A, %m/%d/%Y %I:%M %p') + ' | ' + self.tipos_movimiento[self.tipo_movimiento][1] + ' ' + str(self.cantidad) + ' consumibles ' + self.consumible.codigo

    def clean(self):
        self.clean_fields(exclude=['id_solicitud', 'cantidad'])
        _cantidad = self.cantidad
        if self.tipo_movimiento % 2 != 0:
            _cantidad *= -1
        if self.consumible:
            _consumible = Consumible.objects.filter(id=self.consumible.id)[0]
            if not _consumible.cantidad_existente + _cantidad >= 0:
                raise ValidationError({'cantidad': ValidationError('Cantidad en stock no es suficiente para la operacion')})

    def save(self, *args, **kwargs):
        _cantidad = self.cantidad
        if self.tipo_movimiento % 2 != 0:
            _cantidad *= -1
        _consumible = Consumible.objects.filter(id=self.consumible.id)[0]
        if _consumible.cantidad_existente + _cantidad >= 0:
            _consumible.cantidad_existente += _cantidad
            _consumible.save()
            super(Movimiento, self).save(*args, **kwargs)
