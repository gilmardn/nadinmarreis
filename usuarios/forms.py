from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password  # Importe make_password para criptografar a senha

#===============================================================================
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha')
    first_name = forms.CharField(label='Nome Completo')

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'email')

        help_texts = {
            'username': ''
        }

    def __init__(self, *args, **kwargs):  # Corrigido: __init__ em vez de _init_
        super().__init__(*args, **kwargs)  # Corrigido: super() com parênteses

        for x, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:  # Corrigido: __class__ em vez de _class_
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Senhas não coincidem.')

    def save(self, commit=True):
        user = super().save(commit=False)  # Salva o usuário sem commit para adicionar a senha
        user.set_password(self.cleaned_data['password'])  # Define a senha criptografada
        if commit:
            user.save()  # Salva o usuário no banco de dados
        return user

#===============================================================================