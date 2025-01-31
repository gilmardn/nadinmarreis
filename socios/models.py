from django.db import models
from django.utils.timezone import now
#from django.core.validators import MinValueValidator, MaxValueValidator
#from django.db.models import Sum
#from datetime import datetime
#from django.db.models import Q

#==================================================================================
class Socio_so_ativos(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ativo=True)
    
        # socios_ativos = Socio.objects.all()    # Retorna apenas os sócios ativos
        # socios_todos = Socio._base_manager.all()  # Retorna todos os sócios, incluindo os inativos (usando o Manager padrão)
    
#==================================================================================
class Socio(models.Model):
    TIPOS_SOCIO = [('patrimonial', 'Patrimonial'), ('contribuinte', 'Contribuinte'), ('remido', 'Remido'), ('benemerito', 'Benemérito'),]
    TIPOS_ESPORTE = [ ('beachtennis', 'BeachTennis'),  ('cartas', 'Cartas'), ('futebol', 'Futebol'), ('voleibol', 'Voleibol'), ('nenhum', 'Nenhum'),]
    nome = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_admisao = models.DateField(blank=True, null=True)
    observacao = models.TextField(verbose_name="Observacões", blank=True, null=True)
    cidade = models.CharField(verbose_name= 'Cidade/Estado',max_length=50, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    cep = models.CharField(verbose_name="CEP",max_length=12, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='fotos_socios/', blank=True, null=True)
    cpf = models.CharField(verbose_name="CPF", max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField(verbose_name="RG",max_length=20, blank=True, null=True)
    tipo_socio = models.CharField(max_length=15, choices=TIPOS_SOCIO)
    esporte = models.CharField(verbose_name="Esporte Preferido", max_length=15, blank=True, null=True, choices=TIPOS_ESPORTE)
    num_titulo = models.CharField(verbose_name="Numero Titulo",max_length=3, blank=True, null=True, default='000' )

    # Manager personalizado
    objects = Socio_so_ativos()

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']
    
    
#==================================================================================
class Dependente(models.Model):
    TIPOS_PARENTESCO = [
        ('esposa', 'Esposa'), 
        ('esposo', 'Esposo'), 
        ('filha', 'Filha'), 
        ('filho', 'Filho'), 
        ('enteada', 'Enteada'), 
        ('enteado', 'Enteado'), 
        ('mae', 'Mãe'), 
        ('pai', 'Pai'), 
        ('outro', 'Outro'),]
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='dependentes')
    nome = models.CharField(verbose_name= 'Nome do dependente', max_length=100)
    parentesco = models.CharField(max_length=50, choices=TIPOS_PARENTESCO)
    data_nascimento = models.DateField()
    cpf = models.CharField(verbose_name= 'CPF', max_length=14, blank=True, null=True)
    rg = models.CharField(verbose_name= 'RG', max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_dependentes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} dependente do socio {self.socio.nome}"
    
    class Meta:
        ordering = ['nome']
    
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
        #return [meses_nome[mes] for mes in meses_nome if getattr(self, mes)]
        return [meses_nome[mes] if getattr(self, mes) else '___' for mes in meses_nome]

    def __str__(self):
        return f"{self.socio.nome, self.get_meses_pagos()}"

    

