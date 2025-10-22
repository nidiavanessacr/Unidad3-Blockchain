from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_balance/', views.get_balance, name='get_balance'),
    path('info/', views.info, name='info'),
    path('envios/', views.envios, name='envios'),
]