# src/documents.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet # CORREGIDO: Eliminado 'Style' extra
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

from src.models import Factura, Cliente, Producto, ItemFactura 

class DocumentoPDF:
    """
    Clase abstracta para todos nuestros documentos PDF.
    Aplica Abstraccion: Oculta la complejidad de la inicializacion de Reportlab.
    Aplica Herencia: proporciona metodos comunes para la creacion de PDFs.
    """

    def __init__(self, filename: str, title: str):
        self.filename = filename
        self.title = title
        self.doc = SimpleDocTemplate(filename, pagesize=letter)
        # CORREGIDO: getSampleStyleSheet() - Un solo 'Style'
        self.styles = getSampleStyleSheet() 
        self.story = [] # Lista para almacenar los elementos del documento

    def _add_header(self):
        # Añade un encabezado comun a todos los documentos.
        self.story.append(Paragraph(self.title, self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

    def _build_content(self):
        """
        Método abstracto que debe ser implementado por las subclases.
        Aplica Polimorfismo: Cada subclase implementará este método de forma diferente
                             para generar su contenido específico.
        """
        raise NotImplementedError("Este metodo debe ser implementado por las subclases.")
    
    def generate(self):
        # Genera el documento PDF COMPLETO.
        self._add_header()

        # para que la subclase agregue su contenido a self.story antes de build.
        self._build_content() 
        try:
            self.doc.build(self.story)
            print(f"DEBUG: Documento '{self.filename}' generado exitosamente.") # Mensaje de depuración
        except Exception as e:
            print(f"ERROR: Falló al generar el documento: '{self.filename}': {e}") # Mensaje de error
            import traceback
            traceback.print_exc() # Esto imprimirá la traza completa del error


class FacturaPDF(DocumentoPDF):
    """
    Generador de documentos PDF para facturas.
    Hereda de DocumentoPDF.
    Aplica Polimorfismo: Implementa _build_content de forma especifica para facturas.
    """
    def __init__(self, filename: str, factura: Factura):
        super().__init__(filename, f"Factura #{factura.id_factura}")
        if not isinstance(factura, Factura):
            raise TypeError("El objeto 'factura' debe ser una instancia de la clase Factura.")
        self.factura = factura # Almacena la factura para generar el PDF
        
    def _build_content(self):
        """
        Implementacion especifica para la creacion del contenido de una factura.
        """
        # Informacion del cliente
        self.story.append(Paragraph("Datos del Cliente", self.styles['h3']))
        self.story.append(Paragraph(f"Nombre: {self.factura.cliente.nombre}", self.styles['Normal']))
        self.story.append(Paragraph(f"Direccion: {self.factura.cliente.direccion}", self.styles['Normal']))
        self.story.append(Paragraph(f"Email: {self.factura.cliente.email}", self.styles['Normal']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Detalles de la factura
        self.story.append(Paragraph("Detalle de Items:", self.styles['h3']))
        data = [['Descripcion', 'Cantidad', 'Precio Unitario', 'Subtotal']]

        # Detalles de los items
        for item in self.factura.items:
            data.append([
                item.producto.descripcion,
                str(item.cantidad),
                f"${item.producto.precio_unitario:.2f}",
                f"${item.subtotal:.2f}"
            ])

        # Fila para el total
        data.append(['', '', 'Total:', f"${self.factura.total:.2f}"])

        table_style = TableStyle([
            # Se mantiene tu color '#ff1a1a'
            ('BACKGROUND' , (0, 0), (-1, 0), colors.HexColor('#ff1a1a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'), 
            ('FONTNAME', (0, 0), (-1 ,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            # CORREGIDO: Ajuste de ALIGN para la columna del total (era (2,-1) a (-1,-1), ahora (3,-1) a (3,-1) para la 4ta columna)
            ('ALIGN', (3, -1), (3, -1), 'RIGHT'), 
            ('FONTNAME', (2, -1), (3, -1), 'Helvetica-Bold'), # Total en negrita
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E0E0E0')), # Fondo para la fila del total
        ])

        table = Table(data, colWidths=[3*inch, 0.8*inch, 1*inch, 1*inch]) 
        table.setStyle(table_style)
        self.story.append(table)
        self.story.append(Spacer(1,0.5 * inch))
        self.story.append(Paragraph("Gracias por su compra!", self.styles['Normal']))

# CORREGIDO: InformeVentaPDF a InformeVentasPDF (para consistencia con el import en main.py)
class InformeVentaPDF(DocumentoPDF): 
    """
    Generador de documentos PDF para informes de ventas con graficos.
    Hereda de DocumentoPDF.
    Aplica Polimorfismo: Implementa _build_content de forma especifica para informes de ventas
    """

    def __init__(self, filename: str, data: dict, title: str = "Informe de Ventas"):
        super().__init__(filename, title)
        self.data = data # datos para el informe, ej: {'Producto A: 150, 'Producto B': 200} 

    def _build_content(self):
        self.story.append(Paragraph("Resumen de Ventas por Producto", self.styles['h3']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Crear tabla de resumen
        table_data = [['Producto', 'Ventas']]
        for producto, ventas in self.data.items():
            table_data.append([producto, f"${ventas:.2f}"])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D3D3D3')),
            ('TEXTCOLOR',(0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8), 
            ('GRID', (0, 0 ), (-1, -1), 1, colors.grey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'), # Alinea ventas a la derecha
        ])

        ventas_table = Table(table_data, colWidths=[2.5*inch, 1.5*inch])
        ventas_table.setStyle(table_style)
        self.story.append(ventas_table)
        self.story.append(Spacer(1,0.5 * inch))

        # Crear grafico de barras simple
        drawing = Drawing(400, 200) # Ancho y alto del dibujo
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [tuple(self.data.values())] # los datos deben ser una lista de tuplas
        chart.groupSpacing = 10
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(self.data.values()) * 1.2 # un poco mas arriba que el maximo
        chart.categoryAxis.labels.boxAnchor = 'ne' # centra las etiquetas en el eje x
        chart.categoryAxis.labels.dx = 8 # desplaza las etiquetas a la derecha
        chart.categoryAxis.labels.dy = -2
        chart.categoryAxis.categoryNames = list(self.data.keys()) # nombres de las categorias

        drawing.add(chart)
        self.story.append(drawing)
        self.story.append(Spacer(1, 0.6 * inch))
        self.story.append(Paragraph("Este grafico muestra las ventas acumuladas por producto.", self.styles['Italic']))