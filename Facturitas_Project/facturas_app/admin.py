from django.contrib import admin
from .models import Cliente, Producto, Factura, ItemFactura

# Registrar tus modelos aquí.
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Factura)
admin.site.register(ItemFactura)