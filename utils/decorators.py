from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def permissoes_requeridas(niveis_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Você não está logado.")
                return redirect('home')

            if not hasattr(request.user, 'nivel_acesso') or request.user.nivel_acesso not in niveis_permitidos:
                messages.warning(request, "Você não tem permissão para acessar esta página.")
                return redirect('home')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


