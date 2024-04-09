from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.landing_view, name='landing_page'), 
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),#check
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),#check
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),#check
    path('lista_cuentas/', views.lista_cuentas, name='lista_cuentas'),#check
    path('activar_desactivar_cliente/<int:cliente_id>/', views.activar_desactivar_cliente, name='activar_desactivar_cliente'),
    path('ingresar_dinero/', views.ingresar_dinero, name='ingresar_dinero'),
    path('ingresar_dinero_cliente/', views.ingresar_dinero_cliente, name='ingresar_dinero_cliente'),
    path('Movimiento/', views.lista_movimientos, name='Movimiento'),
    path('retirar_dinero/', views.retirar_dinero, name='retirar_dinero'),
    path('cliente/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('cuenta/eliminar/<int:cuenta_id>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('retirar_dinero_cliente/', views.retirar_dinero_cliente, name='retirar_dinero_cliente'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)