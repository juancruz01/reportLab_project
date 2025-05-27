class Cliente:
    """
    Representa un cliente con su informacion basica.
    aplica abstraccion: solo expone los datos relevantes del cliente.
    aplica Encapsulamiento: los atributos son accesibles a traves de propiedades(opcionalmente)
                            o directamente si se consideran publicos para este ejemplo simple.
    """
    def __init__(self, id_cliente:str, nombre: str, direccion: str, email:str, ):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.email = direccion

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
        return f"Producto: {self.descripcion} (${self.precio_unitario:.2f})"
    
pr1 = Producto("0002", "Iphone 16 Pro Max", 1250)

print(pr1)