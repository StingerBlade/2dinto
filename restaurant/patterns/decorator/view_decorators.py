# restaurant/patterns/decorator/view_decorators.py

"""
PATRÓN DECORATOR - Decoradores para Vistas Django

Este módulo implementa el patrón Decorator para añadir funcionalidades
adicionales a las vistas de Django sin modificar su código original.

Decoradores implementados:
- log_view_access: Registra cada acceso a una vista
- require_role: Valida que el usuario tenga un rol específico
- measure_performance: Mide el tiempo de ejecución de una vista
- validate_restaurant_open: Valida que el restaurante esté abierto

Propósito:
- Añadir funcionalidades dinámicamente
- Cumplir con el principio Open/Closed
- Reutilizar lógica común entre vistas
- Separar concerns (logging, permisos, validación)

Uso:
    from restaurant.patterns.decorator.view_decorators import log_view_access, require_role
    
    @log_view_access
    @require_role('mesero')
    def mi_vista(request):
        ...
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import logging
import time
from datetime import datetime

# Configurar logger
logger = logging.getLogger('restaurant')


def log_view_access(view_func):
    """
    Decorador que registra cada acceso a una vista en el log del sistema.
    
    Registra:
    - Usuario que accedió
    - Vista accedida
    - Timestamp
    - Método HTTP (GET, POST, etc.)
    - IP del cliente
    
    Ejemplo:
        @log_view_access
        def lista_platillos(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Obtener información del request
        user = request.user.username if request.user.is_authenticated else 'Anónimo'
        view_name = view_func.__name__
        method = request.method
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Registrar en el log
        log_message = (
            f"[{timestamp}] 👤 Usuario: {user} | "
            f"🎯 Vista: {view_name} | "
            f"📡 Método: {method} | "
            f"🌐 IP: {ip}"
        )
        logger.info(log_message)
        
        # También imprimir en consola para desarrollo
        print(f"\n📝 [DECORATOR LOG] {log_message}\n")
        
        # Ejecutar la vista original
        return view_func(request, *args, **kwargs)
    
    return wrapper


def require_role(*roles):
    """
    Decorador que valida que el usuario tenga uno de los roles especificados.
    
    Los roles se definen mediante grupos de Django:
    - 'admin': Administrador del sistema
    - 'mesero': Meseros que toman pedidos
    - 'cocina': Personal de cocina
    - 'caja': Personal de caja/pagos
    
    Args:
        *roles: Uno o más roles permitidos
    
    Ejemplo:
        @require_role('mesero', 'admin')
        def crear_pedido(request):
            ...
    
    Si el usuario no tiene el rol, se le redirige con un mensaje de error.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario tiene alguno de los roles permitidos
            user_groups = request.user.groups.values_list('name', flat=True)
            
            has_permission = any(role in user_groups for role in roles)
            
            if not has_permission:
                # Log del intento de acceso no autorizado
                logger.warning(
                    f"⚠️ Acceso denegado: {request.user.username} "
                    f"intentó acceder a {view_func.__name__} "
                    f"sin los roles requeridos: {', '.join(roles)}"
                )
                
                messages.error(
                    request,
                    f'❌ No tienes permisos para acceder a esta sección. '
                    f'Roles requeridos: {", ".join(roles)}'
                )
                return redirect('restaurant:dashboard')
            
            # Log de acceso autorizado
            logger.info(
                f"✅ Acceso autorizado: {request.user.username} "
                f"accedió a {view_func.__name__} con rol válido"
            )
            
            # Ejecutar la vista original
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def measure_performance(view_func):
    """
    Decorador que mide el tiempo de ejecución de una vista.
    
    Útil para:
    - Identificar vistas lentas
    - Optimización de rendimiento
    - Monitoreo del sistema
    
    Registra el tiempo en el log y lo imprime en consola.
    
    Ejemplo:
        @measure_performance
        def vista_compleja(request):
            # código que puede ser lento
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Registrar tiempo de inicio
        start_time = time.time()
        
        # Ejecutar la vista
        response = view_func(request, *args, **kwargs)
        
        # Calcular tiempo transcurrido
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Registrar en el log
        log_message = (
            f"⏱️ Vista: {view_func.__name__} | "
            f"Tiempo: {execution_time:.4f}s"
        )
        
        # Usar diferentes niveles según el tiempo
        if execution_time > 2.0:
            logger.warning(f"🐌 LENTO! {log_message}")
            print(f"\n🐌 [DECORATOR PERFORMANCE] LENTO! {log_message}\n")
        elif execution_time > 1.0:
            logger.info(f"⚡ {log_message}")
            print(f"\n⚡ [DECORATOR PERFORMANCE] {log_message}\n")
        else:
            logger.info(f"🚀 RÁPIDO! {log_message}")
            print(f"\n🚀 [DECORATOR PERFORMANCE] {log_message}\n")
        
        return response
    
    return wrapper


def validate_restaurant_open(view_func):
    """
    Decorador que valida si el restaurante está en horario de operación.
    
    Verifica la hora actual contra el horario configurado en el Singleton.
    Si está fuera de horario, redirige con un mensaje.
    
    Nota: Esta es una validación simplificada. En producción, se debería
    parsear el horario correctamente.
    
    Ejemplo:
        @validate_restaurant_open
        def crear_pedido(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from restaurant.patterns.singleton.config_manager import RestaurantConfig
        
        # Obtener configuración
        config = RestaurantConfig()
        
        # Por ahora, siempre permitimos (para desarrollo)
        # En producción, aquí iría la lógica de validación de horario
        
        # Ejemplo de cómo se podría implementar:
        # hora_actual = datetime.now().time()
        # if not esta_dentro_del_horario(hora_actual, config.get_horario()):
        #     messages.warning(request, f'⏰ El restaurante está cerrado. Horario: {config.get_horario()}')
        #     return redirect('restaurant:dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def ajax_required(view_func):
    """
    Decorador que valida que la petición sea AJAX/asíncrona.
    
    Útil para proteger endpoints que solo deben ser llamados vía AJAX.
    
    Ejemplo:
        @ajax_required
        def actualizar_estado_pedido(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            logger.warning(f"⚠️ Intento de acceso no-AJAX a {view_func.__name__}")
            return HttpResponseForbidden('Esta acción solo está permitida vía AJAX')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def log_post_data(view_func):
    """
    Decorador que registra los datos POST enviados a una vista.
    
    Útil para auditoría y debugging.
    PRECAUCIÓN: No usar en vistas que manejen datos sensibles (contraseñas, etc.)
    
    Ejemplo:
        @log_post_data
        def procesar_formulario(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            # Excluir campos sensibles
            sensitive_fields = ['password', 'csrfmiddlewaretoken']
            post_data = {
                key: value for key, value in request.POST.items()
                if key not in sensitive_fields
            }
            
            logger.info(
                f"📤 POST a {view_func.__name__} | "
                f"Usuario: {request.user.username} | "
                f"Datos: {post_data}"
            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper