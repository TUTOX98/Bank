# Generated by Django 3.2.8 on 2024-02-21 22:42

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0012_auto_20240221_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15),
        ),
    ]
