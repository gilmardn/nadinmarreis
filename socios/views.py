from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Socio, Dependente, Mensalidade # ,Pagamento, 
from .forms import SocioForm, DependenteForm, MensalidadeForm, SocioFormEdit, DependenteFormEdit
from django.views.generic import  UpdateView, DeleteView # ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from utils.decorators import permissoes_requeridas
from django.contrib.auth.decorators import login_required

from django.conf import settings
LINHAS_POR_PAGINA = int(settings.LINHAS_POR_PAGINA)

#==============================================================
#@login_required
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
#@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def home(request):
    return render(request, 'socios/home.html')

#====================================================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def lista_mensalidades(request):
    query = request.GET.get('q') 
    socios = Socio.objects.filter(tipo_socio__in=['patrimonial', 'contribuinte']).prefetch_related('mensalidades')
    if query: 
       socios = socios.filter(nome__icontains=query) 
    paginator = Paginator(socios, LINHAS_POR_PAGINA - 4)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Passa o objeto de paginação
        'query': query  # Passa a consulta para exibir no template
    }
    return render(request, 'socios/lista_mensalidades.html', context)

#====================================================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social']), name='dispatch')
class MensalidadeUpdateView(UpdateView):
    model = Mensalidade
    form_class = MensalidadeForm
    template_name = 'socios/mensalidade_form.html'
    success_url = reverse_lazy('gestao_mensalidades')
    
    def form_valid(self, form):  #####  MENSAGEM DE SUCESSO AO SALVAR #####
        response = super().form_valid(form)
        messages.success(self.request, "Mensalidades atualizadas com sucesso!")
        return response

    def form_invalid(self, form):  #####  MENSAGEM DE ERRO SE O FORMULÁRIO FOR INVÁLIDO #####
        messages.error(self.request, "Erro ao atualizar mensalidades.")
        return super().form_invalid(form)
   
#====================================================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@method_decorator(permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social']), name='dispatch')
class MensalidadeDeleteView(DeleteView):
    model = Mensalidade
    template_name = 'socios/mensalidade_confirm_delete.html'
    success_url = reverse_lazy('gestao_mensalidades')

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
#@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def sobre(request):
    return render(request, 'socios/sobre.html')

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def gerenciamento(request):
    query = request.GET.get('q') 
    query1 = request.GET.get('q1') 
    query2 = request.GET.get('q2') 
    socios = Socio.objects.all()
    dependentes = Dependente.objects.all()
    mensalidades = Mensalidade.objects.all()
   
    if query: 
        socios = Socio.objects.filter(nome__icontains=query) 
        
    if query1: 
        dependentes = Dependente.objects.filter(nome__icontains=query1) 
       
    if query2: 
        mensalidades = Mensalidade.objects.filter(socio__nome__icontains=query2) 
       

    context = {'query':query, 'query1':query1, 'query2':query2, 'socios':socios ,  'dependentes': dependentes, 'mensalidades': mensalidades}
    return render(request, 'socios/gerenciamento.html', context)

#====================================================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def gestao_socios(request):
    query = request.GET.get('q') 
    socios = Socio._base_manager.all() # Retorna todo ativos e inativos = True e False
    if query: 
        socios = socios.filter(nome__icontains=query) 

    paginator = Paginator(socios, LINHAS_POR_PAGINA)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'socios':page_obj.object_list, 'page_obj': page_obj}
    
    return render(request, 'socios/gestao_socios.html', context)

#====================================================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def gestao_dependentes(request):
    query = request.GET.get('q') 
    dependentes = Dependente.objects.all()
    if query: 
        dependentes = dependentes.filter(nome__icontains=query) 

    paginator = Paginator(dependentes, LINHAS_POR_PAGINA)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'dependentes':page_obj.object_list, 'page_obj': page_obj}
    
    return render(request, 'socios/gestao_dependentes.html', context)

#====================================================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def gestao_mensalidades(request):
    query = request.GET.get('q') 
    mensalidades = Mensalidade.objects.all().select_related('socio')  # Otimiza consultas ao banco de dados
    if query: 
        mensalidades = mensalidades.filter(socio__nome__icontains=query)

    paginator = Paginator(mensalidades, LINHAS_POR_PAGINA - 4)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,  # Passa o objeto de paginação
        'query': query  # Passa a consulta para exibir no template
    }
    
    return render(request, 'socios/gestao_mensalidades.html', context)

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def busca_socio(request): 
    query = request.GET.get('q') 
    if query: 
        socios = Socio.objects.filter(nome__icontains=query) 
    else: 
        socios = Socio.objects.all() 
    return render(request, 'socios/gerenciamento.html', {'socios': socios})

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def lista_socio_dependentes(request):
    query = request.GET.get('q') 
    socios = Socio.objects.prefetch_related('dependentes').all()  # Agora usa 'dependentes'
    if query: 
        socios = socios.filter(nome__icontains=query) 

    paginator = Paginator(socios, LINHAS_POR_PAGINA)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,  # Passa o objeto de paginação
        'query': query } # Passa a consulta para exibir no template
    return render(request, 'socios/lista_socio_dependentes.html',context)

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def lista_socios(request):
    socios = Socio.objects.all()
    return render(request, 'socios/lista_socios.html', {'socios': socios})

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico'] 
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def cria_socio(request):
  
    if request.method == 'POST':
        form = SocioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Socio incluido com sucesso.')
            return redirect('gestao_socios')
        else:
            messages.error(request, 'Ocorreu um erro ao processar o formulário.')
    else:
        form = SocioForm()
    return render(request, 'socios/cria_socio.html', {'form': form})

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico']
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def edita_socio(request, pk):
   
    #socios = Socio.objects.all()  # Retorna so os ativos = True
    socios = Socio._base_manager.all() # Retorna todo ativos e inativos = True e False
    socio = get_object_or_404(socios, pk=pk)
    if request.method == 'POST':
        form = SocioFormEdit(request.POST, request.FILES, instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Socio alterado com sucesso.')
            return redirect('gestao_socios')
        else:
            messages.error(request, 'Ocorreu um erro ao processar o formulário.')
    else:
        form = SocioFormEdit(instance=socio)
        
    return render(request, 'socios/edita_socio.html', {'form': form, 'socio': socio})

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico']
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def exclui_socio(request, pk):
 
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        socio.delete()
        return redirect('gestao_socios')
    return render(request, 'socios/exclui_socio.html', {'socio': socio})

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico']
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social', 'esportivo', 'basico'])
def lista_dependentes(request, socio_id):
    socio = get_object_or_404(Socio, pk=socio_id)
    dependentes = socio.dependentes.all()
    return render(request, 'socios/lista_dependentes.html', {'socio': socio, 'dependentes': dependentes})

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico']
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def cria_dependente(request):
 
    if request.method == 'POST':
        form = DependenteForm(request.POST, request.FILES)  # Preenche o formulário com os dados enviados
        if form.is_valid():
            dependente = form.save(commit=False)
            dependente.save()
            messages.success(request, 'Dependente Incluido com sucesso.')
            return redirect('gestao_dependentes')  # Redireciona para a lista de dependentes
    else:
        form = DependenteForm()  # Cria um formulário vazio
    return render(request, 'socios/cria_dependente.html', {'form': form})

#==============================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico']
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def edita_dependente(request, dependente_id):
 
    dependente = get_object_or_404(Dependente, pk=dependente_id)  # Obtém o dependente pelo ID
    if request.method == 'POST':
        form = DependenteFormEdit(request.POST, request.FILES, instance=dependente)  # Preenche o formulário com os dados enviados
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            messages.success(request, 'dependente alterado com sucesso.')
            return redirect('gestao_dependentes')  # Redireciona para a lista de dependentes do sócio
    else:
        form = DependenteFormEdit(instance=dependente)  # Preenche o formulário com os dados atuais do dependente
    return render(request, 'socios/edita_dependente.html', {'form': form, 'dependente': dependente})

#======================================================================================================================
#niveis_permitidos = ['admin', 'financeiro', 'social', 'esportivo', 'basico']
@permissoes_requeridas(niveis_permitidos=['admin', 'financeiro', 'social'])
def exclui_dependente(request, dependente_id):

    dependente = get_object_or_404(Dependente, pk=dependente_id) 
    if request.method == 'POST':
        dependente.delete()  # Exclui o dependente do banco de dados
        return redirect('gestao_dependentes')  # Redireciona para a lista de dependentes
    return render(request, 'socios/exclui_dependente.html', {'dependente': dependente})



