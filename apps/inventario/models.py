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


class Edificio(models.Model):
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=32)
    alias = models.CharField(max_length=16, null=True, blank=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.PROTECT, null=True, blank=True)

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
    cargo = models.CharField(max_length=64)

    def __str__(self):
        return self.nombre + " " + self.apellido


class Impresora(models.Model):
    estados_choises = (
        (0, 'En Stock'),
        (1, 'Operativa'),
        (2, 'Averiada'),
    )

    id = models.AutoField(primary_key=True)
    modelo = models.ForeignKey(ModeloImpresora, on_delete=models.PROTECT)
    serial = models.CharField(max_length=16)
    estado = models.IntegerField(choices=estados_choises, default=0)
    ultima_asignacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        asignacion = Asignacion.objects.filter(impresora=self.id)
        if asignacion:
            return asignacion[0].__str__()
        else:
            return self.modelo.__str__() + " S/N:" + self.serial + ' No Asignada'


class Asignacion(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    impresora = models.OneToOneField(Impresora, on_delete=models.PROTECT, null=False)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, null=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = "asignaciones"

    def __str__(self):
        if self.usuario:
            asigned = self.usuario.__str__()
        elif self.departamento:
            asigned = self.departamento.__str__()
        else:
            return "No asignacion de " + self.impresora.modelo.__str__() + "S/N: " + self.impresora.serial + " Ubicada en " + self.ubicacion.__str__()
        return "Asignacion de " + self.impresora.modelo.__str__() + "S/N: " + self.impresora.serial + " a " + asigned

