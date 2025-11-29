# restaurant/patterns/singleton/config_manager.py

"""
PATRÓN SINGLETON - Gestor de Configuración del Restaurante

Este módulo implementa el patrón Singleton para gestionar la configuración
global del restaurante. Garantiza que solo exista UNA instancia de configuración
en toda la aplicación.

Propósito:
- Configuración centralizada y única
- Acceso global a parámetros del restaurante
- Evitar inconsistencias en la configuración

Uso:
    from restaurant.patterns.singleton.config_manager import RestaurantConfig
    
    config = RestaurantConfig()
    impuesto = config.get_impuesto()
"""

import json
import os
from django.conf import settings


class RestaurantConfig:
    """
    Implementación del patrón Singleton para gestión de configuración.
    
    Esta clase garantiza que solo exista una instancia de configuración
    en toda la aplicación Django.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """
        Método especial que controla la creación de instancias.
        Solo permite crear UNA instancia de la clase.
        
        Returns:
            RestaurantConfig: La única instancia de la clase
        """
        if cls._instance is None:
            print("🔧 [SINGLETON] Creando NUEVA instancia de RestaurantConfig...")
            cls._instance = super(RestaurantConfig, cls).__new__(cls)
        else:
            print("♻️ [SINGLETON] Reutilizando instancia existente de RestaurantConfig")
        return cls._instance
    
    def __init__(self):
        """
        Inicializa la configuración solo la primera vez.
        Las siguientes veces que se intente crear una instancia,
        este método no reinicializará los valores.
        """
        if not RestaurantConfig._initialized:
            print("✅ [SINGLETON] Inicializando configuración del restaurante...")
            
            # Configuración por defecto
            self._config = {
                'nombre_restaurante': 'Restaurante Code & Taste',
                'direccion': 'Av. Universidad #123, Chihuahua, Chih.',
                'telefono': '614-123-4567',
                'horario': '9:00 AM - 11:00 PM',
                'impuesto': 0.16,  # 16% IVA
                'propina_sugerida': 0.15,  # 15% propina sugerida
                'moneda': 'MXN',
                'mesas_activas': True,
                'tiempo_max_espera': 45,  # minutos
                'email': 'contacto@codeandtaste.com',
                'capacidad_maxima': 80,  # personas
            }
            
            # Intentar cargar configuración desde archivo si existe
            self._load_from_file()
            
            RestaurantConfig._initialized = True
    
    def _load_from_file(self):
        """
        Carga configuración desde un archivo JSON si existe.
        """
        config_file = os.path.join(settings.BASE_DIR, 'restaurant_config.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
                    print(f"📁 [SINGLETON] Configuración cargada desde {config_file}")
            except Exception as e:
                print(f"⚠️ [SINGLETON] Error al cargar configuración: {e}")
    
    def save_to_file(self):
        """
        Guarda la configuración actual en un archivo JSON.
        """
        config_file = os.path.join(settings.BASE_DIR, 'restaurant_config.json')
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
                print(f"💾 [SINGLETON] Configuración guardada en {config_file}")
        except Exception as e:
            print(f"❌ [SINGLETON] Error al guardar configuración: {e}")
    
    # ==================== GETTERS ====================
    
    def get_nombre_restaurante(self):
        """Obtiene el nombre del restaurante"""
        return self._config['nombre_restaurante']
    
    def get_direccion(self):
        """Obtiene la dirección del restaurante"""
        return self._config['direccion']
    
    def get_telefono(self):
        """Obtiene el teléfono del restaurante"""
        return self._config['telefono']
    
    def get_horario(self):
        """Obtiene el horario del restaurante"""
        return self._config['horario']
    
    def get_impuesto(self):
        """Obtiene el porcentaje de impuesto (IVA)"""
        return self._config['impuesto']
    
    def get_propina_sugerida(self):
        """Obtiene el porcentaje de propina sugerida"""
        return self._config['propina_sugerida']
    
    def get_moneda(self):
        """Obtiene la moneda utilizada"""
        return self._config['moneda']
    
    def get_tiempo_max_espera(self):
        """Obtiene el tiempo máximo de espera en minutos"""
        return self._config['tiempo_max_espera']
    
    def get_email(self):
        """Obtiene el email del restaurante"""
        return self._config['email']
    
    def get_capacidad_maxima(self):
        """Obtiene la capacidad máxima de personas"""
        return self._config['capacidad_maxima']
    
    def get_all_config(self):
        """Obtiene toda la configuración como diccionario"""
        return self._config.copy()
    
    # ==================== SETTERS ====================
    
    def set_nombre_restaurante(self, nombre):
        """Establece el nombre del restaurante"""
        self._config['nombre_restaurante'] = nombre
        print(f"✅ [SINGLETON] Nombre actualizado: {nombre}")
    
    def set_impuesto(self, impuesto):
        """
        Establece el porcentaje de impuesto.
        
        Args:
            impuesto (float): Porcentaje de impuesto (0.0 a 1.0)
        """
        if 0 <= impuesto <= 1:
            self._config['impuesto'] = impuesto
            print(f"✅ [SINGLETON] Impuesto actualizado: {impuesto * 100}%")
        else:
            print("❌ [SINGLETON] Error: El impuesto debe estar entre 0 y 1")
    
    def set_propina_sugerida(self, propina):
        """
        Establece el porcentaje de propina sugerida.
        
        Args:
            propina (float): Porcentaje de propina (0.0 a 1.0)
        """
        if 0 <= propina <= 1:
            self._config['propina_sugerida'] = propina
            print(f"✅ [SINGLETON] Propina sugerida actualizada: {propina * 100}%")
        else:
            print("❌ [SINGLETON] Error: La propina debe estar entre 0 y 1")
    
    def set_horario(self, horario):
        """Establece el horario del restaurante"""
        self._config['horario'] = horario
        print(f"✅ [SINGLETON] Horario actualizado: {horario}")
    
    def set_capacidad_maxima(self, capacidad):
        """Establece la capacidad máxima"""
        if capacidad > 0:
            self._config['capacidad_maxima'] = capacidad
            print(f"✅ [SINGLETON] Capacidad máxima actualizada: {capacidad} personas")
        else:
            print("❌ [SINGLETON] Error: La capacidad debe ser mayor a 0")
    
    # ==================== UTILIDADES ====================
    
    def calcular_total_con_impuesto(self, subtotal):
        """
        Calcula el total aplicando el impuesto configurado.
        
        Args:
            subtotal (float): Subtotal sin impuesto
            
        Returns:
            dict: Diccionario con subtotal, impuesto y total
        """
        impuesto = subtotal * self.get_impuesto()
        total = subtotal + impuesto
        
        return {
            'subtotal': round(subtotal, 2),
            'impuesto': round(impuesto, 2),
            'total': round(total, 2)
        }
    
    def calcular_propina_sugerida(self, total):
        """
        Calcula la propina sugerida sobre el total.
        
        Args:
            total (float): Total de la cuenta
            
        Returns:
            float: Monto de propina sugerida
        """
        return round(total * self.get_propina_sugerida(), 2)
    
    def mostrar_configuracion(self):
        """
        Muestra la configuración actual en consola.
        Útil para debugging.
        """
        print("\n" + "="*60)
        print(f"🍽️  {self.get_nombre_restaurante()}")
        print("="*60)
        print(f"📍 Dirección: {self.get_direccion()}")
        print(f"📞 Teléfono: {self.get_telefono()}")
        print(f"📧 Email: {self.get_email()}")
        print(f"🕐 Horario: {self.get_horario()}")
        print(f"👥 Capacidad: {self.get_capacidad_maxima()} personas")
        print(f"💰 Impuesto: {self.get_impuesto() * 100}%")
        print(f"💵 Propina sugerida: {self.get_propina_sugerida() * 100}%")
        print(f"💳 Moneda: {self.get_moneda()}")
        print("="*60 + "\n")