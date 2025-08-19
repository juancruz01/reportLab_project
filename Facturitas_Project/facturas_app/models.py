from django.db import models


# Create your models here.
class Cliente(models.Model):
    # Django creará automáticamente un campo 'id' de tipo entero,
    # que será la clave primaria.
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    descripcion = models.CharField(max_length=200)
    # DecimalField es ideal para dinero
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descripcion
    
class Factura(models.Model):
    # Relaciona la factura con un cliente.
    # on_delete=models.CASCADE significa que si borras un cliente,
    # se borran todas sus facturas.
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True) # La fecha se pone sola al crear
    # El total se puede calcular en la lógica de negocio, no siempre se guarda en la DB
    total = models.DecimalField(max_digits=10, decimal_places=2) 
    # Opcional, para guardar la ruta del PDF
    pdf_path = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f"Factura #{self.pk}" # El id de Django se accede con .pk
    

class ItemFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        # Este cálculo se hace "al vuelo" cada vez que se pide, no se guarda en la DB.
        return self.cantidad * self.producto.precio_unitario

    def __str__(self):
        return f"Item: {self.producto.descripcion} x {self.cantidad}"
    

