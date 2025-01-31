from django import forms
from .models import Quadra, Horario, Caixa, Parceiro
from django.forms.widgets import DateInput, TimeInput

#-----------------------------------------------------------------------------
class DatePickerInput(DateInput):
    input_type = 'date'

#-----------------------------------------------------------------------------
class TimePickerInput(TimeInput):
    input_type = 'time'  # Define o tipo de input como 'time'

#---------------------------------------------------------------------------------------
class QuadraForm(forms.ModelForm):
    class Meta:
        model = Quadra
        fields = ['nome', 'descricao']

#---------------------------------------------------------------------------------------
class HorarioForm(forms.ModelForm):
    data = forms.DateField(widget=DatePickerInput())
    hora_inicio = forms.TimeField(widget=TimePickerInput())
    hora_fim = forms.TimeField(widget=TimePickerInput())
    class Meta:
        model = Horario
        fields = ['quadra', 'responsavel', 'data', 'hora_inicio', 'hora_fim']

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for campos, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

#---------------------------------------------------------------------------------------
class HorarioFormEdit(forms.ModelForm):
    #data = forms.DateField(widget=DatePickerInput)
    hora_inicio = forms.TimeField(widget=TimePickerInput())
    hora_fim = forms.TimeField(widget=TimePickerInput())
    class Meta:
        model = Horario
        fields = ['quadra', 'responsavel', 'data', 'hora_inicio', 'hora_fim']

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

#---------------------------------------------------------------------------------------
class CaixaForm(forms.ModelForm):
    data = forms.DateField(widget=DatePickerInput)
   
    class Meta:
        model = Caixa
        fields = ['tipo_operacao', 'categoria', 'parceiro', 'data', 'descricao', 'valor']

    def __init__(self, *args, **kwargs):
        super(CaixaForm, self).__init__(*args, **kwargs)

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

        if self.instance and self.instance.consolidado:
            for field in self.fields:
                self.fields[field].disabled = True

#---------------------------------------------------------------------------------------
class CaixaFormEdit(forms.ModelForm):
   #data = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Caixa
        fields = ['tipo_operacao', 'categoria', 'parceiro', 'data', 'descricao', 'valor']

    def __init__(self, *args, **kwargs):
        super(CaixaFormEdit, self).__init__(*args, **kwargs)

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

        if self.instance and self.instance.consolidado:
            for field in self.fields:
                self.fields[field].disabled = True

#---------------------------------------------------------------------------------------
class ParceiroForm(forms.ModelForm):
    class Meta:
        model = Parceiro
        fields = ['nome','email', 'telefone', 'cidade', 'endereco', 'cep', 'cpf_cnpj', 'ie', 'ativo']

        widgets = {
            'cep': forms.TextInput(attrs={'data-mask': '00.000-000'}),
            'ie': forms.TextInput(attrs={'data-mask': '000/000000-0'}),
            'cpf_cnpj': forms.TextInput(attrs={'data-mask': '00.000.000/0000-00'}),
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 00000-0000'}),
            }

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  

        for x, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

