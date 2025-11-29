# Sistema de Gestión de Restaurante

Sistema completo de gestión de restaurante desarrollado con Django que implementa tres patrones de diseño fundamentales.

## 🎯 Patrones de Diseño Implementados

### 1. **Singleton (Creacional)**
- **Ubicación:** `restaurant/patterns/singleton/config_manager.py`
- **Propósito:** Gestión única de configuración del restaurante
- **Uso:** Impuestos, propinas, horarios, capacidad

### 2. **Decorator (Estructural)**
- **Ubicación:** `restaurant/patterns/decorator/view_decorators.py`
- **Propósito:** Añadir funcionalidades a vistas dinámicamente
- **Implementaciones:**
  - `@log_view_access` - Logging de accesos
  - `@require_role` - Control de permisos por rol
  - `@measure_performance` - Medición de rendimiento

### 3. **Observer (Comportamiento)**
- **Ubicación:** `restaurant/patterns/observer/observers.py`
- **Propósito:** Sistema de notificaciones automáticas
- **Observadores:**
  - `CocinaObserver` - Notificaciones a cocina
  - `MeseroObserver` - Notificaciones a meseros
  - `AdministradorObserver` - Monitoreo general

## 🛠️ Tecnologías Utilizadas

- **Framework:** Django 4.2+
- **Base de datos:** SQLite (desarrollo)
- **Frontend:** Bootstrap 5
- **Lenguaje:** Python 3.8+

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
cd restaurant_management
```

### 2. Crear entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install django pillow
```

### 4. Crear estructura de carpetas para media
```bash
mkdir media
mkdir media/platillos
mkdir media/facturas
```

### 5. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Cargar datos de prueba
```bash
python manage.py init_data
```

Este comando creará:
- ✅ Grupos de usuarios (admin, mesero, cocina, caja)
- ✅ Usuarios de prueba con contraseñas
- ✅ Categorías de platillos
- ✅ Platillos de ejemplo
- ✅ Mesas del restaurante
- ✅ Métodos de pago
- ✅ Configuración inicial (Singleton)

### 7. Ejecutar el servidor
```bash
python manage.py runserver
```

### 8. Acceder al sistema

Abre tu navegador en: `http://127.0.0.1:8000`

## 👤 Credenciales de Acceso

| Usuario  | Contraseña  | Rol            | Permisos                    |
|----------|-------------|----------------|-----------------------------|
| admin    | admin123    | Administrador  | Acceso completo al sistema  |
| mesero1  | mesero123   | Mesero         | Gestión de pedidos y mesas  |
| cocina1  | cocina123   | Cocina         | Ver y actualizar pedidos    |
| caja1    | caja123     | Caja           | Procesar pagos              |

## 📁 Estructura del Proyecto
```
restaurant_management/
├── restaurant_project/          # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── restaurant/                  # Aplicación principal
│   ├── models.py               # Modelos de datos
│   ├── views.py                # Vistas
│   ├── forms.py                # Formularios
│   ├── urls.py                 # URLs de la app
│   ├── admin.py                # Configuración del admin
│   ├── patterns/               # Patrones de diseño
│   │   ├── singleton/
│   │   │   └── config_manager.py
│   │   ├── decorator/
│   │   │   └── view_decorators.py
│   │   └── observer/
│   │       └── observers.py
│   └── management/
│       └── commands/
│           └── init_data.py
├── templates/                   # Plantillas HTML
│   ├── base.html
│   ├── registration/
│   └── restaurant/
├── media/                       # Archivos subidos
├── static/                      # Archivos estáticos
├── db.sqlite3                   # Base de datos
└── README.md
```

## 🎮 Funcionalidades Principales

### Gestión de Mesas
- ✅ CRUD completo de mesas
- ✅ Visualización de estado (ocupada/disponible)
- ✅ Creación rápida de pedidos desde mesa

### Gestión de Pedidos
- ✅ Crear pedidos por mesa
- ✅ Agregar/quitar platillos
- ✅ Cambio de estados (Pendiente → En Preparación → Listo → Entregado)
- ✅ **Notificaciones automáticas** (Patrón Observer)

### Gestión de Platillos
- ✅ CRUD completo de platillos
- ✅ Categorización
- ✅ Búsqueda y filtros
- ✅ Imágenes de platillos

### Configuración del Restaurante
- ✅ Configuración única (Patrón Singleton)
- ✅ Impuestos personalizables
- ✅ Propina sugerida
- ✅ Horarios y capacidad

### Sistema de Pagos
- ✅ Múltiples métodos de pago
- ✅ Cálculo automático de totales
- ✅ Propina sugerida basada en configuración

## 📊 Demostración de Patrones

### Patrón Singleton en acción:
```python
from restaurant.patterns.singleton.config_manager import RestaurantConfig

# Primera instancia
config1 = RestaurantConfig()
config1.set_impuesto(0.16)

# Segunda "instancia" (en realidad es la misma)
config2 = RestaurantConfig()
print(config2.get_impuesto())  # Output: 0.16

# Ambas son la misma instancia
print(config1 is config2)  # Output: True
```

### Patrón Observer en acción:

Cuando cambias el estado de un pedido, automáticamente se notifica a:
- 🍳 Cocina (nuevos pedidos y cancelaciones)
- 🧑‍🍳 Meseros (pedidos listos)
- 👔 Administrador (todos los eventos)

Verás las notificaciones en la consola del servidor.

### Patrón Decorator en acción:
```python
@login_required
@log_view_access          # Registra cada acceso
@require_role('mesero')   # Solo meseros pueden acceder
@measure_performance      # Mide tiempo de ejecución
def crear_pedido(request):
    # ...
```

## 📝 Logging

El sistema registra todos los eventos en `restaurant.log`:
- Accesos a vistas (Decorator)
- Cambios de estado en pedidos (Observer)
- Operaciones CRUD
- Errores y advertencias

## 🧪 Pruebas

Para probar el sistema completo:

1. **Login como admin** → Configurar el restaurante
2. **Login como mesero1** → Crear un pedido en una mesa
3. **Observa la consola** → Verás las notificaciones del Observer
4. **Login como cocina1** → Cambiar estado a "En Preparación"
5. **Observa nuevamente** → Más notificaciones
6. **Login como caja1** → Procesar el pago

## 🐛 Solución de Problemas

### Error: "No module named 'restaurant'"
```bash
# Asegúrate de estar en el directorio correcto
cd restaurant_management
python manage.py runserver
```

### Error: "Table doesn't exist"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Las imágenes no se muestran
```bash
# Verifica que exista la carpeta media
mkdir -p media/platillos
```

## 📚 Documentación Adicional

- **Modelos:** Ver `restaurant/models.py`
- **Patrones:** Ver carpeta `restaurant/patterns/`
- **Forms:** Ver `restaurant/forms.py`
- **Admin:** Accede a `/admin` con usuario `admin`

## 👨‍💻 Autor

[Tu Nombre] - Grupo IDGS71N
Arquitecturas de Software - UTCH

## 📅 Fecha

Noviembre 2024

## 📄 Licencia

Este proyecto es con fines educativos.