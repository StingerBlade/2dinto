# restaurant/management/commands/init_data.py

"""
Comando para inicializar datos de prueba en el sistema
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from restaurant.models import Categoria, Platillo, Mesa, MetodoPago
from restaurant.patterns.singleton.config_manager import RestaurantConfig


class Command(BaseCommand):
    help = 'Inicializa datos de prueba para el sistema de restaurante'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n🚀 Iniciando carga de datos...\n'))

        # 1. Crear grupos de usuarios
        self.crear_grupos()

        # 2. Crear usuarios de prueba
        self.crear_usuarios()

        # 3. Crear categorías
        self.crear_categorias()

        # 4. Crear platillos
        self.crear_platillos()

        # 5. Crear mesas
        self.crear_mesas()

        # 6. Crear métodos de pago
        self.crear_metodos_pago()

        # 7. Inicializar configuración Singleton
        self.inicializar_configuracion()

        self.stdout.write(self.style.SUCCESS('\n✅ ¡Datos inicializados correctamente!\n'))
        self.mostrar_credenciales()

    def crear_grupos(self):
        """Crea los grupos de usuarios del sistema"""
        self.stdout.write('📋 Creando grupos...')
        
        grupos = ['admin', 'mesero', 'cocina', 'caja']
        
        for nombre_grupo in grupos:
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            if created:
                self.stdout.write(f'  ✓ Grupo "{nombre_grupo}" creado')
            else:
                self.stdout.write(f'  → Grupo "{nombre_grupo}" ya existe')

    def crear_usuarios(self):
        """Crea usuarios de prueba para cada rol"""
        self.stdout.write('\n👤 Creando usuarios...')

        usuarios = [
            {'username': 'admin', 'password': 'admin123', 'grupo': 'admin', 'is_staff': True, 'is_superuser': True},
            {'username': 'mesero1', 'password': 'mesero123', 'grupo': 'mesero', 'is_staff': False, 'is_superuser': False},
            {'username': 'cocina1', 'password': 'cocina123', 'grupo': 'cocina', 'is_staff': False, 'is_superuser': False},
            {'username': 'caja1', 'password': 'caja123', 'grupo': 'caja', 'is_staff': False, 'is_superuser': False},
        ]

        for user_data in usuarios:
            username = user_data['username']
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=user_data['password'],
                    is_staff=user_data['is_staff'],
                    is_superuser=user_data['is_superuser']
                )
                
                # Agregar al grupo
                grupo = Group.objects.get(name=user_data['grupo'])
                user.groups.add(grupo)
                
                self.stdout.write(f'  ✓ Usuario "{username}" creado (rol: {user_data["grupo"]})')
            else:
                self.stdout.write(f'  → Usuario "{username}" ya existe')

    def crear_categorias(self):
        """Crea categorías de platillos"""
        self.stdout.write('\n🏷️  Creando categorías...')

        categorias = [
            {'nombre': 'Entradas', 'descripcion': 'Platillos para comenzar'},
            {'nombre': 'Platos Fuertes', 'descripcion': 'Platillos principales'},
            {'nombre': 'Postres', 'descripcion': 'Dulces y postres'},
            {'nombre': 'Bebidas', 'descripcion': 'Bebidas frías y calientes'},
            {'nombre': 'Ensaladas', 'descripcion': 'Ensaladas frescas'},
        ]

        for cat_data in categorias:
            cat, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            if created:
                self.stdout.write(f'  ✓ Categoría "{cat.nombre}" creada')
            else:
                self.stdout.write(f'  → Categoría "{cat.nombre}" ya existe')

    def crear_platillos(self):
        """Crea platillos de ejemplo"""
        self.stdout.write('\n🍽️  Creando platillos...')

        platillos = [
            # Entradas
            {'nombre': 'Nachos con Queso', 'descripcion': 'Nachos crujientes con queso cheddar fundido', 'categoria': 'Entradas', 'precio': 85.00, 'tiempo': 10},
            {'nombre': 'Alitas BBQ', 'descripcion': 'Alitas de pollo bañadas en salsa BBQ', 'categoria': 'Entradas', 'precio': 120.00, 'tiempo': 15},
            {'nombre': 'Dedos de Queso', 'descripcion': 'Palitos de queso mozzarella empanizados', 'categoria': 'Entradas', 'precio': 95.00, 'tiempo': 12},
            
            # Platos Fuertes
            {'nombre': 'Hamburguesa Clásica', 'descripcion': 'Hamburguesa de res con queso, lechuga, tomate y papas', 'categoria': 'Platos Fuertes', 'precio': 145.00, 'tiempo': 20},
            {'nombre': 'Pizza Margarita', 'descripcion': 'Pizza con salsa de tomate, mozzarella y albahaca', 'categoria': 'Platos Fuertes', 'precio': 165.00, 'tiempo': 25},
            {'nombre': 'Pasta Alfredo', 'descripcion': 'Pasta fettuccine con salsa Alfredo y pollo', 'categoria': 'Platos Fuertes', 'precio': 155.00, 'tiempo': 18},
            {'nombre': 'Tacos al Pastor', 'descripcion': 'Tacos de carne al pastor con piña y cilantro', 'categoria': 'Platos Fuertes', 'precio': 110.00, 'tiempo': 15},
            
            # Ensaladas
            {'nombre': 'Ensalada César', 'descripcion': 'Lechuga romana, crutones, queso parmesano y aderezo césar', 'categoria': 'Ensaladas', 'precio': 95.00, 'tiempo': 8},
            {'nombre': 'Ensalada Griega', 'descripcion': 'Tomate, pepino, cebolla, aceitunas y queso feta', 'categoria': 'Ensaladas', 'precio': 105.00, 'tiempo': 8},
            
            # Postres
            {'nombre': 'Pastel de Chocolate', 'descripcion': 'Rebanada de pastel de chocolate con helado', 'categoria': 'Postres', 'precio': 75.00, 'tiempo': 5},
            {'nombre': 'Flan Napolitano', 'descripcion': 'Flan tradicional con caramelo', 'categoria': 'Postres', 'precio': 65.00, 'tiempo': 5},
            {'nombre': 'Helado', 'descripcion': 'Bola de helado sabor a elegir', 'categoria': 'Postres', 'precio': 45.00, 'tiempo': 3},
            
            # Bebidas
            {'nombre': 'Refresco', 'descripcion': 'Refresco de cola 600ml', 'categoria': 'Bebidas', 'precio': 35.00, 'tiempo': 2},
            {'nombre': 'Agua Natural', 'descripcion': 'Agua natural 1L', 'categoria': 'Bebidas', 'precio': 25.00, 'tiempo': 2},
            {'nombre': 'Limonada', 'descripcion': 'Limonada natural preparada', 'categoria': 'Bebidas', 'precio': 40.00, 'tiempo': 5},
            {'nombre': 'Café Americano', 'descripcion': 'Café americano caliente', 'categoria': 'Bebidas', 'precio': 35.00, 'tiempo': 5},
        ]

        for plat_data in platillos:
            categoria = Categoria.objects.get(nombre=plat_data['categoria'])
            
            plat, created = Platillo.objects.get_or_create(
                nombre=plat_data['nombre'],
                defaults={
                    'descripcion': plat_data['descripcion'],
                    'categoria': categoria,
                    'precio': plat_data['precio'],
                    'tiempo_preparacion': plat_data['tiempo'],
                    'disponible': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Platillo "{plat.nombre}" creado')
            else:
                self.stdout.write(f'  → Platillo "{plat.nombre}" ya existe')

    def crear_mesas(self):
        """Crea mesas del restaurante"""
        self.stdout.write('\n🪑 Creando mesas...')

        mesas = [
            {'numero': 1, 'capacidad': 2, 'ubicacion': 'Interior'},
            {'numero': 2, 'capacidad': 2, 'ubicacion': 'Interior'},
            {'numero': 3, 'capacidad': 4, 'ubicacion': 'Interior'},
            {'numero': 4, 'capacidad': 4, 'ubicacion': 'Interior'},
            {'numero': 5, 'capacidad': 6, 'ubicacion': 'Interior'},
            {'numero': 6, 'capacidad': 4, 'ubicacion': 'Terraza'},
            {'numero': 7, 'capacidad': 4, 'ubicacion': 'Terraza'},
            {'numero': 8, 'capacidad': 8, 'ubicacion': 'VIP'},
            {'numero': 9, 'capacidad': 6, 'ubicacion': 'Terraza'},
            {'numero': 10, 'capacidad': 2, 'ubicacion': 'Barra'},
        ]

        for mesa_data in mesas:
            mesa, created = Mesa.objects.get_or_create(
                numero=mesa_data['numero'],
                defaults={
                    'capacidad': mesa_data['capacidad'],
                    'ubicacion': mesa_data['ubicacion'],
                    'activa': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Mesa {mesa.numero} creada')
            else:
                self.stdout.write(f'  → Mesa {mesa.numero} ya existe')

    def crear_metodos_pago(self):
        """Crea métodos de pago disponibles"""
        self.stdout.write('\n💳 Creando métodos de pago...')

        metodos = ['Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', 'Transferencia']

        for metodo in metodos:
            mp, created = MetodoPago.objects.get_or_create(
                nombre=metodo,
                defaults={'activo': True}
            )
            
            if created:
                self.stdout.write(f'  ✓ Método "{metodo}" creado')
            else:
                self.stdout.write(f'  → Método "{metodo}" ya existe')

    def inicializar_configuracion(self):
        """Inicializa la configuración del restaurante usando Singleton"""
        self.stdout.write('\n⚙️  Inicializando configuración (Patrón Singleton)...')
        
        config = RestaurantConfig()
        config.mostrar_configuracion()
        
        self.stdout.write('  ✓ Configuración inicializada')

    def mostrar_credenciales(self):
        """Muestra las credenciales de acceso"""
        self.stdout.write(self.style.WARNING('\n' + '='*60))
        self.stdout.write(self.style.WARNING('CREDENCIALES DE ACCESO'))
        self.stdout.write(self.style.WARNING('='*60))
        
        credenciales = [
            ('admin', 'admin123', 'Administrador - Acceso completo'),
            ('mesero1', 'mesero123', 'Mesero - Gestión de pedidos'),
            ('cocina1', 'cocina123', 'Cocina - Ver pedidos'),
            ('caja1', 'caja123', 'Caja - Procesar pagos'),
        ]
        
        for username, password, descripcion in credenciales:
            self.stdout.write(f'\n👤 Usuario: {username}')
            self.stdout.write(f'   Contraseña: {password}')
            self.stdout.write(f'   Rol: {descripcion}')
        
        self.stdout.write(self.style.WARNING('\n' + '='*60 + '\n'))