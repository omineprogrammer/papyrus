# Generated by Django 2.0.7 on 2018-10-21 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impresora',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]