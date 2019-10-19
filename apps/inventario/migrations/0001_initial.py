# Generated by Django 2.0.7 on 2019-03-05 20:19

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
            options={
                'verbose_name_plural': 'asignaciones',
            },
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
            options={
                'verbose_name_plural': 'fabricantes de impresora',
            },
        ),
        migrations.CreateModel(
            name='Impresora',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('serial', models.CharField(max_length=16, unique=True)),
                ('estado', models.IntegerField(choices=[(0, 'En Stock'), (1, 'Operativa'), (2, 'Averiada'), (3, 'En Reparacion'), (4, 'De Baja')], default=0)),
                ('ultima_asignacion', models.DateTimeField(blank=True, null=True)),
                ('empresa_propietario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Empresa', verbose_name='Propiedad de')),
            ],
        ),
        migrations.CreateModel(
            name='ModeloImpresora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=32)),
                ('funcionalidad', models.BooleanField(default=True, verbose_name='es multi-funcional')),
                ('conexion_local', models.BooleanField(default=True, verbose_name='tiene conexion USB')),
                ('conexion_red_cableada', models.BooleanField(default=False, verbose_name='tiene conexion LAN')),
                ('conexion_red_inalambrica', models.BooleanField(default=False, verbose_name='tiene conexion WiFi')),
                ('fabricante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.FabricanteImpresora')),
            ],
            options={
                'verbose_name_plural': 'modelos de impresora',
            },
        ),
        migrations.CreateModel(
            name='TipoImpresion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': 'tipo de impresiones',
            },
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('alias', models.CharField(blank=True, max_length=64, null=True)),
                ('edificio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Edificio')),
            ],
            options={
                'verbose_name_plural': 'ubicaciones',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
                ('apellido', models.CharField(max_length=32)),
                ('cargo', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='modeloimpresora',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.TipoImpresion', verbose_name='tipo impresion'),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Departamento'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='impresora',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='inventario.Impresora'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Ubicacion'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.Usuario'),
        ),
    ]
