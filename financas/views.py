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

from django.urls import path



from django.conf import settings
LINHAS_POR_PAGINA = settings.LINHAS_POR_PAGINA

#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 

#-----------------------------------------------------------------------------
class DatePickerInput(DateInput):
    input_type = 'date'

#-----------------------------------------------------------------------------
class HorarioListView(ListView):
    model = Horario
    template_name = 'financas/horario_list.html'

#-----------------------------------------------------------------------------
class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'financas/horario_form.html'
    success_url = reverse_lazy('gestao_horario')
    #####  ROTINA DE PERMISSOES  #######
    def dispatch(self, request, *args, **kwargs):
        niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo'] 
        if not request.user.is_authenticated:
            messages.error(request, "Você não está logado.")
            return redirect('home')  
        if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
            messages.warning(request, "Você não tem permissão para acessar esta página.")
            return redirect('home') 
        # Se o usuário tiver permissão, continua com a execução normal da view
        return super().dispatch(request, *args, **kwargs)
    
    #####  MENSAGEM DE SUCESSO AO SALVAR #####
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Horário salvo com sucesso!")
        return response

    #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
    def form_invalid(self, form):
        messages.error(self.request, "Erro ao salvar o horário.")
        return super().form_invalid(form)
    #########################################

#-----------------------------------------------------------------------------
class HorarioUpdateView(UpdateView):
    model = Horario
    form_class = HorarioFormEdit
    template_name = 'financas/horario_form.html'
    success_url = reverse_lazy('gestao_horario')
    #####  ROTINA DE PERMISSOES  #######
    def dispatch(self, request, *args, **kwargs):
        niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo'] 
        if not request.user.is_authenticated:
            messages.error(request, "Você não está logado.")
            return redirect('home')  
        if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
            messages.warning(request, "Você não tem permissão para acessar esta página.")
            return redirect('home') 
        # Se o usuário tiver permissão, continua com a execução normal da view
        return super().dispatch(request, *args, **kwargs)
    #########################################

    #####  MENSAGEM DE SUCESSO AO SALVAR #####
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Horário salvo com sucesso!")
        return response

    #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
    def form_invalid(self, form):
        messages.error(self.request, "Erro ao salvar o horário.")
        return super().form_invalid(form)
    #########################################
 
#-----------------------------------------------------------------------------
class HorarioDeleteView(DeleteView):
    model = Horario
    template_name = 'financas/horario_confirm_delete.html'
    success_url = reverse_lazy('gestao_horario')
    #####  ROTINA DE PERMISSOES  #######
    def dispatch(self, request, *args, **kwargs):
        niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo'] 
        if not request.user.is_authenticated:
            messages.error(request, "Você não está logado.")
            return redirect('home')  
        if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
            messages.warning(request, "Você não tem permissão para acessar esta página.")
            return redirect('home') 
        # Se o usuário tiver permissão, continua com a execução normal da view
        return super().dispatch(request, *args, **kwargs)
    #########################################

#-----------------------------------------------------------------------------
def gestao_horario(request):
    horarios = Horario.objects.filter(data__gte=timezone.now().date()).order_by('data')
    return render(request, 'financas/gestao_horario.html', { 'horarios': horarios})

#-----------------------------------------------------------------------------
class CaixaListView(ListView):
    model = Caixa
    template_name = 'financas/caixa_list.html'

#-----------------------------------------------------------------------------
class CaixaCreateView(CreateView):
    model = Caixa
    form_class = CaixaForm
    template_name = 'financas/caixa_form.html'
    success_url = reverse_lazy('caixa-create')
    #####  ROTINA DE PERMISSOES  #######
    def dispatch(self, request, *args, **kwargs):
        niveis_permitidos = ['admin', 'financeiro'] 
        if not request.user.is_authenticated:
            messages.error(request, "Você não está logado.")
            return redirect('home')  
        if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
            messages.warning(request, "Você não tem permissão para acessar esta página.")
            return redirect('home') 
        # Se o usuário tiver permissão, continua com a execução normal da view
        return super().dispatch(request, *args, **kwargs)
    
    #####  MENSAGEM DE SUCESSO AO SALVAR #####
    def form_valid(self, form):
        # Salva o formulário e cria o objeto
        response = super().form_valid(form)
        # Adiciona uma mensagem de sucesso
        messages.success(self.request, 'Lançamento criado com sucesso!')
        return response
    
    #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
    def form_invalid(self, form):
        messages.error(self.request, "Erro ao salvar o horário. Verifique os dados e tente novamente.")
        return super().form_invalid(form)
    
#-----------------------------------------------------------------------------
class CaixaUpdateView(UpdateView):
    model = Caixa
    form_class = CaixaFormEdit
    template_name = 'financas/caixa_form.html'
    success_url = reverse_lazy('gestao_caixa')
    #####  ROTINA DE PERMISSOES  #######
    def dispatch(self, request, *args, **kwargs):
        niveis_permitidos = ['admin', 'financeiro'] 
        if not request.user.is_authenticated:
            messages.error(request, "Você não está logado.")
            return redirect('home')  
        if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
            messages.warning(request, "Você não tem permissão para acessar esta página.")
            return redirect('home') 
        # Se o usuário tiver permissão, continua com a execução normal da view
        return super().dispatch(request, *args, **kwargs)
    #########################################

    def form_valid(self, form):
        # Salva o formulário e cria o objeto
        response = super().form_valid(form)
        # Adiciona uma mensagem de sucesso
        messages.success(self.request, 'Lançamento criado com sucesso!')
        return response
    
    #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
    def form_invalid(self, form):
        messages.error(self.request, "Erro ao salvar o horário. Verifique os dados e tente novamente.")
        return super().form_invalid(form)
    

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(consolidado=False)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.consolidado:
            # messages.warning(request, "Esta entrada não pode ser editada porque ja foi Consolidada.")
            return redirect('gerencia_financa')
        return super().get(request, *args, **kwargs)

#-----------------------------------------------------------------------------
class CaixaDeleteView(DeleteView):
    model = Caixa
    template_name = 'financas/caixa_confirm_delete.html'
    success_url = reverse_lazy('gestao_caixa')

    #####  ROTINA DE PERMISSOES  #######
    def dispatch(self, request, *args, **kwargs):
        niveis_permitidos = ['admin', 'financeiro'] 
        if not request.user.is_authenticated:
            messages.error(request, "Você não está logado.")
            return redirect('home')  
        if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
            messages.warning(request, "Você não tem permissão para acessar esta página.")
            return redirect('home') 
        # Se o usuário tiver permissão, continua com a execução normal da view
        return super().dispatch(request, *args, **kwargs)
    #########################################

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(consolidado=False)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.consolidado:
            # messages.warning(request, "Esta entrada não pode ser editada porque foi Consolidada.")
            return redirect('gerencia_financa')
        return super().post(request, *args, **kwargs)

#-----------------------------------------------------------------------------
def gerencia_financa(request):
    horarios = Horario.objects.all()
    caixas = Caixa.objects.all()
    paginator = Paginator(caixas, LINHAS_POR_PAGINA)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'financas/gerencia_financa.html', {'caixas': caixas, 'horarios': horarios, 'page_obj': page_obj })#, 'page_obj': page_obj})


#-----------------------------------------------------------------------------
def gestao_caixa(request):
    caixas = Caixa.objects.all().order_by('-data')
    saldo_consolidado = Caixa().saldo_consolidado
    saldo_a_consolidar = Caixa().saldo_a_consolidar
    paginator = Paginator(caixas, LINHAS_POR_PAGINA)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'financas/gestao_caixa.html', { 'caixas': caixas, 'saldo_consolidado' : saldo_consolidado, 'saldo_a_consolidar':saldo_a_consolidar, 'page_obj': page_obj})


#-----------------------------------------------------------------------------
def lista_caixa(request):
    caixas = Caixa.objects.all().order_by('-data')
    saldo_caixa = caixas.aggregate(total=Sum('valor')).get('total', 0)
    paginator = Paginator(caixas, LINHAS_POR_PAGINA) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'financas/lista_caixa.html', { 'caixas': caixas, 'saldo_caixa' : saldo_caixa, 'page_obj': page_obj}) #'page_obj': page_obj,

#-----------------------------------------------------------------------------
def lista_horario(request):
    quadras = Quadra.objects.all()
    return render(request, 'financas/lista_horario.html', {'quadras': quadras})



#============================= CRUD PARCEIROS =============================
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
class ParceiroCreateView(CreateView):
    model = Parceiro
    form_class = ParceiroForm
    template_name = 'financas/parceiro_form.html'
    success_url = reverse_lazy('gestao_parceiro')

#=================================================================================    
class ParceiroUpdateView(UpdateView):
    model = Parceiro
    form_class = ParceiroForm
    template_name = 'financas/parceiro_form.html'
    success_url = reverse_lazy('gestao_parceiro')

    def get_queryset(self):
        #return Parceiro.objects.all()  # Retorna so os ativos = True
        return Parceiro._base_manager.all() # Garante que todos os parceiros sejam listados ativos e inativos

#=================================================================================    
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
def importa_socios_para_parceiros(request):
    if request.method == 'POST':
        # Filtra sócios ativos
        socios_ativos = Socio.objects.filter(ativo=True)

        # Contador de sócios importados
        count = 0

        for socio in socios_ativos:
            # Verifica se o sócio já existe na tabela de parceiros pelo CPF
            if not Parceiro.objects.filter(nome=socio.nome).exists():
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

        # Exibe uma mensagem de sucesso
        messages.success(request, f'{count} sócios foram importados para a tabela de parceiros.')

    # Redireciona de volta para a página do admin
    form = AnoForm()
    return render(request, 'financas/rotina_periodica.html', {'form': form})


#-----------------------------------------------------------------------------
def consolidar_registros(request):
    #####  ROTINA DE PERMISSOES  #######
    niveis_permitidos = ['admin', 'financeiro'] 
    if not request.user.is_authenticated:
        messages.error(request, "Você não está logado.")
        return redirect('home')  
    if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
        messages.warning(request, "Você não tem permissão para acessar esta página.")
        return redirect('home') 
    # Se o usuário tiver permissão, continua com a execução normal da view
    #########################################
    contador = Contador(observacoes= 'xxxxxxxxxxx')
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
def rotina_periodica(request):  # CRIA MENSALIDADE PARA ASSOCIADOS NOVOS
    #####  ROTINA DE PERMISSOES  #######
    niveis_permitidos = ['admin', 'financeiro'] 
    if not request.user.is_authenticated:
        messages.error(request, "Você não está logado.")
        return redirect('home')  
    if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
        messages.warning(request, "Você não tem permissão para acessar esta página.")
        return redirect('home') 
    # Se o usuário tiver permissão, continua com a execução normal da view
    #########################################
    registros_criados = 0
    ano = None
    if request.method == 'POST':
        form = AnoForm(request.POST)
        if form.is_valid():
            ano = form.cleaned_data['ano']
            # Filtra sócios que são 'patrimonial' ou 'contribuinte'
            socios = Socio.objects.filter(Q(tipo_socio='patrimonial') | Q(tipo_socio='contribuinte'))
            for socio in socios:
                # Verifica se já existe uma mensalidade para o sócio no ano especificado
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

