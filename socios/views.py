from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Socio, Dependente, Mensalidade # ,Pagamento, 
from .forms import SocioForm, DependenteForm, MensalidadeForm, SocioFormEdit, DependenteFormEdit
from django.views.generic import  UpdateView, DeleteView # ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages



#====================================================================================
def lista_mensalidades(request):
    query = request.GET.get('q') 
    socios = Socio.objects.prefetch_related('mensalidades').all()  # Agora usa 'dependentes'
    if query: 
       socios = socios.filter(nome__icontains=query) 
    paginator = Paginator(socios, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'socios/lista_mensalidades.html', {'socios':page_obj.object_list, 'page_obj': page_obj})

#====================================================================================
class MensalidadeUpdateView(UpdateView):
    model = Mensalidade
    form_class = MensalidadeForm
    template_name = 'socios/mensalidade_form.html'
    success_url = reverse_lazy('gestao_mensalidades')

#====================================================================================
class MensalidadeDeleteView(DeleteView):
    model = Mensalidade
    template_name = 'socios/mensalidade_confirm_delete.html'
    success_url = reverse_lazy('gestao_mensalidades')

#==============================================================
def home(request):
    return render(request, 'socios/home.html')

#==============================================================
def sobre(request):
    return render(request, 'socios/sobre.html')

#==============================================================
def gerenciamento(request):
    query = request.GET.get('q') 
    active_tab = request.GET.get('activeTab', 'tab1')  # Valor padrão é 'tab1'
    print(active_tab)
    socios = Socio.objects.all()
    if query: 
        socios = Socio.objects.filter(nome__icontains=query) 

    paginator = Paginator(socios, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dependentes = Dependente.objects.all()
    mensalidades = Mensalidade.objects.all()
    context = {'socios':page_obj.object_list ,  'dependentes': dependentes, 'mensalidades': mensalidades, 'page_obj': page_obj}

    if request.method == 'POST':
        if active_tab == 'tab1':  
            socios = Socio.objects.all()
            if query: 
                socios = Socio.objects.filter(nome__icontains=query) 

            paginator = Paginator(socios, 10)  # Display 10 items per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            dependentes = Dependente.objects.all()
            mensalidades = Mensalidade.objects.all()
            context = {'socios':page_obj.object_list ,  'dependentes': dependentes, 'mensalidades': mensalidades, 'page_obj': page_obj}

        elif active_tab == 'tab2':
            dependentes = Dependente.objects.all()
            paginator = Paginator(dependentes, 10)  # Display 10 items per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            socios = Socio.objects.all()
            mensalidades = Mensalidade.objects.all()
            context = {'socios': socios ,  'dependentes': page_obj.object_list, 'mensalidades': mensalidades, 'page_obj': page_obj}

        elif active_tab == 'tab3':
            mensalidades = Mensalidade.objects.all()
            paginator = Paginator(mensalidades, 10)  # Display 10 items per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            socios = Socio.objects.all()
            dependentes = Dependente.objects.all()
            context = {'socios':socios,  'dependentes': dependentes, 'mensalidades': page_obj.object_list, 'page_obj': page_obj}

    return render(request, 'socios/gerenciamento.html',context)

#====================================================================================
def gestao_socios(request):
    query = request.GET.get('q') 
    socios = Socio.objects.all()
    if query: 
        socios = socios.filter(nome__icontains=query) 

    paginator = Paginator(socios, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'socios':page_obj.object_list, 'page_obj': page_obj}
    
    return render(request, 'socios/gestao_socios.html',context)

#====================================================================================
def gestao_dependentes(request):
    query = request.GET.get('q') 
    dependentes = Dependente.objects.all()
    if query: 
        dependentes = dependentes.filter(nome__icontains=query) 

    paginator = Paginator(dependentes, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'dependentes':page_obj.object_list, 'page_obj': page_obj}
    
    return render(request, 'socios/gestao_dependentes.html', context)

#====================================================================================
def gestao_mensalidades(request):
    query = request.GET.get('q') 
    mensalidades = Mensalidade.objects.all()
    if query: 
        mensalidades = mensalidades.filter(socio__nome__icontains=query)

    paginator = Paginator(mensalidades, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'mensalidades':page_obj.object_list, 'page_obj': page_obj}
    
    return render(request, 'socios/gestao_mensalidades.html', context)

#==============================================================
def busca_socio(request): 
    query = request.GET.get('q') 
    if query: 
        socios = Socio.objects.filter(nome__icontains=query) 
    else: 
        socios = Socio.objects.all() 
    return render(request, 'socios/gerenciamento.html', {'socios': socios})

#==============================================================
def lista_socio_dependentes(request):
    query = request.GET.get('q') 
    socios = Socio.objects.prefetch_related('dependentes').all()  # Agora usa 'dependentes'
    if query: 
        socios = socios.filter(nome__icontains=query) 
    paginator = Paginator(socios, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'socios':page_obj.object_list, 'page_obj': page_obj}
    return render(request, 'socios/lista_socio_dependentes.html',context)

#==============================================================
def lista_socios(request):
    socios = Socio.objects.all()
    return render(request, 'socios/lista_socios.html', {'socios': socios})

#==============================================================
def cria_socio(request):
    if request.method == 'POST':
        form = SocioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Socio incluido com sucesso.')
            return redirect('gestao_socios')
        else:
            messages.error(request, 'Ocorreu um erro ao processar o formulário.')
    else:
        form = SocioForm()
    return render(request, 'socios/cria_socio.html', {'form': form})

#==============================================================
def edita_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)

    if request.method == 'POST':
        form = SocioFormEdit(request.POST, request.FILES, instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request, f'Socio alterado com sucesso.')
            return redirect('gestao_socios')
        else:
            messages.error(request, 'Ocorreu um erro ao processar o formulário.')
    else:
        form = SocioFormEdit(instance=socio)
        
    return render(request, 'socios/edita_socio.html', {'form': form, 'socio': socio})

#==============================================================
def exclui_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        socio.delete()
        return redirect('gestao_socios')
    return render(request, 'socios/exclui_socio.html', {'socio': socio})

#==============================================================
def lista_dependentes(request, socio_id):
    socio = get_object_or_404(Socio, pk=socio_id)
    dependentes = socio.dependentes.all()
    return render(request, 'socios/lista_dependentes.html', {'socio': socio, 'dependentes': dependentes})

#==============================================================
def cria_dependente(request):
    if request.method == 'POST':
        form = DependenteForm(request.POST, request.FILES)  # Preenche o formulário com os dados enviados
        if form.is_valid():
            dependente = form.save(commit=False)
            dependente.save()
            return redirect('gestao_dependentes')  # Redireciona para a lista de dependentes
    else:
        form = DependenteForm()  # Cria um formulário vazio
    return render(request, 'socios/cria_dependente.html', {'form': form})

#==============================================================
def edita_dependente(request, dependente_id):
    dependente = get_object_or_404(Dependente, pk=dependente_id)  # Obtém o dependente pelo ID
    if request.method == 'POST':
        form = DependenteFormEdit(request.POST, request.FILES, instance=dependente)  # Preenche o formulário com os dados enviados
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            return redirect('gestao_dependentes')  # Redireciona para a lista de dependentes do sócio
    else:
        form = DependenteFormEdit(instance=dependente)  # Preenche o formulário com os dados atuais do dependente
    return render(request, 'socios/edita_dependente.html', {'form': form, 'dependente': dependente})

#======================================================================================================================
def exclui_dependente(request, dependente_id):
    dependente = get_object_or_404(Dependente, pk=dependente_id) 
    if request.method == 'POST':
        dependente.delete()  # Exclui o dependente do banco de dados
        return redirect('gestao_dependentes')  # Redireciona para a lista de dependentes
    return render(request, 'socios/exclui_dependente.html', {'dependente': dependente})

