# src/models.py

class Cliente:
    """
    Representa un cliente con su informacion basica.
    aplica abstraccion: solo expone los datos relevantes del cliente.
    aplica Encapsulamiento: los atributos son accesibles a traves de propiedades(opcionalmente)
                            o directamente si se consideran publicos para este ejemplo simple.
    """
    def __init__(self, id_cliente:str, nombre: str, direccion: str, email:str):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.email = email # CORREGIDO: Antes era "email = direccion", ahora es "email = email"

    def __str__(self):
        return f"Cliente: {self.nombre} (ID: {self.id_cliente})"
    
"""
cliente1 = Cliente("0001", "Juan Cruz", "angel hubac 5183", "ejemplo@gmail.com")
print(cliente1)
"""

class Producto:
    """
    Respresenta un producto con su descripcion y precio unitario.
    aplica Abstraccion: oculta como se gestiona internamente los precios o descripciones
    """

    def __init__(self, id_producto: str, descripcion: str, precio_unitario: float):
        self.id_producto = id_producto
        self.descripcion = descripcion
        # Encapsulamiento: Nos aseguramos que el precio sea positivo
        if precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo.")
        self._precio_unitario = precio_unitario #Usamos un guion bajo para indicar que es protegido

    @property
    def precio_unitario(self):
        return self._precio_unitario
    
    def __str__(self):
        return f"Producto: {self.descripcion} (${self.precio_unitario:.2f})" #.2f formateo el valor del FLOAT mostrando el numero con solo 2 decimales, para ser mas precisos y redondear el numero
    
 
"""    
pr1 = Producto("0002", "Iphone 16 Pro Max", 1250)
print(pr1)
"""

class ItemFactura:
    """
    Representa una linea de un articulo en una factura.
    Aplica Encapsulamiento: El subtotal se calcula internamente y no se puede modificar directamente
    """

    def __init__(self, producto: Producto, cantidad: int):
        if not isinstance(producto, Producto):
            raise TypeError("El 'producto' debe ser una instancia de la clase Producto.")
        if cantidad <= 0:
            raise ValueError("la cantidad debe ser mayor que cero(0).")
        
        self.producto = producto
        self.cantidad = cantidad
        # CORREGIDO: Ahora se calcula y asigna _subtotal
        self._subtotal = self.producto.precio_unitario * self.cantidad 

    @property #getter para subtotal
    def subtotal(self):
        return self._subtotal
    
    def __str__(self):
        # CORREGIDO: Acceso a precio_unitario a través de self.producto
        return (f"Item: {self.producto.descripcion} x {self.cantidad} "
                f"(@${self.producto.precio_unitario:.2f} c/u) = ${self.subtotal:.2f}")


class Factura:
    """
    Representa una factura completa, agrupando clientes e items.
    Aplica Encapsulamiento: El total se calcula y actualiza internamente.
    """

    def __init__(self, id_factura : str, cliente: Cliente, fecha: str):
        if not isinstance(cliente, Cliente):
            raise ValueError("El 'Cliente' debe ser una instancia de la clase Cliente")
        
        self.id_factura = id_factura
        self.cliente = cliente
        self.fecha = fecha 
        self._items = []
        self._total = 0.0 

    # CORREGIDO: Estos métodos deben estar a nivel de CLASE, no dentro de __init__
    def agregar_item(self, item: ItemFactura):
        # Añade un item a la factura y actualiza el total.
        if not isinstance(item, ItemFactura):
            raise ValueError("El 'item' no es una instancia de la clase ItemFactura.")
        self._items.append(item)
        self._calcular_total() # actualiza el total.

    def _calcular_total(self):
        # metodo privado para recalcular el total de la factura
        self._total = sum(item.subtotal for item in self._items)

    @property # crea un getter de items
    def items(self):
        return self._items # devuelve una copia para evitar modificacion externa directa
    
    @property # getter para total
    def total(self):
        return self._total
    
    def __str__(self):
        items_str = "\n".join(str(item) for item in self._items)
        return (f"Factura ID:{self.id_factura}\n"
                f"Cliente: {self.cliente.nombre}\n"
                f"Fecha: {self.fecha}\n" 
                f"Items:\n {items_str}\n"
                f"Total: {self.total:.2f}")