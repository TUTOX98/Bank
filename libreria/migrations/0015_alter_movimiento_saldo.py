# Generated by Django 3.2.8 on 2024-02-21 22:50

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0014_remove_cliente_saldo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=9),
        ),
    ]
