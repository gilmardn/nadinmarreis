from django import forms
from .models import Socio, Dependente, Mensalidade
from financas.models import Contador
from datetime import datetime
from django.forms.widgets import DateInput

ano_atual = datetime.now().year

#===============================================================================
class DatePickerInput(DateInput):
    input_type = 'date'

#===============================================================================
class AnoForm(forms.Form):

    if ano_atual == 2025:
        choices_anos =[(ano_atual,  ano_atual),]
    elif ano_atual == 2026:
        choices_anos =[(ano_atual,  ano_atual),(ano_atual - 1, ano_atual - 1),]
    else:
        choices_anos =[(ano_atual,  ano_atual),(ano_atual - 1, ano_atual - 1), (ano_atual - 2, ano_atual - 2),]

    choices_anos =[(ano_atual,  ano_atual),]
   
    ano = forms.ChoiceField(
        choices=choices_anos,
        label='Mensalidades do ano.',
        widget=forms.Select(attrs={'class': 'form-select'}),  # Adiciona a classe do Bootstrap
    )
   

#===============================================================================
class SocioForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DatePickerInput)
    data_admisao = forms.DateField(widget=DatePickerInput)

    class Meta:
        model = Socio
        fields = '__all__'
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': "4"}),
            'cpf': forms.TextInput(attrs={'data-mask': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'data-mask': '00.000-000'}),
            }
        

        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

          

#===============================================================================
class SocioFormEdit(forms.ModelForm):

    class Meta:
        model = Socio
        fields = '__all__'
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': "4"}),
            'cpf': forms.TextInput(attrs={'data-mask': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'data-mask': '00.000-000'}),
            }

  
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

            if field.widget.__class__ in [forms.Textarea]:
                field.widget.attrs['rows'] = '4'

        

#===============================================================================
class DependenteForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Dependente
        fields = ['socio', 'nome', 'parentesco', 'data_nascimento', 'cpf', 'rg', 'foto']  # Campos que serão exibidos no formulário

        widgets = {
            'cpf': forms.TextInput(attrs={'data-mask': '000.000.000-00'}),
            }


    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

#===============================================================================
class DependenteFormEdit(forms.ModelForm):
    #data_nascimento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Dependente
        fields = ['socio', 'nome', 'parentesco', 'data_nascimento', 'cpf', 'rg', 'foto']  # Campos que serão exibidos no formulário

        widgets = {
            'cpf': forms.TextInput(attrs={'data-mask': '000.000.000-00'}),
            }


    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'


#===============================================================================
class MensalidadeForm(forms.ModelForm):
    class Meta:
        model = Mensalidade
        fields = ['socio', 'ano', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
                  'jul', 'ago', 'set', 'out', 'nov', 'dez', 'observacoes']
        
        widgets = {
            'socio': forms.TextInput(attrs={'type': "hidden"}),
            'ano': forms.TextInput(attrs={'readonly': "true"}),
            'observacoes': forms.Textarea(attrs={'rows': "4"}),
        }
        
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

#===============================================================================      
        