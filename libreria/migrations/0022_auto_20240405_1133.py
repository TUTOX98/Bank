# Generated by Django 3.2.8 on 2024-04-05 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0021_auto_20240405_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='saldo',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='saldo',
        ),
    ]
