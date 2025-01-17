from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from datetime import datetime
from django.db.models import Q

#==================================================================================
class Socio(models.Model):
    TIPOS_SOCIO = [('remido', 'Remido'), ('patrimonial', 'Patrimonial'), ('benemerito', 'Benemérito'),('contribuinte', 'Contribuinte'),]
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_admisao = models.DateField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(verbose_name="CEP",max_length=9, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='fotos_socios/', blank=True, null=True)
    cpf = models.CharField(verbose_name="CPF", max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField(verbose_name="RG",max_length=20, blank=True, null=True)
    tipo_socio = models.CharField(max_length=15, choices=TIPOS_SOCIO)
    

    def __str__(self):
        return self.nome
    
#==================================================================================
class Dependente(models.Model):
    TIPOS_PARENTESCO = [('conjuge', 'Conjuge'), ('filho', 'Filho(a)'), ('enteado', 'Enteado(a)'), ('sobrinho', 'Sobrinho(a)'), ('outro', 'Outro'),]
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='dependentes')
    nome = models.CharField(verbose_name= 'Nome do dependente', max_length=100)
    parentesco = models.CharField(max_length=50, choices=TIPOS_PARENTESCO)
    data_nascimento = models.DateField()
    cpf = models.CharField(verbose_name= 'CPF', max_length=14, blank=True, null=True)
    rg = models.CharField(verbose_name= 'RG', max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_dependentes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} dependente do socio {self.socio.nome}"
    
#==================================================================================
class Mensalidade(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='mensalidades')
    ano = models.IntegerField(verbose_name="Mensalidade do ano", default=now().year)
    jan = models.BooleanField(default=False)
    fev = models.BooleanField(default=False)
    mar = models.BooleanField(default=False)
    abr = models.BooleanField(default=False)
    mai = models.BooleanField(default=False)
    jun = models.BooleanField(default=False)
    jul = models.BooleanField(default=False)
    ago = models.BooleanField(default=False)
    set = models.BooleanField(default=False)
    out = models.BooleanField(default=False)
    nov = models.BooleanField(default=False)
    dez = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, null=True)
   
    class Meta:
        unique_together = ('socio', 'ano')
        ordering = ['socio', 'ano']

    def get_meses_pagos(self):
        # Nome completo dos meses para exibição
        meses_nome = {'jan': 'Jan', 'fev': 'Fev', 'mar': 'Mar', 'abr': 'Abr', 'mai': 'Mai', 'jun': 'Jun',
                    'jul': 'Jul', 'ago': 'Ago', 'set': 'Set', 'out': 'Out', 'nov': 'Nov','dez': 'Dez',
        }

        # Retorna os nomes dos meses pagos
        return [meses_nome[mes] for mes in meses_nome if getattr(self, mes)]

    def __str__(self):
        return f"{self.socio.nome, self.get_meses_pagos}"

    

