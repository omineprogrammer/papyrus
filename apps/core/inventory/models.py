from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    class Meta:
        verbose_name = "Fabricante"
        verbose_name_plural = "Fabricantes"

class TypeItem(models.Model):
    initials = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Tipo de item"
        verbose_name_plural = "Tipos de item"