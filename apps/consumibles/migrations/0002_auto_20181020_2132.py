# Generated by Django 2.0.7 on 2018-10-21 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumibles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimiento',
            name='solicitud',
        ),
        migrations.AddField(
            model_name='movimiento',
            name='id_solicitud',
            field=models.IntegerField(choices=[(1, 'Ticket Sample')], default=1, verbose_name='id de ticket en freshservice'),
        ),
        migrations.DeleteModel(
            name='Solicitud',
        ),
    ]