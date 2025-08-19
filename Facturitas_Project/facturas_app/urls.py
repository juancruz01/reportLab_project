# facturas_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crear/', views.crear_factura, name='crear_factura'),
    path('factura/<int:pk>/', views.ver_factura, name='ver_factura'),
]