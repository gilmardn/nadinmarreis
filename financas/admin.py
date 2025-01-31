from django.contrib import admin
from .models import Quadra, Horario, Caixa, Categoria, Contador, Parceiro


class CaixaAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj and obj.consolidado:
            return False
        return super().has_delete_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.consolidado:
            return self.readonly_fields + ('data', 'tipo_operacao', 'categoria', 'descricao', 'valor', 'consolidado', 'criado_em', 'atualizado_em')
        return self.readonly_fields

@admin.register(Parceiro)
class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'email', 'cpf')


admin.site.register(Quadra)
admin.site.register(Horario)
admin.site.register(Caixa, CaixaAdmin)
admin.site.register(Categoria)
admin.site.register(Contador)


