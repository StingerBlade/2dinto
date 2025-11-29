# 🚀 GUÍA PASO A PASO - Sistema de Gestión de Restaurante

Esta guía te llevará desde cero hasta tener el sistema completamente funcional.

---

## ✅ PASO 1: VERIFICAR REQUISITOS

### 1.1 Verificar Python

Abre una terminal/cmd y ejecuta:
```bash
python --version
```

Debe mostrar Python 3.8 o superior. Si no tienes Python, descárgalo de: https://www.python.org/downloads/

### 1.2 Verificar pip
```bash
pip --version
```

Si no funciona, instala pip siguiendo: https://pip.pypa.io/en/stable/installation/

---

## ✅ PASO 2: CREAR ESTRUCTURA DEL PROYECTO

### 2.1 Crear carpeta principal
```bash
mkdir restaurant_management
cd restaurant_management
```

### 2.2 Crear entorno virtual

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

### 2.3 Activar entorno virtual

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

✅ **Verificación:** Deberías ver `(venv)` al inicio de tu línea de comando.

---

## ✅ PASO 3: INSTALAR DEPENDENCIAS
```bash
pip install django pillow
```

Espera a que termine la instalación.

---

## ✅ PASO 4: CREAR PROYECTO DJANGO
```bash
django-admin startproject restaurant_project .
python manage.py startapp restaurant
```

**Nota:** El punto (.) al final es importante.

---

## ✅ PASO 5: CREAR ESTRUCTURA DE CARPETAS

### 5.1 Crear carpetas de patterns
```bash
mkdir -p restaurant/patterns/singleton
mkdir -p restaurant/patterns/decorator
mkdir -p restaurant/patterns/observer
```

**Windows (si mkdir -p no funciona):**
```bash
mkdir restaurant\patterns
mkdir restaurant\patterns\singleton
mkdir restaurant\patterns\decorator
mkdir restaurant\patterns\observer
```

### 5.2 Crear carpetas de management
```bash
mkdir -p restaurant/management/commands
```

**Windows:**
```bash
mkdir restaurant\management
mkdir restaurant\management\commands
```

### 5.3 Crear carpetas de templates
```bash
mkdir -p templates/restaurant/categorias
mkdir -p templates/restaurant/platillos
mkdir -p templates/restaurant/mesas
mkdir -p templates/restaurant/pedidos
mkdir -p templates/registration
```

**Windows:**
```bash
mkdir templates
mkdir templates\restaurant
mkdir templates\restaurant\categorias
mkdir templates\restaurant\platillos
mkdir templates\restaurant\mesas
mkdir templates\restaurant\pedidos
mkdir templates\registration
```

### 5.4 Crear carpetas de media
```bash
mkdir -p media/platillos
mkdir -p media/facturas
```

**Windows:**
```bash
mkdir media
mkdir media\platillos
mkdir media\facturas
```

### 5.5 Crear carpetas de static (opcional)
```bash
mkdir static
```

---

## ✅ PASO 6: CREAR ARCHIVOS __init__.py

Es importante crear estos archivos vacíos para que Python reconozca las carpetas como paquetes:
```bash
# Linux/Mac
touch restaurant/patterns/__init__.py
touch restaurant/patterns/singleton/__init__.py
touch restaurant/patterns/decorator/__init__.py
touch restaurant/patterns/observer/__init__.py
touch restaurant/management/__init__.py
touch restaurant/management/commands/__init__.py
```

**Windows (usa un editor de texto o ejecuta estos comandos):**
```bash
type nul > restaurant\patterns\__init__.py
type nul > restaurant\patterns\singleton\__init__.py
type nul > restaurant\patterns\decorator\__init__.py
type nul > restaurant\patterns\observer\__init__.py
type nul > restaurant\management\__init__.py
type nul > restaurant\management\commands\__init__.py
```

---

## ✅ PASO 7: COPIAR TODOS LOS ARCHIVOS

Ahora copia el contenido de cada archivo que te proporcioné en la conversación:

### 7.1 Archivos de configuración
- ✅ `restaurant_project/settings.py`
- ✅ `restaurant_project/urls.py`

### 7.2 Archivos de la app restaurant
- ✅ `restaurant/models.py`
- ✅ `restaurant/views.py`
- ✅ `restaurant/forms.py`
- ✅ `restaurant/urls.py`
- ✅ `restaurant/admin.py`

### 7.3 Archivos de patrones
- ✅ `restaurant/patterns/singleton/config_manager.py`
- ✅ `restaurant/patterns/decorator/view_decorators.py`
- ✅ `restaurant/patterns/observer/observers.py`

### 7.4 Archivo de inicialización
- ✅ `restaurant/management/commands/init_data.py`

### 7.5 Templates (todos los archivos .html)
- ✅ `templates/base.html`
- ✅ `templates/registration/login.html`
- ✅ `templates/restaurant/dashboard.html`
- ✅ `templates/restaurant/configuracion.html`
- ✅ Y todos los demás templates de categorías, platillos, mesas, pedidos

### 7.6 Documentación
- ✅ `README.md`

---

## ✅ PASO 8: VERIFICAR ESTRUCTURA FINAL

Tu estructura debería verse así:
```
restaurant_management/
├── venv/                        ← Entorno virtual
├── restaurant_project/
│   ├── __init__.py
│   ├── settings.py             ← CONFIGURADO
│   ├── urls.py                 ← CONFIGURADO
│   ├── wsgi.py
│   └── asgi.py
├── restaurant/
│   ├── __init__.py
│   ├── models.py               ← CREADO
│   ├── views.py                ← CREADO
│   ├── forms.py                ← CREADO
│   ├── urls.py                 ← CREADO
│   ├── admin.py                ← CREADO
│   ├── apps.py
│   ├── patterns/
│   │   ├── __init__.py
│   │   ├── singleton/
│   │   │   ├── __init__.py
│   │   │   └── config_manager.py
│   │   ├── decorator/
│   │   │   ├── __init__.py
│   │   │   └── view_decorators.py
│   │   └── observer/
│   │       ├── __init__.py
│   │       └── observers.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── init_data.py
├── templates/
│   ├── base.html
│   ├── registration/
│   │   └── login.html
│   └── restaurant/
│       ├── dashboard.html
│       ├── configuracion.html
│       ├── categorias/
│       ├── platillos/
│       ├── mesas/
│       └── pedidos/
├── media/
│   ├── platillos/
│   └── facturas/
├── static/
├── manage.py
└── README.md
```

---

## ✅ PASO 9: CREAR BASE DE DATOS

### 9.1 Crear migraciones
```bash
python manage.py makemigrations
```

**Salida esperada:**
```
Migrations for 'restaurant':
  restaurant/migrations/0001_initial.py
    - Create model Categoria
    - Create model Mesa
    - Create model MetodoPago
    - Create model Platillo
    - Create model Pedido
    - Create model ItemPedido
    - Create model Pago
    - Create model Factura
```

### 9.2 Aplicar migraciones
```bash
python manage.py migrate
```

**Salida esperada:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, restaurant, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying restaurant.0001_initial... OK
```

---

## ✅ PASO 10: CARGAR DATOS INICIALES
```bash
python manage.py init_data
```

**Salida esperada:**
```
🚀 Iniciando carga de datos...

📋 Creando grupos...
  ✓ Grupo "admin" creado
  ✓ Grupo "mesero" creado
  ✓ Grupo "cocina" creado
  ✓ Grupo "caja" creado

👤 Creando usuarios...
  ✓ Usuario "admin" creado (rol: admin)
  ✓ Usuario "mesero1" creado (rol: mesero)
  ✓ Usuario "cocina1" creado (rol: cocina)
  ✓ Usuario "caja1" creado (rol: caja)

🏷️  Creando categorías...
  ✓ Categoría "Entradas" creada
  ✓ Categoría "Platos Fuertes" creada
  ✓ Categoría "Postres" creada
  ✓ Categoría "Bebidas" creada
  ✓ Categoría "Ensaladas" creada

🍽️  Creando platillos...
  ✓ Platillo "Nachos con Queso" creado
  ✓ Platillo "Hamburguesa Clásica" creado
  ... (más platillos)

🪑 Creando mesas...
  ✓ Mesa 1 creada
  ✓ Mesa 2 creada
  ... (10 mesas en total)

💳 Creando métodos de pago...
  ✓ Método "Efectivo" creado
  ✓ Método "Tarjeta de Crédito" creado
  ✓ Método "Tarjeta de Débito" creado
  ✓ Método "Transferencia" creado

⚙️  Inicializando configuración (Patrón Singleton)...
🔧 Creando NUEVA instancia de RestaurantConfig...
✅ Configuración inicializada

==================================================
🍽️  Restaurante Code & Taste
==================================================
📍 Dirección: Av. Universidad #123, Chihuahua, Chih.
📞 Teléfono: 614-123-4567
📧 Email: contacto@codeandtaste.com
🕐 Horario: 9:00 AM - 11:00 PM
👥 Capacidad: 80 personas
💰 Impuesto: 16.0%
💵 Propina sugerida: 15.0%
💳 Moneda: MXN
==================================================

✅ ¡Datos inicializados correctamente!

============================================================
CREDENCIALES DE ACCESO
============================================================

👤 Usuario: admin
   Contraseña: admin123
   Rol: Administrador - Acceso completo

👤 Usuario: mesero1
   Contraseña: mesero123
   Rol: Mesero - Gestión de pedidos

👤 Usuario: cocina1
   Contraseña: cocina123
   Rol: Cocina - Ver pedidos

👤 Usuario: caja1
   Contraseña: caja123
   Rol: Caja - Procesar pagos

============================================================
```

---

## ✅ PASO 11: EJECUTAR EL SERVIDOR
```bash
python manage.py runserver
```

**Salida esperada:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 28, 2024 - 15:30:00
Django version 4.2.x, using settings 'restaurant_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## ✅ PASO 12: PROBAR EL SISTEMA

### 12.1 Abrir navegador

Abre tu navegador en: **http://127.0.0.1:8000**

### 12.2 Iniciar sesión

Usa cualquiera de estas credenciales:

| Usuario  | Contraseña | Rol           |
|----------|------------|---------------|
| admin    | admin123   | Administrador |
| mesero1  | mesero123  | Mesero        |
| cocina1  | cocina123  | Cocina        |
| caja1    | caja123    | Caja          |

---

## ✅ PASO 13: PRUEBA DE PATRONES

### 13.1 Probar Patrón Singleton

1. Login como **admin**
2. Ve a **Configuración** en el menú lateral
3. Cambia el impuesto a 18%
4. Guarda
5. Ve a **Dashboard**
6. Observa que el impuesto cambió globalmente

**En la consola verás:**
```
🔧 [SINGLETON] Creando NUEVA instancia de RestaurantConfig...
✅ [SINGLETON] Impuesto actualizado: 18.0%
💾 [SINGLETON] Configuración guardada en restaurant_config.json
```

### 13.2 Probar Patrón Decorator

1. En la consola del servidor, observa los logs
2. Cada vez que accedas a una vista verás:
```
📝 [DECORATOR LOG] [2024-11-28 15:35:12] 👤 Usuario: admin | 🎯 Vista: dashboard | 📡 Método: GET | 🌐 IP: 127.0.0.1

🚀 [DECORATOR PERFORMANCE] RÁPIDO! ⏱️ Vista: dashboard | Tiempo: 0.0523s
```

### 13.3 Probar Patrón Observer

1. Login como **mesero1**
2. Ve a **Mesas**
3. Haz clic en **"Crear Pedido"** en la Mesa 1
4. Crea el pedido
5. **Observa la consola del servidor:**
```
➕ [OBSERVER] CocinaObserver suscrito al Pedido #1
➕ [OBSERVER] MeseroObserver suscrito al Pedido #1
➕ [OBSERVER] AdministradorObserver suscrito al Pedido #1

📣 [15:40:15] NOTIFICACIÓN - Pedido #1 - Evento: cambio_estado
   Notificando a 3 observador(es)...

🍳 [COCINA] [15:40:15] NUEVO PEDIDO - Mesa 1 - Pedido #1
   Items:

🧑‍🍳 [MESERO] [15:40:15] ...

👔 [ADMIN] [15:40:15] Pedido #1 - Estado: None → pendiente - Mesa 1
```

6. Ahora agrega items al pedido
7. Cambia el estado a "En Preparación"
8. **Observa más notificaciones en la consola**

---

## ✅ PASO 14: PROBAR FUNCIONALIDADES COMPLETAS

### Flujo completo de un pedido:

1. **Mesero crea pedido:**
   - Login: `mesero1 / mesero123`
   - Mesas → Mesa 3 → Crear Pedido
   - Agregar items (Hamburguesa, Refresco)
   - Ver notificaciones en consola

2. **Cocina prepara:**
   - Login: `cocina1 / cocina123`
   - Pedidos → Ver pedido
   - Cambiar estado a "En Preparación"
   - Luego "Listo"
   - Ver notificaciones

3. **Mesero entrega:**
   - Login: `mesero1 / mesero123`
   - Cambiar estado a "Entregado"

4. **Caja cobra:**
   - Login: `caja1 / caja123`
   - Pedidos → Ver pedido
   - "Procesar Pago"
   - Seleccionar método de pago
   - Ver notificación de pago

---

## 🎉 ¡SISTEMA COMPLETO Y FUNCIONANDO!

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Problema 1: "ModuleNotFoundError: No module named 'restaurant'"

**Solución:**
```bash
# Asegúrate de estar en la carpeta correcta
cd restaurant_management
# Verifica que existe manage.py
ls manage.py  # Linux/Mac
dir manage.py # Windows
```

### Problema 2: "django.db.utils.OperationalError: no such table"

**Solución:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problema 3: "TemplateDoesNotExist"

**Solución:**
Verifica que `DIRS` en `settings.py` apunte a la carpeta templates:
```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

### Problema 4: Imágenes no se muestran

**Solución:**
```bash
# Crear carpeta media
mkdir -p media/platillos

# Verificar settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Problema 5: "Permission denied" al activar venv (Windows PowerShell)

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema 6: Los decoradores no funcionan

**Solución:**
Verifica que los usuarios tengan grupos asignados:
```bash
python manage.py init_data
```

---

## 📊 VERIFICACIÓN FINAL

### Checklist de funcionalidades:

- [ ] ✅ Login funciona
- [ ] ✅ Dashboard muestra estadísticas
- [ ] ✅ Puedo crear categorías
- [ ] ✅ Puedo crear platillos
- [ ] ✅ Puedo crear mesas
- [ ] ✅ Puedo crear pedidos
- [ ] ✅ Puedo agregar items a pedidos
- [ ] ✅ Puedo cambiar estado de pedidos
- [ ] ✅ Veo notificaciones en consola (Observer)
- [ ] ✅ Veo logs de acceso en consola (Decorator)
- [ ] ✅ La configuración es única (Singleton)
- [ ] ✅ Puedo procesar pagos
- [ ] ✅ La propina se calcula automáticamente

---

## 🎓 SIGUIENTE PASO: DOCUMENTACIÓN

Ahora que tienes el sistema funcionando, crea tu documentación:

1. **Diagramas UML** (usa los códigos Mermaid que te daré)
2. **Documento de Justificación de Patrones**
3. **Manual de Usuario**
4. **Video demostración** (opcional)

---

## 📞 SOPORTE

Si tienes problemas:
1. Verifica que seguiste todos los pasos
2. Revisa la sección de solución de problemas
3. Verifica los logs en `restaurant.log`
4. Revisa la consola del servidor

---

**¡FELICIDADES! 🎉 Tienes un sistema completo de gestión de restaurante con 3 patrones de diseño implementados.**