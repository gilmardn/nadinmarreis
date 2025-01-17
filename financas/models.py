from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from django.db.models import Q
from usuarios.models import Usuario

#==================================================================================
class Categoria(models.Model):
    nome = models.CharField(max_length=50) 
    ordem = models.CharField(max_length=50, blank=True)
    class Meta:
        ordering = ['ordem']
    def __str__(self):
        return f"{self.nome}"
#==================================================================================
class Contador(models.Model):
    id_salvo = models.AutoField(primary_key=True)  # Campo autoincrementável
    data_execucao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Execução')
    observacoes = models.CharField(verbose_name='Observacões', max_length=100)

    def __str__(self):
        return   f"{self.id_salvo} - {self.data_execucao} - {self.observacoes}"
      

#==================================================================================
class Caixa(models.Model):
    TIPOS_OPERACAO = [('entrada', 'Entrada'), ('saida', 'Saida')]
    data = models.DateField()
    tipo_operacao = models.CharField(verbose_name='Tipo do operação', max_length=15, choices=TIPOS_OPERACAO)
    categoria = models.ForeignKey(Categoria, verbose_name='Categoria', on_delete=models.CASCADE)
    cliente_fornecedor = models.CharField(verbose_name='Cliente/Fornecedor', max_length=150, blank=True, default='')
    descricao = models.CharField(max_length=150, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    consolidado = models.BooleanField(default=False)
    id_consolidacao = models.IntegerField(default=0)  # Novo campo
    criado_em = models.DateTimeField(auto_now_add=True)  # Data de criação
    atualizado_em = models.DateTimeField(auto_now=True)  # Data de atualização

    class Meta:
        ordering = ['-data', '-id']

    def __str__(self):
        return f"de: ##<{self.tipo_operacao}>####<{self.valor}>####<{self.data.strftime('%d/%m/%Y')}>## "
    
    def id_formatado(self):
        return f"{self.id:05}"  # Formata o código com zeros à esquerda

    def Xfdata(self):
        return f"{self.data.strftime('%d/%m/%Y')}"
    
    @property
    def saldo_consolidado(self):
        entrada = Caixa.objects.filter(Q(tipo_operacao='entrada') & Q(consolidado=True)).aggregate(total=models.Sum('valor'))['total'] or 0
        saida = Caixa.objects.filter(Q(tipo_operacao='saida') & Q(consolidado=True)).aggregate(total=models.Sum('valor'))['total'] or 0
        z = entrada - saida
        return f"{z:,.2f}"
    @property
    def saldo_a_consolidar(self):
        entrada = Caixa.objects.filter(Q(tipo_operacao='entrada') & Q(consolidado=False)).aggregate(total=models.Sum('valor'))['total'] or 0
        saida = Caixa.objects.filter(Q(tipo_operacao='saida') & Q(consolidado=False)).aggregate(total=models.Sum('valor'))['total'] or 0
        z = entrada - saida
        return f"{z:,.2f}"
    
#==========================  Finanças ============================================
class Quadra(models.Model):
    nome = models.CharField(max_length=20)  # Voleibol 1 ou Voleibol 2
    descricao = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.nome

#==================================================================================
class Horario(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)
    responsavel = models.CharField(verbose_name='Responsavel', max_length=100)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    def __str__(self):
        return f" <<< {self.quadra.nome} >>>  Dia {self.data.strftime('%d/%m/%y')}  das  {self.hora_inicio.strftime('%H:%M')} as  {self.hora_fim.strftime('%H:%M')} horas"
    def Xfdata(self):
        return f"{self.data.strftime('%d/%m/%Y')}"
    def Xfhora_inicio(self):
        return f'{self.hora_inicio.strftime("%H:%M")}'
    def Xfhora_fim(self):
        return f'{self.hora_fim.strftime("%H:%M")}'


    
    
