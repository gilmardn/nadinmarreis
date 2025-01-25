from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', include('socios.urls')),
    path('financas/', include('financas.urls')),
    path('socios/', include('socios.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('admin/', admin.site.urls),
]

