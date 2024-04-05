# Generated by Django 3.2.8 on 2024-02-21 21:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0004_adm_cuenta_ciudad'),
    ]

    operations = [
        migrations.DeleteModel(
            name='adm_cuenta',
        ),
        migrations.RenameField(
            model_name='movimiento',
            old_name='fecha',
            new_name='fecha_mov',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='documento',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='cuenta',
            name='activa',
        ),
        migrations.RemoveField(
            model_name='cuenta',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='cuenta',
            name='saldo',
        ),
        migrations.RemoveField(
            model_name='cuenta',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='cuenta',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='monto',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='tipo_movimiento',
        ),
        migrations.AddField(
            model_name='cliente',
            name='apellido_cli',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cedula_cli',
            field=models.CharField(default='', max_length=12, unique=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cod_ciudad',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='cliente',
            name='direccion_cli',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='cliente',
            name='nombre_cli',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefono_cli',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='codigo_cta',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='fecha_creacion_cta',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='nombre_cta',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='cedula_cli',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='codigo_cta',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default='', max_digits=15),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='tipo_mov',
            field=models.CharField(default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='ciudad',
            name='cod_ciudad',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='ciudad',
            name='nombre_ciudad',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
