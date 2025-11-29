# restaurant/admin.py

"""
Configuración del Admin de Django para el sistema de restaurante
"""

from django.contrib import admin
from .models import (
    Categoria, Platillo, Mesa, Pedido, ItemPedido,
    MetodoPago, Pago, Factura
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin para Categorías"""
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']


@admin.register(Platillo)
class PlatilloAdmin(admin.ModelAdmin):
    """Admin para Platillos"""
    list_display = ['nombre', 'categoria', 'precio', 'disponible', 'tiempo_preparacion']
    list_filter = ['categoria', 'disponible']
    search_fields = ['nombre', 'descripcion']
    ordering = ['categoria', 'nombre']
    list_editable = ['precio', 'disponible']


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    """Admin para Mesas"""
    list_display = ['numero', 'capacidad', 'ubicacion', 'activa']
    list_filter = ['activa', 'ubicacion']
    search_fields = ['numero', 'ubicacion']
    ordering = ['numero']
    list_editable = ['activa']


class ItemPedidoInline(admin.TabularInline):
    """Inline para mostrar items del pedido"""
    model = ItemPedido
    extra = 0
    readonly_fields = ['precio_unitario', 'subtotal']


class PagoInline(admin.TabularInline):
    """Inline para mostrar pagos del pedido"""
    model = Pago
    extra = 0
    readonly_fields = ['fecha_pago']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Admin para Pedidos"""
    list_display = ['id', 'mesa', 'mesero', 'estado', 'total', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['id', 'mesa__numero']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'subtotal', 'impuesto', 'total']
    inlines = [ItemPedidoInline, PagoInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('mesa', 'mesero', 'estado')
        }),
        ('Detalles', {
            'fields': ('notas_especiales',)
        }),
        ('Montos', {
            'fields': ('subtotal', 'impuesto', 'total')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion')
        }),
    )


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    """Admin para Items de Pedido"""
    list_display = ['pedido', 'platillo', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['pedido__fecha_creacion']
    search_fields = ['pedido__id', 'platillo__nombre']
    readonly_fields = ['precio_unitario', 'subtotal']


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    """Admin para Métodos de Pago"""
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    list_editable = ['activo']


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    """Admin para Pagos"""
    list_display = ['pedido', 'metodo_pago', 'monto', 'fecha_pago']
    list_filter = ['metodo_pago', 'fecha_pago']
    search_fields = ['pedido__id', 'referencia']
    readonly_fields = ['fecha_pago']
    ordering = ['-fecha_pago']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    """Admin para Facturas"""
    list_display = ['folio', 'pedido', 'nombre_cliente', 'rfc_cliente', 'fecha_emision']
    list_filter = ['fecha_emision']
    search_fields = ['folio', 'rfc_cliente', 'nombre_cliente']
    readonly_fields = ['fecha_emision']
    ordering = ['-fecha_emision']