from decimal import Decimal
from django.utils import timezone
from django.db import models

class Cliente(models.Model):
    cedula_cli = models.CharField(max_length=12, unique=True ,default='')
    nombre_cli = models.CharField(max_length=25, default='')
    apellido_cli = models.CharField(max_length=25, default='') 
    telefono_cli = models.CharField(max_length=15, default='')
    direccion_cli = models.CharField(max_length=50, default='')
    cod_ciudad = models.CharField(max_length=10, default='')
    activo = models.BooleanField(default=True) 
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

class Cliente_admin(models.Model):
    cedula_cli = models.CharField(max_length=12, unique=True ,default='')
    contraseña = models.CharField(max_length=25, default='')

class Ciudad(models.Model):
    cod_ciudad = models.CharField(max_length=10, unique=True, default='')
    nombre_ciudad = models.CharField(max_length=25, default='')

class Movimiento(models.Model):
    cedula_cli = models.CharField(max_length=12, default='')
    codigo_cta = models.CharField(max_length=10, default='')
    fecha_mov = models.DateTimeField(default=timezone.now)
    tipo_mov = models.CharField(max_length=1, default='') 
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


class Cuenta(models.Model):
    codigo_cta = models.CharField(max_length=10, unique=True, default='')
    nombre_cta = models.CharField(max_length=25, default='')
    fecha_creacion_cta = models.DateTimeField(default=timezone.now)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cedula = models.CharField(max_length=12 ,default='')
    chequera= models.IntegerField(default=0)

class adm_cuenta(models.Model):
    codigo_adm = models.CharField(max_length=10, unique=True, default='')
    cedula_cli = models.CharField(max_length=12, default='')
    fecha_creacion_cta = models.DateTimeField(default=timezone.now)