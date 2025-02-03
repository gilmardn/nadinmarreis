from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from socios.models import Mensalidade, Socio
from socios.forms import AnoForm
from .models import Quadra, Horario, Caixa, Contador, Parceiro
from .forms import HorarioForm, CaixaForm, CaixaFormEdit, HorarioFormEdit, ParceiroForm
from django.contrib import messages
from django.db.models import Q
from django.forms.widgets import DateInput
from django.utils import timezone
from datetime import datetime
from django.utils.decorators import method_decorator
from utils.decorators import permissoes_requeridas
from django.conf import settings


LINHAS_POR_PAGINA = int(settings.LINHAS_POR_PAGINA)

if LINHAS_POR_PAGINA is None:
    LINHAS_POR_PAGINA = 10  # ou outro valor padrão



#-----------------------------------------------------------------------------
class DatePickerInput(DateInput):
    input_type = 'date'

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico']), name='dispatch')
class HorarioListView(ListView):
    model = Horario
    template_name = 'financas/horario_list.html'

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo']), name='dispatch')
class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'financas/horario_form.html'
    success_url = reverse_lazy('gestao_horario')
 
    def form_valid(self, form): #####  MENSAGEM DE SUCESSO DO FORMULÁRIO VÁLIDO #####
        response = super().form_valid(form)
        messages.success(self.request, "Horário salvo com sucesso!")
        return response

    def form_invalid(self, form): #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
        messages.error(self.request, "Erro ao salvar o horário.")
        return super().form_invalid(form)

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo']), name='dispatch')
class HorarioUpdateView(UpdateView):
    model = Horario
    form_class = HorarioFormEdit
    template_name = 'financas/horario_form.html'
    success_url = reverse_lazy('gestao_horario')

    def form_valid(self, form): #####  MENSAGEM DE SUCESSO AO SALVAR #####
        response = super().form_valid(form)
        messages.success(self.request, "Horário salvo com sucesso!")
        return response

    def form_invalid(self, form): #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
        messages.error(self.request, "Erro ao salvar o horário.")
        return super().form_invalid(form)
 
#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo']), name='dispatch')
class HorarioDeleteView(DeleteView):
    model = Horario
    template_name = 'financas/horario_confirm_delete.html'
    success_url = reverse_lazy('gestao_horario')

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def gestao_horario(request):
    horarios = Horario.objects.filter(data__gte=timezone.now().date()).order_by('data')
    return render(request, 'financas/gestao_horario.html', { 'horarios': horarios})

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class CaixaListView(ListView):
    model = Caixa
    template_name = 'financas/caixa_list.html'

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class CaixaCreateView(CreateView):
    model = Caixa
    form_class = CaixaForm
    template_name = 'financas/caixa_form.html'
    success_url = reverse_lazy('caixa-create')

    def form_valid(self, form):  #####  MENSAGEM DE SUCESSO AO SALVAR #####
        # Salva o formulário e cria o objeto
        response = super().form_valid(form)
        # Adiciona uma mensagem de sucesso
        messages.success(self.request, 'Lançamento criado com sucesso!')
        return response
    
    def form_invalid(self, form):  #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
        messages.error(self.request, "Erro ao salvar o horário. Verifique os dados e tente novamente.")
        return super().form_invalid(form)
    
#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class CaixaUpdateView(UpdateView):
    model = Caixa
    form_class = CaixaFormEdit
    template_name = 'financas/caixa_form.html'
    success_url = reverse_lazy('gestao_caixa')
 
    def form_valid(self, form):   # Salva o formulário e cria o objeto
        response = super().form_valid(form) 
        messages.success(self.request, 'Lançamento criado com sucesso!')
        return response
    
    def form_invalid(self, form): #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
        messages.error(self.request, "Erro ao salvar o horário. Verifique os dados e tente novamente.")
        return super().form_invalid(form)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(consolidado=False)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.consolidado:
            messages.warning(request, "Esta entrada não pode ser editada porque ja foi Consolidada.")
            return redirect('gerencia_financa')
        return super().get(request, *args, **kwargs)

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class CaixaDeleteView(DeleteView):
    model = Caixa
    template_name = 'financas/caixa_confirm_delete.html'
    success_url = reverse_lazy('gestao_caixa')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(consolidado=False)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.consolidado:
            messages.warning(request, "Esta entrada não pode ser editada porque foi Consolidada.")
            return redirect('gerencia_financa')
        return super().post(request, *args, **kwargs)

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro'])
def gerencia_financa(request):
    horarios = Horario.objects.all().order_by('-data')
    caixas = Caixa.objects.all().order_by('-data')
    saldo_consolidado = Caixa().saldo_consolidado  # Retorna um número
    saldo_a_consolidar = Caixa().saldo_a_consolidar  # Retorna um número
    saldo_atual = float(saldo_consolidado) + float(saldo_a_consolidar)

    paginator = Paginator(caixas, LINHAS_POR_PAGINA)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    paginator_1 = Paginator(horarios, LINHAS_POR_PAGINA)
    page_number_1 = request.GET.get('page')
    page_obj_1 = paginator_1.get_page(page_number_1)

    context = {
        'page_obj': page_obj,
        'saldo_atual': f"{saldo_atual:,.2f}",  # Passa o saldo atual como número
        'page_obj_1': page_obj_1,
    }

    return render(request, 'financas/gerencia_financa.html', context)
#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro'])
def gestao_caixa(request):
    # Obtém todos os objetos Caixa ordenados por data (do mais recente para o mais antigo)
    caixas = Caixa.objects.all().order_by('-data')
    saldo_consolidado = Caixa().saldo_consolidado
    saldo_a_consolidar = Caixa().saldo_a_consolidar
    paginator = Paginator(caixas, LINHAS_POR_PAGINA)
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Obtém os objetos da página atual
    context = {
        'page_obj': page_obj,  # Passa o objeto de paginação
        'saldo_consolidado': saldo_consolidado,
        'saldo_a_consolidar': saldo_a_consolidar
    }

    return render(request, 'financas/gestao_caixa.html', context)

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def lista_caixa(request):
    caixas = Caixa.objects.all().order_by('-data')
    saldo_caixa = caixas.aggregate(total=Sum('valor')).get('total', 0)
    paginator = Paginator(caixas, LINHAS_POR_PAGINA) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'financas/lista_caixa.html', { 'caixas': caixas, 'saldo_caixa' : saldo_caixa, 'page_obj': page_obj}) #'page_obj': page_obj,

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
#@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def lista_horario(request):
    quadras = Quadra.objects.all()
    return render(request, 'financas/lista_horario.html', {'quadras': quadras})

#============================= CRUD PARCEIROS =============================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class ParceiroListView(ListView):
    model = Parceiro
    template_name = 'financas/gestao_parceiro.html'
    context_object_name = 'parceiros'

    def get_queryset(self):
        query = self.request.GET.get('q')  # Pega o parâmetro de busca da URL
        parceiros = Parceiro._base_manager.all() # Garante que todos os parceiros sejam listados ativos e inativos
        if query:  # Se a query estiver presente, aplica o filtro
            parceiros = parceiros.filter(nome__icontains=query)
        return parceiros
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parceiros = context[self.context_object_name]  # Pega os parceiros do contexto
        paginator = Paginator(parceiros, LINHAS_POR_PAGINA)  # Aqui você pode definir o número de itens por página
        page_number = self.request.GET.get('page')  # Pega o número da página da URL
        page_obj = paginator.get_page(page_number)  # Obtém a página atual
        context = {'parceiros':page_obj.object_list ,  'page_obj': page_obj}
        return context
    
#=================================================================================    
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class ParceiroCreateView(CreateView):
    model = Parceiro
    form_class = ParceiroForm
    template_name = 'financas/parceiro_form.html'
    success_url = reverse_lazy('gestao_parceiro')

#=================================================================================    
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class ParceiroUpdateView(UpdateView):
    model = Parceiro
    form_class = ParceiroForm
    template_name = 'financas/parceiro_form.html'
    success_url = reverse_lazy('gestao_parceiro')

    def get_queryset(self):
        #return Parceiro.objects.all()  # Retorna so os ativos = True
        return Parceiro._base_manager.all() # Garante que todos os parceiros sejam listados ativos e inativos

#=================================================================================    
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro']), name='dispatch')
class ParceiroDeleteView(DeleteView):
    model = Parceiro
    template_name = 'financas/parceiro_confirm_delete.html'
    success_url = reverse_lazy('gestao_parceiro')

    def get_queryset(self):
        #return Parceiro.objects.all()  # Retorna so os ativos = True
        return Parceiro._base_manager.all() # Garante que todos os parceiros sejam listados ativos e inativos


#=================================================================================    
#=====================  Rotinas Periodicas======================================   
#=================================================================================   


#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin'])
def importa_socios_para_parceiros(request):
    if request.method == 'POST':
        socios_ativos = Socio.objects.filter(ativo=True)  # Filtra sócios ativos
        count = 0  # Contador de sócios importados

        for socio in socios_ativos:
            
            if not Parceiro.objects.filter(nome=socio.nome).exists():  # Verifica se o sócio já existe na tabela de parceiros pelo nome
                # Cria um novo parceiro com os dados do sócio
                Parceiro.objects.create(
                    nome=socio.nome,
                    email=socio.email,
                    telefone=socio.telefone,
                    cidade=socio.cidade,
                    endereco=socio.endereco,
                    cep=socio.cep,
                    ativo=socio.ativo,
                    cpf_cnpj=socio.cpf,
                    ie=""  # Inscrição Estadual vazia, como solicitado
                )
                count += 1
        messages.success(request, f'{count} sócios foram importados para a tabela de parceiros.')

    form = AnoForm()  # Redireciona de volta para a página
    return render(request, 'financas/rotina_periodica.html', {'form': form})


#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro'])
def consolidar_registros(request):

    agora = datetime.now()
    data_formatada = agora.strftime('%d/%m/%Y')  # Formato: dia/mês/ano
    hora_formatada = agora.strftime('%H:%M:%S')  # Formato: horas:minutos:segundos
    texto = f"Registros consolidados em {data_formatada} as {hora_formatada}"
   
    contador = Contador(observacoes= texto)
    contador.save()
    proximo_numero = contador.id_salvo
    
    if request.method == 'POST':
        consolidados = Caixa.objects.filter(consolidado=False)
        total = consolidados.count()
        consolidados.update(consolidado=True, id_consolidacao=proximo_numero)
        messages.success(request, f'{total} registros consolidados.')
    else:
        messages.error(request, 'Ocorreu um erro ao processar o formulário. Verifique os dados e tente novamente.')

    form = AnoForm()
    return render(request, 'financas/rotina_periodica.html', {'form': form})

#-----------------------------------------------------------------------------
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro' , 'social'])
def rotina_periodica(request):  # CRIA MENSALIDADE PARA ASSOCIADOS NOVOS
    registros_criados = 0
    ano = None
    if request.method == 'POST':
        form = AnoForm(request.POST)
        if form.is_valid():
            ano = form.cleaned_data['ano']  # Filtra sócios que são 'patrimonial' ou 'contribuinte'
            socios = Socio.objects.filter(Q(tipo_socio='patrimonial') | Q(tipo_socio='contribuinte'))
            for socio in socios:   # Verifica se já existe uma mensalidade para o sócio no ano especificado
                if not Mensalidade.objects.filter(socio=socio, ano=ano).exists():
                    Mensalidade.objects.create(socio=socio, ano=ano)
                    registros_criados += 1
            
            messages.success(request, f'{registros_criados} mensalidades criadas para o ano {ano}.')
            return redirect('rotina_periodica')
        else:
            messages.error(request, 'Ocorreu um erro ao processar o formulário. Verifique os dados e tente novamente.')
    else:
        form = AnoForm()
    return render(request, 'financas/rotina_periodica.html', {'form': form})

