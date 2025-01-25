from django.contrib import admin
from .models import Socio, Dependente, Mensalidade #  Pagamento

#admin.site.register(Mensalidade)

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'ativo', 'tipo_socio')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('tipo_socio', 'ativo')

@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'parentesco', 'cpf')
    search_fields = ('nome', 'cpf')

@admin.register(Mensalidade)
class MensalidadeAdmin(admin.ModelAdmin):
    list_display = ('socio', 'ano', 'jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez' )
    ordering = ('socio__nome', 'ano')
    
 

