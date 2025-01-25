from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from socios.models import Mensalidade, Socio
from socios.forms import AnoForm
from .models import Quadra, Horario, Caixa, Contador
from .forms import  HorarioForm, CaixaForm, CaixaFormEdit, HorarioFormEdit
from django.contrib import messages
from django.db.models import Q
from django.forms.widgets import DateInput

from django.conf import settings
LINHAS_POR_PAGINA = settings.LINHAS_POR_PAGINA

#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'livre'] 

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
    horarios = Horario.objects.all()
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
    #########################################

    def form_valid(self, form):
        # Salva o formulário e cria o objeto
        response = super().form_valid(form)
        # Adiciona uma mensagem de sucesso
        messages.success(self.request, 'Lançamento criado com sucesso!')
        return response
    
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
    #paginator = Paginator(caixas, LINHAS_POR_PAGINA)  
    #page_number = request.GET.get('page')
    #page_obj = Paginator.get_page(page_number)
    return render(request, 'financas/gerencia_financa.html', {'caixas': caixas, 'horarios': horarios })#, 'page_obj': page_obj})


#-----------------------------------------------------------------------------
def gestao_caixa(request):
    caixas = Caixa.objects.all()
    saldo_consolidado = Caixa().saldo_consolidado
    saldo_a_consolidar = Caixa().saldo_a_consolidar
    return render(request, 'financas/gestao_caixa.html', { 'caixas': caixas, 'saldo_consolidado' : saldo_consolidado, 'saldo_a_consolidar':saldo_a_consolidar})


#-----------------------------------------------------------------------------
def lista_caixa(request):
    caixas = Caixa.objects.all()
    saldo_caixa = caixas.aggregate(total=Sum('valor')).get('total', 0)
    #paginator = Paginator(caixa_list, LINHAS_POR_PAGINA) 
    #page_number = request.GET.get('page')
    #page_obj = Paginator.get_page(page_number)
    return render(request, 'financas/lista_caixa.html', { 'caixas': caixas, 'saldo_caixa' : saldo_caixa}) #'page_obj': page_obj,

#-----------------------------------------------------------------------------
def lista_horario(request):
    quadras = Quadra.objects.all()
    return render(request, 'financas/lista_horario.html', {'quadras': quadras})

#-----------------------------------------------------------------------------
def rotina_periodica(request):
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

