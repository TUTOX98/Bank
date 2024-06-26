# Generated by Django 3.2.8 on 2024-02-21 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0011_adm_cuenta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=15),
        ),
    ]
