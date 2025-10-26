from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=58)  
    private_key = models.TextField() 

    def __str__(self):
        return f"Wallet de {self.user.username}"

# Create your models here.
class Contacto(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='contactos')
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=58)
    mensaje = models.TextField()

    def __str__(self):
        return f"{self.nombre} - ({self.direccion}) - {self.mensaje}"