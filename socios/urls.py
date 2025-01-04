


from django.urls import path
from .views import ( MensalidadeUpdateView, MensalidadeDeleteView,
    #MensalidadeListView,
    #MensalidadeCreateView,
)

from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('gerenciamento/', views.gerenciamento, name='gerenciamento'),
]
urlpatterns += [
    path('lista_socios/', views.lista_socios, name='lista_socios'),
    path('gestao_socios/', views.gestao_socios, name='gestao_socios'),
    path('incluir/', views.cria_socio, name='cria_socio'),
    path('editar/<int:pk>/', views.edita_socio, name='edita_socio'),
    path('excluir/<int:pk>/', views.exclui_socio, name='exclui_socio'),
    path('socios/lista_socio_dependentes/', views.lista_socio_dependentes, name='lista_socio_dependentes'),

]

urlpatterns += [
    path('<int:socio_id>/dependentes/', views.lista_dependentes, name='lista_dependentes'),
    path('dependentes/gestao_dependentes/', views.gestao_dependentes, name='gestao_dependentes'),
    path('dependentes/incluir/', views.cria_dependente, name='cria_dependente'),
    path('dependentes/editar/<int:dependente_id>/', views.edita_dependente, name='edita_dependente'),
    path('dependentes/excluir/<int:dependente_id>/', views.exclui_dependente, name='exclui_dependente'),
]
urlpatterns += [
    #path('<int:socio_id>/mensalidades/', views.lista_mensalidades, name='lista_mensalidades'),
    #path('<int:socio_id>/mensalidades/incluir/', views.cria_pagamento, name='cria_pagamento'),
    #path('mensalidades/editar/<int:pagamento_id>/', views.edita_pagamento, name='edita_pagamento'),
    #path('confirmar_pagamento/<int:mensalidade_id>/<str:meses>/', views.confirmar_pagamento, name='confirmar_pagamento'),
]
urlpatterns += [
    #path('list/', MensalidadeListView.as_view(), name='mensalidade_list'),
    path('list/',views.lista_mensalidades, name='lista_mensalidades'),
    path('gestao_mensalidades/',views.gestao_mensalidades, name='gestao_mensalidades'),
    #path('create/', MensalidadeCreateView.as_view(), name='mensalidade_create'),
    path('update/<int:pk>/', MensalidadeUpdateView.as_view(), name='mensalidade_update'),
    path('delete/<int:pk>/', MensalidadeDeleteView.as_view(), name='mensalidade_delete'),

]









