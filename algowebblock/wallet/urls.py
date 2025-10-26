from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_balance/', views.get_balance, name='get_balance'),
    path('info/', views.info, name='info'),
    path('envios/', views.envios, name='envios'),

    # Nuevas rutas para contactos
    path('contactos/', views.mis_contactos, name='mis_contactos'),
    path('contactos/agregar/', views.agregar_contacto, name='agregar_contacto'),
]