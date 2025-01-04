from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import  UsuarioForm 
from financas.models import Categoria, Quadra
from django.contrib import messages
from  .models import Usuario
#====================================================================================

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            form.add_error('first_name', 'Senhas não coincidem.')
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})



#====================================================================================


def login_view(request):
    # Redireciona usuários já autenticados
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Verifica se os campos estão preenchidos
        if not username or not password:
            messages.error(request, 'Preencha todos os campos.')
            return render(request, 'usuarios/login.html')

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Sua conta está inativa.')
        else:
            # Feedback mais específico (opcional)
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Usuário não encontrado.')
            else:
                messages.error(request, 'Senha incorreta.')

    return render(request, 'usuarios/login.html')


#====================================================================================
def logout_view(request):
    logout(request)
    return redirect('home')


def popular_categorias(request):
    categorias = [
            {"nome": "Mensalidades de Sócios", "ordem": "A00"},
            {"nome": "Venda de Ingressos para Evento", "ordem": "A55"},
		    {"nome": "Aluguel de Espaços (quadras, salões)", "ordem": "A11"},
		    {"nome": "Patrocínios e Doações", "ordem": "A44"},
		    {"nome": "Receitas de Eventos", "ordem": "A33"},
		    {"nome": "Receitas de Publicidade", "ordem": "A22"},
		    {"nome": "Manutenção de Instalações", "ordem": "B00"},
		    {"nome": "Contas Mensais (água, luz, internet)", "ordem": "B11"},
		    {"nome": "Outras (Receitas)", "ordem": "A99"},
		    {"nome": "Receitas de Parcerias", "ordem": "A66"},
		    {"nome": "Compra de Materiais", "ordem": "B22"},
		    {"nome": "Publicidade e Anúncios (banners)", "ordem": "A45"},
		    {"nome": "Compra de Materiais Esportivos", "ordem": "A44"},
		    {"nome": "Outras (Despesas)", "ordem": "B99"},
        ]

    for categoria in categorias:
            Categoria.objects.get_or_create(
                nome=categoria["nome"],
                ordem=categoria["ordem"]
            )

    quadras = [
        {"nome": "Quadra I", "descricao": "Quadra I"},
        {"nome": "Quadra II", "descricao": "Quadra II"},
        {"nome": "Salão de Festas", "descricao": "Salão de Festas"},
    ]

    for quadra in quadras:
            Quadra.objects.get_or_create(
                nome=quadra["nome"],
                descricao=quadra["descricao"]
            )
    return render(request, 'socios/home.html')
            


