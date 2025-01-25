from django.db import models
from django.contrib.auth.models import AbstractUser

#==================================================================================
class Usuario(AbstractUser):
    ACESSOS_CHOICES = [
        ('admin', 'Administrador'),
        ('financeiro', 'Financeiro'),
        ('social', 'Social'),
        ('esportivo', 'Esportivo'),
        ('livre', 'Livre'),
    ]
    email = models.EmailField(unique=True)
    nivel_acesso = models.CharField(max_length=20, choices=ACESSOS_CHOICES, default='livre')
    

