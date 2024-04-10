from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
import re
import random
from .models import Cliente, Cliente_admin, Cuenta, Movimiento
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction
from .forms import ClienteForm
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST

def crear_cliente(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        cod_ciudad = request.POST.get('cod_ciudad')

        Cliente.objects.create(
            cedula_cli=cedula,
            nombre_cli=nombre,
            apellido_cli=apellido,
            telefono_cli=telefono,
            direccion_cli=direccion,
            cod_ciudad=cod_ciudad
        )
        return redirect('lista_clientes')
    return render(request, 'crear_cliente.html')

@require_POST
def eliminar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')

@require_POST
def eliminar_cuenta(request, cuenta_id):
    cuenta = Cuenta.objects.get(id=cuenta_id)
    cuenta.delete()
    return redirect('lista_cuentas')

def crear_cuenta(request):
    Clientes = Cliente.objects.all()
    
    if request.method == 'POST':
        chequera_num = 0
        nombre_cta = request.POST.get('tipo_cta')
        cedula_cli = request.POST.get('cedula_cli') 
        fecha_creacion = timezone.now()
        if Cuenta.objects.filter(nombre_cta=nombre_cta, cedula=cedula_cli).exists():
            messages.error(request, 'Ya existe una cuenta con ese nombre y cédula asociada.')
            return redirect('crear_cuenta')
        if nombre_cta == 'Corriente':
            chequera_num = 20
        uid = random.randint(100000, 999999)
        while Cuenta.objects.filter(codigo_cta=uid).exists():
            uid = random.randint(100000, 999999)
        Cuenta.objects.create(
            codigo_cta=uid,
            nombre_cta=nombre_cta,
            fecha_creacion_cta=fecha_creacion,
            saldo=0.00,
            cedula=cedula_cli,  
            chequera=chequera_num
        )
        return redirect('lista_cuentas')
    
    return render(request, 'crear_cuenta.html', {'clientes': Clientes})

def lista_cuentas(request):
    cuentas_list = Cuenta.objects.all()
    clientes = Cliente.objects.all().values('cedula_cli', 'nombre_cli')  
    clientes_dict = {cliente['cedula_cli']: cliente['nombre_cli'] for cliente in clientes}  
    
    paginator = Paginator(cuentas_list, 3) 
    page_number = request.GET.get('page')
    cuentas_page = paginator.get_page(page_number)
    for cuenta in cuentas_page:
        cuenta.nombre_cliente = clientes_dict.get(cuenta.cedula, 'Cliente no encontrado')  
    
    return render(request, 'lista_cuentas.html', {'cuentas': cuentas_page})

def lista_clientes(request):
    cedula = request.GET.get('cedula')
    lista_clientes = Cliente.objects.all()

    if cedula:
        lista_clientes = lista_clientes.filter(cedula_cli__icontains=cedula)

    paginator = Paginator(lista_clientes, 3)
    page_number = request.GET.get('page')
    clientes_page = paginator.get_page(page_number)
    return render(request, 'lista_clientes.html', {'clientes_page': clientes_page})

def activar_cuenta(request, cuenta_id):
    cuenta = Cuenta.objects.get(pk=cuenta_id)
    cuenta.activo = True
    cuenta.save()
    return redirect('lista_cuentas')

def desactivar_cuenta(request, cuenta_id):
    cuenta = Cuenta.objects.get(pk=cuenta_id)
    cuenta.activo = False
    cuenta.save()
    return redirect('lista_cuentas')

def ingresar_dinero_cliente(request):
    cedula_imp = request.session.get('cedula', None)
    cliente = Cliente.objects.get(cedula_cli=cedula_imp)
    if request.method == 'POST':
        cedula = cedula_imp
        cuenta_id = request.POST.get('cuenta_id')
        monto = request.POST.get('monto')
        try:
            cliente = Cliente.objects.get(cedula_cli=cedula)
        except Cliente.DoesNotExist:
            messages.error(request, 'El cliente con esa cédula no está registrado.')
            return redirect('ingresar_dinero_cliente')
        if not cliente.activo:
            messages.error(request, 'La cuenta del cliente no está activa.')
            return redirect('ingresar_dinero_cliente')
        else:
            try:
                cuenta = Cuenta.objects.get(pk=cuenta_id)
            except Cuenta.DoesNotExist:
                messages.error(request, 'La cuenta seleccionada no existe.')
                return redirect('ingresar_dinero_cliente')
            
            try:
                with transaction.atomic():
                    monto_decimal = Decimal(monto)
                    cuenta.saldo += monto_decimal
                    cuenta.save()
                    movimiento = Movimiento(
                        cedula_cli=cedula,
                        codigo_cta=cuenta.codigo_cta,
                        fecha_mov=timezone.now(),
                        tipo_mov='I',
                        saldo=monto_decimal
                    )
                    movimiento.save()
                    messages.success(request, 'El dinero ha sido ingresado satisfactoriamente.')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al intentar registrar el movimiento: ' + str(e))
                return redirect('ingresar_dinero_cliente')
        return redirect('ingresar_dinero_cliente')

    cuentas = Cuenta.objects.filter(cedula=cedula_imp) if cedula_imp else Cuenta.objects.none()
    return render(request, 'ingresar_dineroCliente.html', {'cliente': cliente, 'cuentas': cuentas})


def ingresar_dinero(request):
    if request.method == 'POST':
        cuenta_id = request.POST.get('cuenta_id')
        monto = request.POST.get('monto')
        try:
            cuenta = Cuenta.objects.get(pk=cuenta_id)
            try:
                cliente = Cliente.objects.get(cedula_cli=cuenta.cedula)
            except Cliente.DoesNotExist:
                messages.error(request, 'El cliente con esa cédula no está registrado.' + cuenta.cedula)
                return redirect('retirar_dinero_cliente')
            if not cliente.activo:
                messages.error(request, 'La cuenta del cliente no está activa.' + cuenta.cedula)
                return redirect('retirar_dinero_cliente')
        except Cuenta.DoesNotExist:
            messages.error(request, 'La cuenta seleccionada no existe.')
            return redirect('lista_cuentas')
        try:
            cuenta = Cuenta.objects.get(pk=cuenta_id)
        except Cuenta.DoesNotExist:
            messages.error(request, 'La cuenta seleccionada no existe.')
            return redirect('ingresar_dinero')
        with transaction.atomic():
            monto_decimal = Decimal(monto)
            cuenta.saldo += monto_decimal
            cuenta.save()
            messages.success(request, 'El dinero ha sido ingresado satisfactoriamente.')
        return redirect('lista_cuentas')
    clientes = Cliente.objects.all()
    cuentas = Cuenta.objects.all()
    return render(request, 'ingresar_dinero.html', {'clientes': clientes, 'cuentas': cuentas})


def password_reset_request(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        user = Cliente_admin.objects.filter(cedula_cli=cedula).first()
        if user:
            # Genera tu token aquí
            reset_token = "tu_token_generado"
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[reset_token]))
            send_mail(
                'Restablecimiento de contraseña',
                f'Usa este enlace para restablecer tu contraseña: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Se ha enviado un enlace de restablecimiento a tu correo electrónico.')
            return redirect('login')
        else:
            messages.error(request, 'No se encontró una cuenta con esa cédula.')
    return render(request, 'password_reset_request.html')

def login_view(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        password = request.POST.get('password')
        cliente_admin = Cliente_admin.objects.filter(cedula_cli=cedula).first()
        user = authenticate(request, username=cedula, password=password)
        if cliente_admin and cliente_admin.contraseña == password:
            user, created = User.objects.get_or_create(username=cliente_admin.cedula_cli)
            if created:
                user.set_unusable_password()
                user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('lista_clientes')
        if user is not None:
            login(request, user)
            request.session['cedula'] = cedula
            return redirect('ingresar_dinero_cliente')
        else:
            messages.error(request, 'Credenciales inválidas.')
    return render(request, 'login.html')

def lista_movimientos(request):
    cedula_imp = request.session.get('cedula', None)
    cliente = Cliente.objects.get(cedula_cli=cedula_imp)
    cuentas = Cuenta.objects.filter(cedula=cedula_imp) if cedula_imp else Cuenta.objects.none()
    movimientos = Movimiento.objects.filter(cedula_cli=cedula_imp) if cedula_imp else Cuenta.objects.none()
    return render(request, 'movimientos.html', {'cliente': cliente, 'cuentas': cuentas, 'movimientos': movimientos})


def retirar_dinero(request):
    if request.method == 'POST':
        cuenta_id = request.POST.get('cuenta_id')
        monto = Decimal(request.POST.get('monto'))
        try:
            cuenta = Cuenta.objects.get(pk=cuenta_id)
            try:
                cliente = Cliente.objects.get(cedula_cli=cuenta.cedula)
            except Cliente.DoesNotExist:
                messages.error(request, 'El cliente con esa cédula no está registrado.' + cuenta.cedula)
                return redirect('retirar_dinero_cliente')
            if not cliente.activo:
                messages.error(request, 'La cuenta del cliente no está activa.' + cuenta.cedula)
                return redirect('retirar_dinero_cliente')
        except Cuenta.DoesNotExist:
            messages.error(request, 'La cuenta seleccionada no existe.')
            return redirect('lista_cuentas')
        try:
            with transaction.atomic():
                monto_decimal = Decimal(monto)
                reglaluk= cuenta.saldo-monto_decimal
                if cuenta.saldo < monto_decimal or reglaluk<=Decimal(15000):
                    messages.error(request, 'No se pudo realizar la operación.')
                    return redirect('lista_cuentas')
                else:
                    cuenta.saldo -= monto_decimal
                    cuenta.save()
                    messages.success(request, 'Retiro realizado con éxito.' )
        except Exception as e:
            messages.error(request, e + cuenta )
            return redirect('lista_cuentas')

    clientes = Cliente.objects.all()
    cuentas = Cuenta.objects.all()
    return render(request, 'retirar_dinero.html', {'clientes': clientes, 'cuentas': cuentas})

def retirar_dinero_cliente(request):
    cedula_imp = request.session.get('cedula', None)
    cliente = Cliente.objects.get(cedula_cli=cedula_imp)
    if request.method == 'POST':
        cedula = cedula_imp
        cuenta_id = request.POST.get('cuenta_id')
        monto = request.POST.get('monto')
        try:
            cliente = Cliente.objects.get(cedula_cli=cedula)
            cuenta = Cuenta.objects.get(pk=cuenta_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'El cliente con esa cédula no está registrado.')
            return redirect('retirar_dinero_cliente')

        if not cliente.activo:
            messages.error(request, 'La cuenta del cliente no está activa.')
            return redirect('retirar_dinero_cliente')

        try:
            with transaction.atomic():
                monto_decimal = Decimal(monto)
                reglaluk = cuenta.saldo - monto_decimal
                if cuenta.nombre_cta == 'Corriente':
                    if cuenta.chequera < 1:
                        messages.error(request, 'No se pudo realizar la operación, cantidad de cheques insuficiente.')
                        return redirect('retirar_dinero_cliente')
                if cuenta.nombre_cta == 'Ahorro':
                    if cuenta.saldo < monto_decimal or reglaluk <= Decimal(15000):
                        messages.error(request, 'No se pudo realizar la operación.')
                        return redirect('retirar_dinero_cliente')
                cuenta.saldo -= monto_decimal
                if cuenta.nombre_cta == 'Corriente':
                    cuenta.chequera -= 1
                cuenta.save()
                movimiento = Movimiento(
                    cedula_cli=cedula,
                    codigo_cta=cuenta.codigo_cta,
                    fecha_mov=timezone.now(),
                    tipo_mov='R',
                    saldo=monto_decimal
                )
                movimiento.save()
                messages.success(request, 'Retiro realizado con éxito.')
        except Exception as e:
            messages.error(request, str(e)) 
            return redirect('retirar_dinero_cliente')

    cuentas = Cuenta.objects.filter(cedula=cedula_imp) if cedula_imp else Cuenta.objects.none()
    return render(request, 'retirar_dineroCliente.html', {'cliente': cliente, 'cuentas': cuentas})

def registro_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula_cli']
            password = form.cleaned_data['password']
            if not re.match('^\d{6,10}$', cedula):
                form.add_error('cedula_cli', 'La cédula debe tener entre 6 y 10 números.')
                return render(request, 'registro.html', {'form': form})
            if (not re.search('[a-zA-Z]', password) or not re.search('[0-9]', password) 
                or not re.search('[^a-zA-Z0-9]', password)):
                form.add_error('password', 'La contraseña debe contener letras, números y caracteres especiales.')
                return render(request, 'registro.html', {'form': form})
            
            cliente = form.save(commit=False)
            user = User.objects.create_user(username=cliente.cedula_cli, password=password)
            user.save()
            cliente.save()
            login(request, user)
            return redirect('lista_clientes') 
    else:
        form = ClienteForm()
    return render(request, 'registro.html', {'form': form})

def activar_desactivar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.activo = not cliente.activo
    cliente.save()
    return redirect('lista_clientes')

def landing_view(request):
    return render(request, 'index.html')