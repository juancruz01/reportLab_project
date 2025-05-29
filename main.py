from src.models import Cliente, Producto, ItemFactura, Factura
from src.documents import FacturaPDF, InformeVentaPDF
import os
from datetime import datetime

def crear_datos_ejemplo():
    """
    Crea datos de ejemplo para generar una factura y un informe de ventas.
    """
    cliente1 = Cliente("C001", "Juan Cruz", "Calle falsa 123, Claypole", "juano@gmail.com")
    cliente2 = Cliente("C002", "Leandro Herrera", "Avenida Siempre Viva 456","Alejandro Korn", "Leandro@gmail.com")

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

    #datos para el informe de ventas

    datos_ventas ={
        producto1.descripcion: 1200.00 * 5, #5 unidades vendidas
        producto2.descripcion: 650.00 * 3, #3 unidades vendidas
        producto3.descripcion: 300.00 * 10, #10 unidades vendidas
        producto4.descripcion: 400.00 * 2, #2 unidades vendidas
        producto5.descripcion: 1250.00 * 1 #1 unidad vendida
    }

    return factura1, factura2, datos_ventas

def main():
    #Asegurarse de que la carpeta de salida exista
    output_dir = "generated_pdfs"
    os.makedirs(output_dir, exist_ok = True)

    print("Generando datos de ejemplo...")
    factura1, factura2, datos_ventas = crear_datos_ejemplo()
    
    print("\nIniciando generación de PDFs...")

    #Generar Factura 1
    pdf_factura1 = FacturaPDF(os.path.join(output_dir, "factura_F001.pdf"), factura1)
    pdf_factura1.build()

    #Generar Factura 2
    pdf_factura2 = FacturaPDF(os.path.join(output_dir, "factura_F002.pdf"), factura2)
    pdf_factura2.build()

    #Generar informe de ventas
    pdf_informe_ventas = InformeVentaPDF(os.path.join(output_dir, "informe_ventas.pdf"), datos_ventas)
    pdf_informe_ventas.generate_pdf()

    print(f"\nTodos los PDFs generados en la carpeta: {output_dir}")

    if __name__ == "__main__":
        main()