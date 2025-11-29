# restaurant/forms.py

"""
Formularios del Sistema de Gestión de Restaurante

Este módulo contiene todos los formularios Django para el CRUD
de las entidades del sistema.
"""

from django import forms
from .models import (
    Categoria, Platillo, Mesa, Pedido, ItemPedido,
    MetodoPago, Pago, Factura
)


class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear y editar categorías
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Entradas, Platos Fuertes, Postres'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción',
            'activo': 'Activa'
        }


class PlatilloForm(forms.ModelForm):
    """
    Formulario para crear y editar platillos
    """
    class Meta:
        model = Platillo
        fields = [
            'nombre', 'descripcion', 'categoria', 'precio',
            'imagen', 'disponible', 'tiempo_preparacion'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del platillo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del platillo'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_preparacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Tiempo en minutos'
            })
        }
        labels = {
            'nombre': 'Nombre del Platillo',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'precio': 'Precio (MXN)',
            'imagen': 'Imagen',
            'disponible': 'Disponible',
            'tiempo_preparacion': 'Tiempo de Preparación (minutos)'
        }
    
    def clean_precio(self):
        """Validar que el precio sea positivo"""
        precio = self.cleaned_data.get('precio')
        if precio and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a cero')
        return precio
    
    def clean_tiempo_preparacion(self):
        """Validar que el tiempo de preparación sea razonable"""
        tiempo = self.cleaned_data.get('tiempo_preparacion')
        if tiempo and (tiempo < 1 or tiempo > 180):
            raise forms.ValidationError('El tiempo debe estar entre 1 y 180 minutos')
        return tiempo


class MesaForm(forms.ModelForm):
    """
    Formulario para crear y editar mesas
    """
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad', 'ubicacion', 'activa']
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Número de mesa'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '20',
                'placeholder': 'Número de personas'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Terraza, Interior, VIP'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'numero': 'Número de Mesa',
            'capacidad': 'Capacidad (personas)',
            'ubicacion': 'Ubicación',
            'activa': 'Activa'
        }
    
    def clean_numero(self):
        """Validar que el número de mesa sea único"""
        numero = self.cleaned_data.get('numero')
        if numero:
            # Si estamos editando, excluir la mesa actual
            if self.instance.pk:
                exists = Mesa.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists()
            else:
                exists = Mesa.objects.filter(numero=numero).exists()
            
            if exists:
                raise forms.ValidationError(f'Ya existe una mesa con el número {numero}')
        return numero
    
    def clean_capacidad(self):
        """Validar capacidad razonable"""
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad and (capacidad < 1 or capacidad > 20):
            raise forms.ValidationError('La capacidad debe estar entre 1 y 20 personas')
        return capacidad


class PedidoForm(forms.ModelForm):
    """
    Formulario para crear pedidos
    """
    class Meta:
        model = Pedido
        fields = ['mesa', 'notas_especiales']
        widgets = {
            'mesa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notas_especiales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas especiales del pedido (opcional)'
            })
        }
        labels = {
            'mesa': 'Mesa',
            'notas_especiales': 'Notas Especiales'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo mesas activas
        self.fields['mesa'].queryset = Mesa.objects.filter(activa=True)
    
    def clean_mesa(self):
        """Validar que la mesa no tenga un pedido activo"""
        mesa = self.cleaned_data.get('mesa')
        if mesa:
            pedido_activo = Pedido.objects.filter(
                mesa=mesa,
                estado__in=['pendiente', 'en_preparacion', 'listo']
            ).exists()
            
            if pedido_activo:
                raise forms.ValidationError(
                    f'La mesa {mesa.numero} ya tiene un pedido activo'
                )
        return mesa


class ItemPedidoForm(forms.ModelForm):
    """
    Formulario para agregar items a un pedido
    """
    class Meta:
        model = ItemPedido
        fields = ['platillo', 'cantidad', 'notas']
        widgets = {
            'platillo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'notas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Sin cebolla, término medio (opcional)'
            })
        }
        labels = {
            'platillo': 'Platillo',
            'cantidad': 'Cantidad',
            'notas': 'Notas Especiales'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo platillos disponibles
        self.fields['platillo'].queryset = Platillo.objects.filter(disponible=True)
    
    def clean_cantidad(self):
        """Validar cantidad razonable"""
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad and (cantidad < 1 or cantidad > 50):
            raise forms.ValidationError('La cantidad debe estar entre 1 y 50')
        return cantidad
    
    def clean_platillo(self):
        """Validar que el platillo esté disponible"""
        platillo = self.cleaned_data.get('platillo')
        if platillo and not platillo.disponible:
            raise forms.ValidationError(
                f'El platillo "{platillo.nombre}" no está disponible actualmente'
            )
        return platillo


class PagoForm(forms.ModelForm):
    """
    Formulario para procesar pagos
    """
    class Meta:
        model = Pago
        fields = ['metodo_pago', 'monto', 'referencia']
        widgets = {
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de tarjeta, transacción, etc. (opcional)'
            })
        }
        labels = {
            'metodo_pago': 'Método de Pago',
            'monto': 'Monto (MXN)',
            'referencia': 'Referencia'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo métodos de pago activos
        self.fields['metodo_pago'].queryset = MetodoPago.objects.filter(activo=True)
    
    def clean_monto(self):
        """Validar que el monto sea positivo"""
        monto = self.cleaned_data.get('monto')
        if monto and monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero')
        return monto


class FacturaForm(forms.ModelForm):
    """
    Formulario para generar facturas
    """
    class Meta:
        model = Factura
        fields = ['rfc_cliente', 'nombre_cliente']
        widgets = {
            'rfc_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XAXX010101000',
                'maxlength': '13'
            }),
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo o razón social'
            })
        }
        labels = {
            'rfc_cliente': 'RFC',
            'nombre_cliente': 'Nombre / Razón Social'
        }
    
    def clean_rfc_cliente(self):
        """Validar formato básico de RFC"""
        rfc = self.cleaned_data.get('rfc_cliente', '').upper().strip()
        
        if rfc:
            # Validación básica de longitud
            if len(rfc) not in [12, 13]:
                raise forms.ValidationError('El RFC debe tener 12 o 13 caracteres')
            
            # Validar caracteres alfanuméricos
            if not rfc.isalnum():
                raise forms.ValidationError('El RFC solo debe contener letras y números')
        
        return rfc