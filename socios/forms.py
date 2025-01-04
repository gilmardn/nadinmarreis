from django import forms
from .models import Socio, Dependente, Mensalidade
from financas.models import Contador
from datetime import datetime
from django.forms.widgets import DateInput


#===============================================================================
class DatePickerInput(DateInput):
    input_type = 'date'

#===============================================================================
class AnoForm(forms.Form):
   ano_atual = datetime.now().year
   ano = forms.ChoiceField(
        choices=[(ano_atual,  ano_atual),(ano_atual - 1, ano_atual - 1), (ano_atual - 2, ano_atual - 2),],
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
        widgets = {'endereco': forms.Textarea(attrs={'rows': "4"}),}
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            # Adiciona o atributo autocomplete="off" ao widget do campo
            if 'autocomplete' not in field.widget.attrs:
                field.widget.attrs['autocomplete'] = 'off'

#===============================================================================
class SocioFormEdit(forms.ModelForm):
   
    #data_nascimento = forms.DateField(widget=DatePickerInput)
    #data_admisao = forms.DateField(widget=DatePickerInput)

    class Meta:
        model = Socio
        fields = '__all__'
        widgets = {'endereco': forms.Textarea(attrs={'rows': "4"}),}
  
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field.widget.__class__ in [forms.Textarea]:
                field.widget.attrs['rows'] = '4'

                        # Adiciona o atributo autocomplete="off" ao widget do campo
            if 'autocomplete' not in field.widget.attrs:
                field.widget.attrs['autocomplete'] = 'off'

#===============================================================================
class DependenteForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Dependente
        fields = ['socio', 'nome', 'parentesco', 'data_nascimento', 'cpf', 'rg', 'foto']  # Campos que serão exibidos no formulário

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

                    # Adiciona o atributo autocomplete="off" ao widget do campo
            if 'autocomplete' not in field.widget.attrs:
                field.widget.attrs['autocomplete'] = 'off'

#===============================================================================
class DependenteForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Dependente
        fields = ['socio', 'nome', 'parentesco', 'data_nascimento', 'cpf', 'rg', 'foto']  # Campos que serão exibidos no formulário

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

                        # Adiciona o atributo autocomplete="off" ao widget do campo
            if 'autocomplete' not in field.widget.attrs:
                field.widget.attrs['autocomplete'] = 'off'

#===============================================================================
class DependenteForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Dependente
        fields = ['socio', 'nome', 'parentesco', 'data_nascimento', 'cpf', 'rg', 'foto']  # Campos que serão exibidos no formulário

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

#===============================================================================
class DependenteForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Dependente
        fields = ['socio', 'nome', 'parentesco', 'data_nascimento', 'cpf', 'rg', 'foto']  # Campos que serão exibidos no formulário

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

#===============================================================================
class DependenteFormEdit(forms.ModelForm):
    #data_nascimento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Dependente
        fields = ['socio', 'nome', 'parentesco', 'data_nascimento', 'cpf', 'rg', 'foto']  # Campos que serão exibidos no formulário

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


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
            #'name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': ''}),
            #'manufacturing_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder':''}),
            #'image': forms.ClearableFileInput(attrs={'type': 'file', 'class': 'form-control'}),
        }
        
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

#===============================================================================      
        