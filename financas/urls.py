from django.urls import path
from .views import (
    HorarioListView, HorarioCreateView, HorarioUpdateView, HorarioDeleteView,
    CaixaListView, CaixaCreateView, CaixaUpdateView, CaixaDeleteView,
    ParceiroListView, ParceiroCreateView, ParceiroUpdateView, ParceiroDeleteView,
)

from .import views

urlpatterns = [
    path('horario/', HorarioListView.as_view(), name='horario-list'),
    path('horario/create/', HorarioCreateView.as_view(), name='horario-create'),
    path('horario/update/<int:pk>/', HorarioUpdateView.as_view(), name='horario-update'),
    path('horario/delete/<int:pk>/', HorarioDeleteView.as_view(), name='horario-delete'),
    path('lista_horario/', views.lista_horario, name='lista_horario'),
]

urlpatterns += [
    path('caixa/', CaixaListView.as_view(), name='caixa-list'),
    path('lista_caixa/', views.lista_caixa, name='lista_caixa'),
    path('caixa/create/', CaixaCreateView.as_view(), name='caixa-create'),
    path('caixa/update/<int:pk>/', CaixaUpdateView.as_view(), name='caixa-update'),
    path('caixa/delete/<int:pk>/', CaixaDeleteView.as_view(), name='caixa-delete'),
]

urlpatterns += [
    path('gerencia_financa/', views.gerencia_financa, name='gerencia_financa'),
    path('gestao_caixa/', views.gestao_caixa, name='gestao_caixa'),
    path('gestao_horario/', views.gestao_horario, name='gestao_horario'),
    path('rotina_periodica/', views.rotina_periodica, name='rotina_periodica'),
    path('consolidar_registros/', views.consolidar_registros, name='consolidar_registros'),
    path('importa_socios_para_parceiros/', views.importa_socios_para_parceiros, name='importa_socios_para_parceiros'),
]

urlpatterns += [
    path('gestao_parceiro/', ParceiroListView.as_view(), name='gestao_parceiro'),
    path('parceiro_create/', ParceiroCreateView.as_view(), name='parceiro_create'),
    path('<int:pk>/parceiro_update/', ParceiroUpdateView.as_view(), name='parceiro_update'),
    path('<int:pk>/parceiro_delete/', ParceiroDeleteView.as_view(), name='parceiro_delete'),
]
