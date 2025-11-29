# restaurant/patterns/observer/observers.py

"""
PATRÓN OBSERVER - Sistema de Notificaciones

Este módulo implementa el patrón Observer para notificar automáticamente
a diferentes partes del sistema cuando ocurren eventos importantes.

Componentes:
- Observer (Interface): Define el contrato para todos los observadores
- PedidoSubject: Sujeto que notifica cambios en pedidos
- CocinaObserver: Observador que recibe notificaciones para cocina
- MeseroObserver: Observador que recibe notificaciones para meseros
- AdministradorObserver: Observador que recibe todas las notificaciones

Propósito:
- Desacoplamiento entre pedidos y notificaciones
- Múltiples observadores pueden suscribirse a un pedido
- Notificaciones automáticas cuando cambia el estado
- Fácil añadir nuevos tipos de notificaciones

Uso:
    from restaurant.patterns.observer.observers import PedidoSubject, CocinaObserver
    
    # Crear sujeto (pedido)
    pedido_subject = PedidoSubject(pedido)
    
    # Agregar observadores
    pedido_subject.agregar_observador(CocinaObserver())
    
    # Notificar cambio
    pedido_subject.cambiar_estado('en_preparacion')
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger('restaurant')


# ==================== INTERFACE OBSERVER ====================

class Observer(ABC):
    """
    Interface base para todos los observadores.
    
    Todos los observadores deben implementar el método actualizar()
    que será llamado cuando el sujeto notifique un cambio.
    """
    
    @abstractmethod
    def actualizar(self, pedido, evento, datos=None):
        """
        Método que será llamado cuando ocurra un evento en el pedido.
        
        Args:
            pedido: Instancia del modelo Pedido
            evento (str): Tipo de evento ('cambio_estado', 'nuevo_item', etc.)
            datos (dict): Datos adicionales sobre el evento
        """
        pass


# ==================== SUJETO (SUBJECT) ====================

class PedidoSubject:
    """
    Sujeto que mantiene una lista de observadores y los notifica
    cuando ocurren cambios en un pedido.
    
    Este es el componente central del patrón Observer.
    """
    
    def __init__(self, pedido):
        """
        Inicializa el sujeto con un pedido específico.
        
        Args:
            pedido: Instancia del modelo Pedido
        """
        self.pedido = pedido
        self._observadores = []
        
        logger.info(f"📋 [OBSERVER] PedidoSubject creado para Pedido #{pedido.id}")
    
    def agregar_observador(self, observador):
        """
        Suscribe un observador para recibir notificaciones.
        
        Args:
            observador (Observer): Observador a agregar
        """
        if observador not in self._observadores:
            self._observadores.append(observador)
            logger.info(
                f"👤 [OBSERVER] Observador {observador.__class__.__name__} "
                f"agregado a Pedido #{self.pedido.id}"
            )
            print(
                f"\n➕ [OBSERVER] {observador.__class__.__name__} "
                f"suscrito al Pedido #{self.pedido.id}\n"
            )
    
    def quitar_observador(self, observador):
        """
        Desuscribe un observador.
        
        Args:
            observador (Observer): Observador a remover
        """
        if observador in self._observadores:
            self._observadores.remove(observador)
            logger.info(
                f"👋 [OBSERVER] Observador {observador.__class__.__name__} "
                f"removido de Pedido #{self.pedido.id}"
            )
    
    def notificar_observadores(self, evento, datos=None):
        """
        Notifica a todos los observadores sobre un evento.
        
        Args:
            evento (str): Tipo de evento
            datos (dict): Datos adicionales del evento
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        logger.info(
            f"📣 [OBSERVER] Notificando a {len(self._observadores)} "
            f"observador(es) sobre '{evento}' en Pedido #{self.pedido.id}"
        )
        
        print(
            f"\n📣 [{timestamp}] NOTIFICACIÓN - Pedido #{self.pedido.id} - "
            f"Evento: {evento}"
        )
        print(f"   Notificando a {len(self._observadores)} observador(es)...\n")
        
        for observador in self._observadores:
            try:
                observador.actualizar(self.pedido, evento, datos)
            except Exception as e:
                logger.error(
                    f"❌ [OBSERVER] Error al notificar {observador.__class__.__name__}: {e}"
                )
    
    def cambiar_estado(self, nuevo_estado, usuario=None):
        """
        Cambia el estado del pedido y notifica a los observadores.
        
        Args:
            nuevo_estado (str): Nuevo estado del pedido
            usuario: Usuario que realizó el cambio (opcional)
        """
        estado_anterior = self.pedido.estado
        
        # Cambiar el estado en el modelo
        self.pedido.estado = nuevo_estado
        self.pedido.save()
        
        # Preparar datos del evento
        datos = {
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'usuario': usuario.username if usuario else 'Sistema',
            'timestamp': datetime.now()
        }
        
        logger.info(
            f"🔄 [OBSERVER] Pedido #{self.pedido.id}: "
            f"{estado_anterior} → {nuevo_estado}"
        )
        
        # Notificar a todos los observadores
        self.notificar_observadores('cambio_estado', datos)
    
    def agregar_item(self, item, usuario=None):
        """
        Notifica que se agregó un item al pedido.
        
        Args:
            item: ItemPedido agregado
            usuario: Usuario que agregó el item
        """
        datos = {
            'item': item,
            'platillo': item.platillo.nombre,
            'cantidad': item.cantidad,
            'usuario': usuario.username if usuario else 'Sistema',
            'timestamp': datetime.now()
        }
        
        logger.info(
            f"➕ [OBSERVER] Item agregado al Pedido #{self.pedido.id}: "
            f"{item.cantidad}x {item.platillo.nombre}"
        )
        
        self.notificar_observadores('nuevo_item', datos)
    
    def pedido_pagado(self, pago, usuario=None):
        """
        Notifica que el pedido fue pagado.
        
        Args:
            pago: Instancia de Pago
            usuario: Usuario que procesó el pago
        """
        datos = {
            'pago': pago,
            'monto': float(pago.monto),
            'metodo': pago.metodo_pago.nombre,
            'usuario': usuario.username if usuario else 'Sistema',
            'timestamp': datetime.now()
        }
        
        logger.info(
            f"💰 [OBSERVER] Pedido #{self.pedido.id} pagado: "
            f"${pago.monto} via {pago.metodo_pago.nombre}"
        )
        
        self.notificar_observadores('pedido_pagado', datos)


# ==================== OBSERVADORES CONCRETOS ====================

class CocinaObserver(Observer):
    """
    Observador para el área de cocina.
    
    Recibe notificaciones sobre:
    - Nuevos pedidos
    - Nuevos items agregados a pedidos existentes
    - Pedidos cancelados
    """
    
    def actualizar(self, pedido, evento, datos=None):
        """
        Implementación del método actualizar para cocina.
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if evento == 'cambio_estado' and datos['estado_nuevo'] == 'pendiente':
            # Nuevo pedido para cocina
            mensaje = (
                f"🍳 [COCINA] [{timestamp}] NUEVO PEDIDO - "
                f"Mesa {pedido.mesa.numero} - Pedido #{pedido.id}"
            )
            print(mensaje)
            self._mostrar_items_pedido(pedido)
            logger.info(mensaje)
            
        elif evento == 'nuevo_item':
            # Item agregado a pedido existente
            mensaje = (
                f"🍳 [COCINA] [{timestamp}] ITEM AGREGADO - "
                f"Mesa {pedido.mesa.numero} - Pedido #{pedido.id}\n"
                f"   → {datos['cantidad']}x {datos['platillo']}"
            )
            print(mensaje)
            logger.info(mensaje)
            
        elif evento == 'cambio_estado' and datos['estado_nuevo'] == 'cancelado':
            # Pedido cancelado
            mensaje = (
                f"🍳 [COCINA] [{timestamp}] ❌ PEDIDO CANCELADO - "
                f"Mesa {pedido.mesa.numero} - Pedido #{pedido.id}"
            )
            print(mensaje)
            logger.info(mensaje)
    
    def _mostrar_items_pedido(self, pedido):
        """
        Muestra todos los items de un pedido.
        """
        print(f"   Items:")
        for item in pedido.items.all():
            print(f"   - {item.cantidad}x {item.platillo.nombre}")
            if item.notas:
                print(f"     Notas: {item.notas}")


class MeseroObserver(Observer):
    """
    Observador para meseros.
    
    Recibe notificaciones sobre:
    - Pedidos listos para entregar
    - Pedidos pagados
    """
    
    def actualizar(self, pedido, evento, datos=None):
        """
        Implementación del método actualizar para meseros.
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if evento == 'cambio_estado' and datos['estado_nuevo'] == 'listo':
            # Pedido listo para entregar
            mensaje = (
                f"🧑‍🍳 [MESERO] [{timestamp}] ✅ PEDIDO LISTO - "
                f"Mesa {pedido.mesa.numero} - Pedido #{pedido.id}\n"
                f"   → Llevar a la mesa"
            )
            print(mensaje)
            logger.info(mensaje)
            
        elif evento == 'cambio_estado' and datos['estado_nuevo'] == 'entregado':
            # Pedido entregado
            mensaje = (
                f"🧑‍🍳 [MESERO] [{timestamp}] 📦 PEDIDO ENTREGADO - "
                f"Mesa {pedido.mesa.numero} - Pedido #{pedido.id}\n"
                f"   → Total: ${pedido.total}"
            )
            print(mensaje)
            logger.info(mensaje)
            
        elif evento == 'pedido_pagado':
            # Pedido pagado
            mensaje = (
                f"🧑‍🍳 [MESERO] [{timestamp}] 💰 PAGO RECIBIDO - "
                f"Mesa {pedido.mesa.numero} - Pedido #{pedido.id}\n"
                f"   → Monto: ${datos['monto']} via {datos['metodo']}"
            )
            print(mensaje)
            logger.info(mensaje)


class AdministradorObserver(Observer):
    """
    Observador para administradores.
    
    Recibe TODAS las notificaciones para monitoreo general.
    """
    
    def actualizar(self, pedido, evento, datos=None):
        """
        Implementación del método actualizar para administrador.
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if evento == 'cambio_estado':
            mensaje = (
                f"👔 [ADMIN] [{timestamp}] Pedido #{pedido.id} - "
                f"Estado: {datos['estado_anterior']} → {datos['estado_nuevo']} - "
                f"Mesa {pedido.mesa.numero}"
            )
            
        elif evento == 'nuevo_item':
            mensaje = (
                f"👔 [ADMIN] [{timestamp}] Pedido #{pedido.id} - "
                f"Nuevo item: {datos['cantidad']}x {datos['platillo']} - "
                f"Mesa {pedido.mesa.numero}"
            )
            
        elif evento == 'pedido_pagado':
            mensaje = (
                f"👔 [ADMIN] [{timestamp}] Pedido #{pedido.id} - "
                f"Pago: ${datos['monto']} via {datos['metodo']} - "
                f"Mesa {pedido.mesa.numero}"
            )
        
        else:
            mensaje = (
                f"👔 [ADMIN] [{timestamp}] Pedido #{pedido.id} - "
                f"Evento: {evento} - Mesa {pedido.mesa.numero}"
            )
        
        # Mostrar y registrar mensaje
        print(mensaje)
        logger.info(mensaje)


class NotificacionEmailObserver(Observer):
    """
    Observador que envía notificaciones por email.
    
    En un sistema real, aquí se implementaría el envío de emails.
    Por ahora, solo simula el envío.
    """
    
    def __init__(self, email_destino):
        """
        Inicializa el observador con un email destino.
        
        Args:
            email_destino (str): Email donde enviar notificaciones
        """
        self.email_destino = email_destino
    
    def actualizar(self, pedido, evento, datos=None):
        """
        Simula envío de email para eventos importantes.
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Solo enviar emails para eventos importantes
        eventos_importantes = ['pedido_pagado', 'cancelado']
        
        if evento == 'cambio_estado' and datos['estado_nuevo'] in eventos_importantes:
            asunto = f"Pedido #{pedido.id} - {datos['estado_nuevo']}"
            cuerpo = (
                f"Mesa: {pedido.mesa.numero}\n"
                f"Total: ${pedido.total}\n"
                f"Estado: {datos['estado_nuevo']}"
            )
            
            mensaje = (
                f"📧 [EMAIL] [{timestamp}] Enviando email a {self.email_destino}\n"
                f"   Asunto: {asunto}\n"
                f"   Cuerpo: {cuerpo}"
            )
            
            print(mensaje)
            logger.info(mensaje)