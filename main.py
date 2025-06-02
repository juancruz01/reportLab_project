# main.py

from src.models import Cliente, Producto, ItemFactura, Factura
# CORREGIDO: Asegúrate que InformeVentaPDF es InformeVentasPDF si así se llama en documents.py
from src.documents import FacturaPDF, InformeVentaPDF
import os
from datetime import datetime

def crear_datos_ejemplo():
    """
    Crea datos de ejemplo para generar una factura y un informe de ventas.
    """
    print("DEBUG: Creando datos de ejemplo...")
    cliente1 = Cliente("C001", "Juan Cruz", "Calle falsa 123, Claypole", "juano@gmail.com")
    # CORREGIDO: La clase Cliente solo acepta 4 argumentos (id, nombre, direccion, email).
    # Se eliminó el argumento extra "Alejandro Korn".
    cliente2 = Cliente("C002", "Leandro Herrera", "Avenida Siempre Viva 456", "Leandro@gmail.com")

    cliente3 = Cliente("C003", "Facundo Sena", "Calle re lejos 666", "elfacupa@gmail.com")

    producto1 = Producto("P001", "Iphone 14 Pro", 700.00)
    producto2 = Producto("P002", "Samsung Galaxy S23", 650.00)
    producto3 = Producto("P003", "Xiaomi Redmi Note 12", 300.00)    
    producto4 = Producto("P004", "Motorola Edge 40", 400.00)
    producto5 = Producto("P005", "Iphone 16 Pro Max", 1250.00)

    # --- Crear Factura 1 ---
    factura1 = Factura("F001", cliente1, datetime.now().strftime("%Y-%m-%d"))
    factura1.agregar_item(ItemFactura(producto1, 1))
    factura1.agregar_item(ItemFactura(producto3, 1))
    print(factura1) # Para ver la representación de la factura en consola
    print("-" * 30)

    # --- Crear Factura 2 ---
    factura2 = Factura("F002", cliente2, datetime.now().strftime("%Y-%m-%d"))
    factura2.agregar_item(ItemFactura(producto2, 2))
    factura2.agregar_item(ItemFactura(producto4, 1))
    print(factura2) #Para ver la representación de la factura en consola
    print("-" * 30)

     # --- Crear Factura 3 ---
    factura3 = Factura("F003", cliente3, datetime.now().strftime("%Y-%m-%d"))
    factura3.agregar_item(ItemFactura(producto1, 3))
    factura3.agregar_item(ItemFactura(producto4, 1))
    print(factura3) #Para ver la representación de la factura en consola
    print("-" * 30)

    # Datos para el informe de ventas
    # CORREGIDO: Se usan los precios unitarios de los objetos Producto para los datos de ventas,
    # para asegurar consistencia con los datos de los productos.
    datos_ventas ={
        producto1.descripcion: producto1.precio_unitario * 5, # 5 unidades vendidas
        producto2.descripcion: producto2.precio_unitario * 3, # 3 unidades vendidas
        producto3.descripcion: producto3.precio_unitario * 10, # 10 unidades vendidas
        producto4.descripcion: producto4.precio_unitario * 2, # 2 unidades vendidas
        producto5.descripcion: producto5.precio_unitario * 1 # 1 unidad vendida
    }

    print("DEBUG: Datos de ejemplo creados.")
    return factura1, factura2, factura3,  datos_ventas

def main():
    print("DEBUG: Iniciando función main()...")
    # Asegurarse de que la carpeta de salida exista
    output_dir = "generated_pdfs"
    print(f"DEBUG: Intentando crear directorio: {os.path.abspath(output_dir)}")
    os.makedirs(output_dir, exist_ok = True)
    print(f"DEBUG: Directorio '{output_dir}' asegurado.")

    print("Generando datos de ejemplo...")

    factura1, factura2, factura3, datos_ventas = crear_datos_ejemplo()
    
    print("\nIniciando generación de PDFs...")

    # Generar Factura 1
    print("DEBUG: Generando Factura 1...")
    pdf_factura1 = FacturaPDF(os.path.join(output_dir, "factura_F001.pdf"), factura1)
    pdf_factura1.generate()
    print("DEBUG: Factura 1 generada (o intento de).")

    # Generar Factura 2
    print("DEBUG: Generando Factura 2...")
    pdf_factura2 = FacturaPDF(os.path.join(output_dir, "factura_F002.pdf"), factura2)
    pdf_factura2.generate()
    print("DEBUG: Factura 2 generada (o intento de).")

      # Generar Factura 3
    print("DEBUG: Generando Factura 3...")
    pdf_factura3 = FacturaPDF(os.path.join(output_dir, "factura_F003.pdf"), factura3)
    pdf_factura3.generate() 
    print("DEBUG: Factura 3 generada (o intento de).")

    # Generar informe de ventas
    print("DEBUG: Generando Informe de Ventas...")
    pdf_informe_ventas = InformeVentaPDF(os.path.join(output_dir, "informe_ventas.pdf"), datos_ventas)
    pdf_informe_ventas.generate()
    print("DEBUG: Informe de Ventas generado (o intento de).")
    
    print(f"\nTodos los PDFs generados en la carpeta: {os.path.abspath(output_dir)}")
    print("DEBUG: Función main() finalizada.")

# Este es tu print de prueba final que siempre aparece
print("¡Hola! Si ves esto, la terminal y Python funcionan.")

# CORREGIDO: El bloque if __name__ == "__main__": debe estar al nivel superior (sin indentación),
# fuera de cualquier función.
if __name__ == "__main__":
    print("DEBUG: Dentro del bloque __main__.")
    main()

