from django.db import models
from apps.inventario.models import Impresora, ModeloImpresora
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
    codigo_proveedor = models.CharField(max_length=64, blank=True)
    cantidad_existente = models.PositiveIntegerField(default=0)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    compatibilidad_con = models.ManyToManyField(ModeloImpresora)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    descripcion = models.TextField(max_length=256, blank=True, verbose_name='Notaciones')

    def compatible_con(self):
        return ", ".join([c.__str__() for c in self.compatibilidad_con.all()])

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper()
        super(Consumible, self).save(*args, **kwargs)

    def __str__(self):
        if self.codigo_proveedor:
            return self.codigo + ' (' + self.codigo_proveedor + ', ' + self.proveedor + ')'
        return self.codigo


class Movimiento(models.Model):
    tipos_movimiento = (
        (0, 'ingreso'),
        (1, 'salida'),
        (2, 'ingreso de cuadre'),
        (3, 'salida de cuadre'),
    )
    id_solicitudes = getLastSubListRequesterTicket()

    fecha = models.DateTimeField(default=timezone.datetime.now)
    tipo_movimiento = models.IntegerField(choices=tipos_movimiento, default=1)
    cantidad = models.PositiveIntegerField(default=1, validators=[noEqual0])
    consumible = models.ForeignKey(Consumible, on_delete=models.PROTECT, null=False)
    id_solicitud = models.BigIntegerField(choices=id_solicitudes, null=True, blank=True, verbose_name='ticket en freshservice')
    impresora = models.ForeignKey(Impresora, on_delete=models.PROTECT, blank=True, null=True)
    descripcion = models.TextField(max_length=256, blank=True)

    def __str__(self):
        return datetime.strftime(self.fecha, '%A, %m/%d/%Y %I:%M %p') + ' | ' + self.tipos_movimiento[self.tipo_movimiento][1] + ' ' + str(self.cantidad) + ' consumibles ' + self.consumible.codigo

    def clean(self):
        self.clean_fields(exclude=['id_solicitud', 'cantidad'])
        # CHECK: si es movimiento de salida la cantidad se convierte en negativa (los movimientos de codigo par son ingresos)
        _cantidad = self.cantidad
        if self.tipo_movimiento % 2 != 0:
            _cantidad *= -1

        # CHECK: cantidad de consumibles en stock antes de cada operacion
        if self.consumible:
            _consumible = Consumible.objects.filter(id=self.consumible.id).first()
            if not self.impresora in list(_consumible.compatibilidad_con.all()):
                raise ValidationError({
                    'impresora': ValidationError(
                        'Consumible no compatible con impresora {}'.format(self.impresora))
                })

        # CHECK: si el consumible no es compatible con la impresora
        if self.consumible:
            _consumible = Consumible.objects.filter(id=self.consumible.id).first()
            if not _consumible.cantidad_existente + _cantidad >= 0:
                raise ValidationError({'cantidad': ValidationError('Cantidad en stock no es suficiente para la operacion')})

        # si se especifico una impresora
        if self.impresora:
            # CHECK: salida de impresora en operacion o en reparacion
            impresora_estado = self.impresora.estado
            if impresora_estado == 0:
                raise ValidationError({'impresora': ValidationError('Impresora no esta asignada')})
            elif impresora_estado == 2:
                raise ValidationError({'impresora': ValidationError('Impresora esta averiada')})
            elif impresora_estado == 3:
                raise ValidationError({'impresora': ValidationError('Impresora esta en reparacion')})
            elif impresora_estado == 4:
                raise ValidationError({'impresora': ValidationError('Impresora esta dada de baja')})
        # sino se especifico impresora validar que no sea un movimiento de salida, de no ser asi, se lanza excepcion
        elif self.tipo_movimiento % 2 != 0:
            raise ValidationError({'impresora': ValidationError('Si es un movimiento "' + self.tipos_movimiento[self.tipo_movimiento][1] + '" se debe especificar una impresora')})

    def save(self, *args, **kwargs):
        _cantidad = self.cantidad
        if self.tipo_movimiento % 2 != 0:
            _cantidad *= -1
        _consumible = Consumible.objects.filter(id=self.consumible.id)[0]
        if _consumible.cantidad_existente + _cantidad >= 0:
            _consumible.cantidad_existente += _cantidad
            _consumible.save()
            super(Movimiento, self).save(*args, **kwargs)
