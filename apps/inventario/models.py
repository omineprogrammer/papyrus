from django.db import models
from django.utils import timezone


class TipoImpresion(models.Model):
    nombre = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "tipo de impresiones"

    def __str__(self):
        return self.nombre


class FabricanteImpresora(models.Model):
    nombre = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "fabricantes de impresora"

    def __str__(self):
        return self.nombre


class Edificio(models.Model):
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=64)
    alias = models.CharField(max_length=64, null=True, blank=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "ubicaciones"

    def __str__(self):
        if self.alias:
            return self.nombre + " '" + self.alias + "' en " + self.edificio.__str__()
        else:
            return self.nombre + " en " + self.edificio.__str__()


class Empresa(models.Model):
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    nombre = models.CharField(max_length=32)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombre = models.CharField(max_length=32)
    apellido = models.CharField(max_length=32)
    cargo = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.nombre + " " + self.apellido


class ModeloImpresora(models.Model):
    fabricante = models.ForeignKey(FabricanteImpresora, on_delete=models.PROTECT)
    modelo = models.CharField(max_length=32)
    funcionalidad = models.BooleanField(default=True, verbose_name='es multi-funcional')
    tipo = models.ForeignKey(TipoImpresion, on_delete=models.PROTECT, verbose_name='tipo impresion')
    conexion_local = models.BooleanField(default=True, blank=True, verbose_name='tiene conexion USB')
    conexion_red_cableada = models.BooleanField(default=False, verbose_name='tiene conexion LAN')
    conexion_red_inalambrica = models.BooleanField(default=False, verbose_name='tiene conexion WiFi')

    class Meta:
        verbose_name_plural = "modelos de impresora"

    def __str__(self):
        return self.fabricante.__str__() + " " + self.modelo

class Impresora(models.Model):
    estados_choises = (
        (0, 'En Stock'),
        (1, 'Operativa'),
        (2, 'Averiada'),
        (3, 'En Reparacion'),
        (4, 'De Baja'),
    )

    id = models.AutoField(primary_key=True)
    modelo = models.ForeignKey(ModeloImpresora, on_delete=models.PROTECT)
    serial = models.CharField(max_length=16, unique=True)
    empresa_propietario = models.ForeignKey(Empresa, on_delete=models.PROTECT,  verbose_name='Propiedad de')
    estado = models.IntegerField(choices=estados_choises, default=0)
    ultima_asignacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        # return self.modelo.__str__() + " S/N:" + self.serial
        _str = self.modelo.__str__()
        asignacion = Asignacion.objects.filter(impresora=self.id)
        if asignacion:
            _str = asignacion[0].__str__()
        else:
            _str += " S/N:" + self.serial
        if self.estado == 2:
            _str += ' Averiada'
        elif self.estado == 3:
            _str += ' en Reparacion'
        elif self.estado == 0:
            _str += ' sin Asignar'
        return _str


class MyQuerySet(models.query.QuerySet):

    def delete(self):
        pass  # you can throw an exception


class NoDeleteManager(models.Manager):
    def get_query_set(self):
        return MyQuerySet(self.model, using=self._db)




class Asignacion(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    impresora = models.OneToOneField(Impresora, on_delete=models.PROTECT, null=False)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, null=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    # objects = NoDeleteManager()

    class Meta:
        verbose_name_plural = "asignaciones"

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




