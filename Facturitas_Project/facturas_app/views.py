from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import FileResponse
from .models import Cliente, Producto, Factura, ItemFactura
from .src.documents import FacturaPDF
from .src.models import Cliente as Cliente_Clase, Producto as Producto_Clase, ItemFactura as ItemFactura_Clase, Factura as Factura_Clase
from datetime import datetime
import os


# Create your views here.
def home(request):
    """Vista para la página de inicio del panel web."""
    return render(request, 'facturas_app/home.html')

def crear_factura(request):
    # Logica para manejar el formulario y la generacion del PDF
    if request.method == 'POST':
        #-- Logica para manejar el envio del formulario(POST)---
        try:
            #1. Recupera los datos del formulario (de django)
            cliente_id = request.POST.get('cliente')
            cliente_seleccionado = Cliente.objects.get(pk=cliente_id)

            #La fecha actual
            fecha_actual = datetime.now().strftime("%Y-%m-%d")

            #2. Guardar la nueva factura en la base de datos de django
            factura_django = Factura.objects.create(
                cliente=cliente_seleccionado,
                fecha=fecha_actual,
                total=0.00 #lo actualizaremos despues de agregar los items
            )

            #3. Recupera los items (asumiendo que vienen de forma dinamica)
            #este es un ejemplo simplificado. la logica real depende de tu formulario
            items_form = request.POST.getlist('producto_id')
            cantidades_form = request.POST.getlist('cantidad')

            #4. Crear los items en la base de datos de django y calcular el total
            total_factura = 0.0
            items_factura_clases = [] #para almacenar los items de mi clase original
            for producto_id, cantidad in zip(items_form, cantidades_form):
                producto_seleccionado = Producto.objects.get(pk=producto_id)
                cantidad = int(cantidad)

                #Crearel ItemFactura en la base de datos de django
                ItemFactura.objects.create(
                    factura=factura_django,
                    producto=producto_seleccionado,
                    cantidad=cantidad
                )

                #Crear una instancia de tu clase original para el PDF
                producto_clase = Producto_Clase(
                    id_producto=str(producto_seleccionado.id),
                    descripcion=producto_seleccionado.descripcion,
                    precio_unitario=float(producto_seleccionado.precio_unitario)
                )
                item_clase = ItemFactura_Clase(producto_clase, cantidad)
                items_factura_clases.append(item_clase)
                total_factura += item_clase.subtotal


            #5. Actualizar el total en el objeto Factura de django
            factura_django.total = total_factura
            factura_django.save()

            #6 generar el PDF usando mis clases originales
            cliente_clase = Cliente_Clase(
                id_cliente=str(cliente_seleccionado.id),
                nombre=cliente_seleccionado.nombre,
                direccion=cliente_seleccionado.direccion,
                email=cliente_seleccionado.email
            )
            factura_clase = Factura_Clase(
                id_factura=str(factura_django.id),
                cliente=cliente_clase,
                fecha=fecha_actual
            )
            for item in items_factura_clases:
                factura_clase.agregar_item(item)


            #asegurar que la carpeta de DPFs exista
            output_dir = "generated_pdfs"
            os.makedirs(output_dir, exist_ok=True)

            pdf_filename = f"factura_{factura_django.id}.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)

            factura_pdf_generator = FacturaPDF(pdf_path, factura_clase)
            factura_pdf_generator.generate()

            #7. actualizar la ruta del PDF en el modelo de Django
            factura_django.pdf_path = pdf_path
            factura_django.save()

            return redirect(reverse('ver_factura', args=[factura_django.id]))

        except Exception as e:
            #Manejar errores de forma mas elegante en un entorno real
            return render(request, 'facturas_app/error.html', {'error_message': str(e)})

    else:
        #---logica para mostrar el formulario (GET)
        clientes = Cliente.objects.all()
        productos = Producto.objects.all()

        context = {
            'clientes' : clientes,
            'productos': productos,
        }

        return render(request, 'facturas_app/crear_factura.html', context)

def ver_factura(request, pk):
    try:
        factura = Factura.objects.get(pk=pk)
        return FileResponse(open(factura.pdf_path, 'rb'), content_type='application/pdf')
    except Factura.DoesNotExist:
        return render(request, 'facturas_app/error.html', {'error_message': 'Factura no encontrada.'})
    except FileNotFoundError:
        return render(request, 'facturas_app/error.html', {'error_message': 'El archivo PDF no fue encontrado en el servidor'})