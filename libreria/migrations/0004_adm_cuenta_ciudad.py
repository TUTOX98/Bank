# Generated by Django 3.2.8 on 2024-02-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0003_auto_20240221_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='adm_cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_adm', models.CharField(max_length=10, unique=True)),
                ('cedula_cli', models.CharField(max_length=12)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_ciudad', models.CharField(max_length=10, unique=True)),
                ('nombre_ciudad', models.CharField(max_length=25)),
            ],
        ),
    ]
