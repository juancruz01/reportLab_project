from reportlab.platypus import SimpleDocTemplate, paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

from src.Models import Factura, Cliente #Importamos nuestras clases de modelo

class DocumentoPDF:
    """
    clase abstracta para todos nuestros documentos PDF.
    Aplica Abstraccion: Oculta la complejidad de la inicializacion de Reportlab.
    Aplica Herencia: proporciona metodos comunes para la creacion de PDFs.
    """

    def __init__(self, filename: str, title: str):
        self.filename = filename
        self.title = title
        self.doc = SimpleDocTemplate(filename, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = [] #Lista para almacenar los elementos del documento

    def _add_header(self):
        #añade un encabezado comun a todos los documentos.
        self.story.append(paragraph(self.title, self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

    def _build_content(self):
        """
        implementacion especifica para la cracion del contenido de una factura.
        """

        #informacion del cliente
        self.story.append(paragraph("Datos del Cliente", self.styles['h3']))
        self.story.append(paragraph(f"nombre: {self.factura.cliente.nombre}", self.styles['Normal']))
        self.story.append(paragraph(f"Direccion: {self.factura.cliente.direccion}", self.styles['Normal']))
        self.story.append(paragraph(f"Email: {self.factura.cliente.email}", self.styles['Normal']))
        self.story.append(Spacer(1, 0.2 * inch))

        #detalles de la factura
        self.story.append(paragraph("Detalle de Items:", self.styles['h3']))
        data = [['Descripcion', 'Cantidad', 'Precio Unitario', 'Subtotal']]

        for item in self.factura.items:
            data.append([
                item.producto.descripcion,
                str(item.cantidad),
                f"${item.producto.precio_unitario:.2f}",
                f"{item.subtotal:.2f}"
            ])

        #Fila para el total

        data.append(['', '', 'Total:' f"${self.factura.total:.2f}"])

        table_style = TableStyle([
            ('BACKGROUND' , (0, 0), (-1, 0), colors.HexColor('F0F0F0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALING', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1 ,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1) )
        ])