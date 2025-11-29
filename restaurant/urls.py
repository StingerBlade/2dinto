# restaurant/urls.py

"""
URLs de la aplicación Restaurant
"""

from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    # ==================== DASHBOARD ====================
    path('', views.dashboard, name='dashboard'),
    
    # ==================== CATEGORÍAS ====================
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    
    # ==================== PLATILLOS ====================
    path('platillos/', views.lista_platillos, name='lista_platillos'),
    path('platillos/crear/', views.crear_platillo, name='crear_platillo'),
    path('platillos/<int:pk>/editar/', views.editar_platillo, name='editar_platillo'),
    path('platillos/<int:pk>/eliminar/', views.eliminar_platillo, name='eliminar_platillo'),
    
    # ==================== MESAS ====================
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('mesas/crear/', views.crear_mesa, name='crear_mesa'),
    path('mesas/<int:pk>/editar/', views.editar_mesa, name='editar_mesa'),
    path('mesas/<int:pk>/eliminar/', views.eliminar_mesa, name='eliminar_mesa'),
    
    # ==================== PEDIDOS ====================
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/crear/<int:mesa_id>/', views.crear_pedido, name='crear_pedido_mesa'),
    path('pedidos/<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/<int:pk>/cambiar-estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pedidos/<int:pedido_id>/agregar-item/', views.agregar_item_pedido, name='agregar_item_pedido'),
    path('pedidos/<int:pedido_id>/pagar/', views.procesar_pago, name='procesar_pago'),
    
    # ==================== CONFIGURACIÓN ====================
    path('configuracion/', views.ver_configuracion, name='ver_configuracion'),
]