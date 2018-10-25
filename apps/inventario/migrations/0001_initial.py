# Generated by Django 2.0.7 on 2018-10-16 05:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='FabricanteImpresora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Impresora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=16)),
                ('estado', models.IntegerField(choices=[(0, 'Disponible'), (1, 'Asignado'), (2, 'Averiado')], default=0)),
                ('ultima_asignacion', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModeloImpresora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=32)),
                ('conexion_local', models.BooleanField(default=True)),
                ('conexion_red_cableada', models.BooleanField(default=False)),
                ('conexion_red_inalambrica', models.BooleanField(default=False)),
                ('fabricante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.FabricanteImpresora')),
            ],
        ),
        migrations.CreateModel(
            name='TipoImpresion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
                ('alias', models.CharField(blank=True, max_length=16, null=True)),
                ('edificio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventario.Edificio')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
                ('apellido', models.CharField(max_length=32)),
                ('cargo', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='modeloimpresora',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.TipoImpresion'),
        ),
        migrations.AddField(
            model_name='impresora',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.ModeloImpresora'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Empresa'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.Departamento'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='impresora',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='inventario.Impresora'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='ubicacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='inventario.Ubicacion'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventario.Usuario'),
        ),
    ]
