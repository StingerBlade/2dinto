# restaurant/views.py

"""
Vistas del Sistema de Gestión de Restaurante

Este módulo contiene todas las vistas de la aplicación, organizadas por funcionalidad.
Cada vista implementa los patrones de diseño donde corresponde.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import (
    Categoria, Platillo, Mesa, Pedido, ItemPedido,
    MetodoPago, Pago, Factura
)
from .forms import (
    PlatilloForm, CategoriaForm, MesaForm, PedidoForm,
    ItemPedidoForm, PagoForm
)
from .patterns.singleton.config_manager import RestaurantConfig
from .patterns.decorator.view_decorators import (
    log_view_access, require_role, measure_performance
)
from .patterns.observer.observers import (
    PedidoSubject, CocinaObserver, MeseroObserver, AdministradorObserver
)

import logging

logger = logging.getLogger('restaurant')


# ==================== VISTA PRINCIPAL ====================

@login_required
@log_view_access
@measure_performance
def dashboard(request):
    """
    Vista principal del dashboard.
    Muestra estadísticas generales del restaurante.
    """
    # Obtener configuración (Singleton)
    config = RestaurantConfig()
    
    # Estadísticas
    total_pedidos_hoy = Pedido.objects.filter(
        fecha_creacion__date=timezone.now().date()
    ).count()
    
    pedidos_activos = Pedido.objects.filter(
        estado__in=['pendiente', 'en_preparacion', 'listo']
    ).count()
    
    total_ventas_hoy = Pedido.objects.filter(
        fecha_creacion__date=timezone.now().date(),
        estado='entregado'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    mesas_ocupadas = Mesa.objects.filter(
        pedidos__estado__in=['pendiente', 'en_preparacion', 'listo']
    ).distinct().count()
    
    context = {
        'config': config,
        'total_pedidos_hoy': total_pedidos_hoy,
        'pedidos_activos': pedidos_activos,
        'total_ventas_hoy': total_ventas_hoy,
        'mesas_ocupadas': mesas_ocupadas,
        'usuario': request.user,
    }
    
    return render(request, 'restaurant/dashboard.html', context)


# ==================== VISTAS DE CATEGORÍAS ====================

@login_required
@log_view_access
@require_role('admin', 'mesero')
def lista_categorias(request):
    """Lista todas las categorías"""
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'restaurant/categorias/lista.html', context)


@login_required
@log_view_access
@require_role('admin')
def crear_categoria(request):
    """Crea una nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Categoría creada exitosamente')
            logger.info(f"Categoría creada: {form.instance.nombre}")
            return redirect('restaurant:lista_categorias')
    else:
        form = CategoriaForm()
    
    context = {'form': form, 'accion': 'Crear'}
    return render(request, 'restaurant/categorias/form.html', context)


@login_required
@log_view_access
@require_role('admin')
def editar_categoria(request, pk):
    """Edita una categoría existente"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Categoría actualizada exitosamente')
            logger.info(f"Categoría editada: {categoria.nombre}")
            return redirect('restaurant:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {'form': form, 'accion': 'Editar', 'categoria': categoria}
    return render(request, 'restaurant/categorias/form.html', context)


@login_required
@log_view_access
@require_role('admin')
def eliminar_categoria(request, pk):
    """Elimina una categoría"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'✅ Categoría "{nombre}" eliminada')
        logger.info(f"Categoría eliminada: {nombre}")
        return redirect('restaurant:lista_categorias')
    
    context = {'categoria': categoria}
    return render(request, 'restaurant/categorias/eliminar.html', context)


# ==================== VISTAS DE PLATILLOS ====================

@login_required
@log_view_access
@measure_performance
def lista_platillos(request):
    """Lista todos los platillos"""
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('q')
    
    platillos = Platillo.objects.all()
    
    if categoria_id:
        platillos = platillos.filter(categoria_id=categoria_id)
    
    if busqueda:
        platillos = platillos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda)
        )
    
    categorias = Categoria.objects.all()
    
    context = {
        'platillos': platillos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
        'busqueda': busqueda
    }
    return render(request, 'restaurant/platillos/lista.html', context)


@login_required
@log_view_access
@require_role('admin')
def crear_platillo(request):
    """Crea un nuevo platillo"""
    if request.method == 'POST':
        form = PlatilloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Platillo creado exitosamente')
            logger.info(f"Platillo creado: {form.instance.nombre}")
            return redirect('restaurant:lista_platillos')
    else:
        form = PlatilloForm()
    
    context = {'form': form, 'accion': 'Crear'}
    return render(request, 'restaurant/platillos/form.html', context)


@login_required
@log_view_access
@require_role('admin')
def editar_platillo(request, pk):
    """Edita un platillo existente"""
    platillo = get_object_or_404(Platillo, pk=pk)
    
    if request.method == 'POST':
        form = PlatilloForm(request.POST, request.FILES, instance=platillo)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Platillo actualizado exitosamente')
            logger.info(f"Platillo editado: {platillo.nombre}")
            return redirect('restaurant:lista_platillos')
    else:
        form = PlatilloForm(instance=platillo)
    
    context = {'form': form, 'accion': 'Editar', 'platillo': platillo}
    return render(request, 'restaurant/platillos/form.html', context)


@login_required
@log_view_access
@require_role('admin')
def eliminar_platillo(request, pk):
    """Elimina un platillo"""
    platillo = get_object_or_404(Platillo, pk=pk)
    
    if request.method == 'POST':
        nombre = platillo.nombre
        platillo.delete()
        messages.success(request, f'✅ Platillo "{nombre}" eliminado')
        logger.info(f"Platillo eliminado: {nombre}")
        return redirect('restaurant:lista_platillos')
    
    context = {'platillo': platillo}
    return render(request, 'restaurant/platillos/eliminar.html', context)


# ==================== VISTAS DE MESAS ====================

@login_required
@log_view_access
def lista_mesas(request):
    """Lista todas las mesas"""
    mesas = Mesa.objects.all()
    
    # Agregar información de pedidos activos
    for mesa in mesas:
        mesa.pedido_activo = mesa.pedidos.filter(
            estado__in=['pendiente', 'en_preparacion', 'listo']
        ).first()
    
    context = {'mesas': mesas}
    return render(request, 'restaurant/mesas/lista.html', context)


@login_required
@log_view_access
@require_role('admin')
def crear_mesa(request):
    """Crea una nueva mesa"""
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Mesa creada exitosamente')
            logger.info(f"Mesa creada: {form.instance.numero}")
            return redirect('restaurant:lista_mesas')
    else:
        form = MesaForm()
    
    context = {'form': form, 'accion': 'Crear'}
    return render(request, 'restaurant/mesas/form.html', context)


@login_required
@log_view_access
@require_role('admin')
def editar_mesa(request, pk):
    """Edita una mesa existente"""
    mesa = get_object_or_404(Mesa, pk=pk)
    
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Mesa actualizada exitosamente')
            logger.info(f"Mesa editada: {mesa.numero}")
            return redirect('restaurant:lista_mesas')
    else:
        form = MesaForm(instance=mesa)
    
    context = {'form': form, 'accion': 'Editar', 'mesa': mesa}
    return render(request, 'restaurant/mesas/form.html', context)


@login_required
@log_view_access
@require_role('admin')
def eliminar_mesa(request, pk):
    """Elimina una mesa"""
    mesa = get_object_or_404(Mesa, pk=pk)
    
    if request.method == 'POST':
        numero = mesa.numero
        mesa.delete()
        messages.success(request, f'✅ Mesa {numero} eliminada')
        logger.info(f"Mesa eliminada: {numero}")
        return redirect('restaurant:lista_mesas')
    
    context = {'mesa': mesa}
    return render(request, 'restaurant/mesas/eliminar.html', context)


# ==================== VISTAS DE PEDIDOS ====================

@login_required
@log_view_access
@measure_performance
def lista_pedidos(request):
    """Lista todos los pedidos"""
    estado = request.GET.get('estado')
    mesa_id = request.GET.get('mesa')
    
    pedidos = Pedido.objects.all().select_related('mesa', 'mesero')
    
    if estado:
        pedidos = pedidos.filter(estado=estado)
    
    if mesa_id:
        pedidos = pedidos.filter(mesa_id=mesa_id)
    
    mesas = Mesa.objects.all()
    
    context = {
        'pedidos': pedidos,
        'mesas': mesas,
        'estado_seleccionado': estado,
        'mesa_seleccionada': mesa_id,
        'estados': Pedido.ESTADOS
    }
    return render(request, 'restaurant/pedidos/lista.html', context)


@login_required
@log_view_access
@require_role('mesero', 'admin')
def crear_pedido(request, mesa_id=None):
    """Crea un nuevo pedido"""
    mesa = None
    if mesa_id:
        mesa = get_object_or_404(Mesa, pk=mesa_id)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.mesero = request.user
            pedido.save()
            
            # PATRÓN OBSERVER: Crear sujeto y agregar observadores
            pedido_subject = PedidoSubject(pedido)
            pedido_subject.agregar_observador(CocinaObserver())
            pedido_subject.agregar_observador(MeseroObserver())
            pedido_subject.agregar_observador(AdministradorObserver())
            
            # Notificar nuevo pedido
            pedido_subject.cambiar_estado('pendiente', request.user)
            
            messages.success(request, f'✅ Pedido #{pedido.id} creado exitosamente')
            logger.info(f"Pedido creado: #{pedido.id} - Mesa {pedido.mesa.numero}")
            
            return redirect('restaurant:detalle_pedido', pk=pedido.id)
    else:
        initial = {'mesa': mesa} if mesa else {}
        form = PedidoForm(initial=initial)
    
    context = {'form': form, 'accion': 'Crear', 'mesa': mesa}
    return render(request, 'restaurant/pedidos/form.html', context)


@login_required
@log_view_access
@measure_performance
def detalle_pedido(request, pk):
    """Muestra el detalle de un pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    # Obtener configuración del restaurante (Singleton)
    config = RestaurantConfig()
    
    # Calcular propina sugerida
    propina_sugerida = config.calcular_propina_sugerida(float(pedido.total))
    
    context = {
        'pedido': pedido,
        'config': config,
        'propina_sugerida': propina_sugerida
    }
    return render(request, 'restaurant/pedidos/detalle.html', context)


@login_required
@log_view_access
@require_role('mesero', 'admin', 'cocina')
def cambiar_estado_pedido(request, pk):
    """Cambia el estado de un pedido usando el patrón Observer"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in dict(Pedido.ESTADOS).keys():
            # PATRÓN OBSERVER: Notificar cambio de estado
            pedido_subject = PedidoSubject(pedido)
            pedido_subject.agregar_observador(CocinaObserver())
            pedido_subject.agregar_observador(MeseroObserver())
            pedido_subject.agregar_observador(AdministradorObserver())
            
            pedido_subject.cambiar_estado(nuevo_estado, request.user)
            
            messages.success(request, f'✅ Estado del pedido actualizado a: {dict(Pedido.ESTADOS)[nuevo_estado]}')
            logger.info(f"Estado de Pedido #{pedido.id} cambiado a: {nuevo_estado}")
        else:
            messages.error(request, '❌ Estado inválido')
    
    return redirect('restaurant:detalle_pedido', pk=pk)


@login_required
@log_view_access
@require_role('mesero', 'admin')
def agregar_item_pedido(request, pedido_id):
    """Agrega un item a un pedido existente"""
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            item.save()
            
            # Recalcular totales del pedido
            pedido.calcular_totales()
            
            # PATRÓN OBSERVER: Notificar nuevo item
            pedido_subject = PedidoSubject(pedido)
            pedido_subject.agregar_observador(CocinaObserver())
            pedido_subject.agregar_observador(AdministradorObserver())
            
            pedido_subject.agregar_item(item, request.user)
            
            messages.success(request, f'✅ Item agregado: {item.cantidad}x {item.platillo.nombre}')
            logger.info(f"Item agregado al Pedido #{pedido.id}: {item.platillo.nombre}")
            
            return redirect('restaurant:detalle_pedido', pk=pedido.id)
    else:
        form = ItemPedidoForm()
    
    context = {'form': form, 'pedido': pedido}
    return render(request, 'restaurant/pedidos/agregar_item.html', context)


@login_required
@log_view_access
@require_role('caja', 'admin', 'mesero')
def procesar_pago(request, pedido_id):
    """Procesa el pago de un pedido"""
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    config = RestaurantConfig()
    propina_sugerida = config.calcular_propina_sugerida(float(pedido.total))
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.pedido = pedido
            pago.save()
            
            # PATRÓN OBSERVER: Notificar pago
            pedido_subject = PedidoSubject(pedido)
            pedido_subject.agregar_observador(MeseroObserver())
            pedido_subject.agregar_observador(AdministradorObserver())
            
            pedido_subject.pedido_pagado(pago, request.user)
            
            messages.success(request, f'✅ Pago procesado: ${pago.monto}')
            logger.info(f"Pago procesado para Pedido #{pedido.id}: ${pago.monto}")
            
            return redirect('restaurant:detalle_pedido', pk=pedido.id)
    else:
        form = PagoForm(initial={'monto': pedido.total})
    
    context = {
        'form': form, 
        'pedido': pedido,
        'config': config,
        'propina_sugerida': propina_sugerida
    }
    return render(request, 'restaurant/pedidos/procesar_pago.html', context)


# ==================== VISTA DE CONFIGURACIÓN (SINGLETON) ====================

@login_required
@log_view_access
@require_role('admin')
def ver_configuracion(request):
    """Muestra la configuración del restaurante (Patrón Singleton)"""
    config = RestaurantConfig()
    
    if request.method == 'POST':
        # Actualizar configuración
        nombre = request.POST.get('nombre_restaurante')
        impuesto = float(request.POST.get('impuesto'))
        propina = float(request.POST.get('propina_sugerida'))
        horario = request.POST.get('horario')
        capacidad = int(request.POST.get('capacidad_maxima'))
        
        config.set_nombre_restaurante(nombre)
        config.set_impuesto(impuesto / 100)  # Convertir de % a decimal
        config.set_propina_sugerida(propina / 100)
        config.set_horario(horario)
        config.set_capacidad_maxima(capacidad)
        
        # Guardar en archivo
        config.save_to_file()
        
        messages.success(request, '✅ Configuración actualizada exitosamente')
        logger.info("Configuración del restaurante actualizada")
        
        return redirect('restaurant:ver_configuracion')
    
    context = {'config': config}
    return render(request, 'restaurant/configuracion.html', context)