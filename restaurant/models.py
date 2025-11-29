# restaurant/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    """
    Modelo para categorías de platillos (Entradas, Platos Fuertes, Postres, Bebidas)
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Platillo(models.Model):
    """
    Modelo para platillos del menú
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='platillos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='platillos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    tiempo_preparacion = models.IntegerField(help_text='Tiempo en minutos', default=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Platillo'
        verbose_name_plural = 'Platillos'
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Mesa(models.Model):
    """
    Modelo para mesas del restaurante
    """
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100, help_text='Ej: Terraza, Interior, VIP')
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero']
    
    def __str__(self):
        return f"Mesa {self.numero} ({self.capacidad} personas)"


class Pedido(models.Model):
    """
    Modelo para pedidos/órdenes
    """
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='pedidos')
    mesero = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pedidos_atendidos')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas_especiales = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero} - {self.estado}"
    
    def calcular_totales(self):
        """
        Calcula subtotal, impuesto y total del pedido
        """
        from restaurant.patterns.singleton.config_manager import RestaurantConfig
        
        config = RestaurantConfig()
        
        # Calcular subtotal sumando todos los items
        self.subtotal = sum(item.subtotal for item in self.items.all())
        
        # Calcular impuesto
        self.impuesto = self.subtotal * config.get_impuesto()
        
        # Calcular total
        self.total = self.subtotal + self.impuesto
        
        self.save()


class ItemPedido(models.Model):
    """
    Modelo para items individuales de un pedido
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
    
    def __str__(self):
        return f"{self.cantidad}x {self.platillo.nombre}"
    
    def save(self, *args, **kwargs):
        """
        Calcula el subtotal automáticamente antes de guardar
        """
        self.precio_unitario = self.platillo.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)


class MetodoPago(models.Model):
    """
    Modelo para métodos de pago disponibles
    """
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'
    
    def __str__(self):
        return self.nombre


class Pago(models.Model):
    """
    Modelo para registrar pagos de pedidos
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
    
    def __str__(self):
        return f"Pago de ${self.monto} - {self.metodo_pago}"


class Factura(models.Model):
    """
    Modelo para facturas generadas
    """
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='factura')
    folio = models.CharField(max_length=50, unique=True)
    rfc_cliente = models.CharField(max_length=13)
    nombre_cliente = models.CharField(max_length=200)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    archivo_pdf = models.FileField(upload_to='facturas/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
    
    def __str__(self):
        return f"Factura {self.folio}"