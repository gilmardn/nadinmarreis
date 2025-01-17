from django import forms
from .models import Quadra, Horario, Caixa
from datetime import datetime
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
        fields = ['tipo_operacao', 'categoria', 'cliente_fornecedor', 'data', 'descricao', 'valor']

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
        fields = ['tipo_operacao', 'categoria', 'cliente_fornecedor', 'data', 'descricao', 'valor']

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