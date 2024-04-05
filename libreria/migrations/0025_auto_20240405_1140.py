# Generated by Django 3.2.8 on 2024-04-05 16:40

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0024_auto_20240405_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
    ]
