
from django.urls import path
from .import views

urlpatterns = [
    path('relatorio-socios-pdf/', views.relatorio_socios_pdf, name='relatorio_socios_pdf'),
    path('gerar_relatorio_socio_pdf/', views.gerar_relatorio_socio_pdf, name='gerar_relatorio_socio_pdf'),
    path('relatorio_socios_mensalidades_pdf/', views.relatorio_socios_mensalidades_pdf, name='relatorio_socios_mensalidades_pdf'),
    path('grafico_mensalidades/', views.grafico_mensalidades, name='grafico_mensalidades'),
    path('grafico-tipos-socio/', views.grafico_tipos_socio, name='grafico_tipos_socio'),
]

