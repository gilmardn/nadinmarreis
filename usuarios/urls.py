from django.urls import path

from .import views


urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
]
urlpatterns += [
    path('popular_categorias/', views.popular_categorias, name='popular_categorias'),
]


