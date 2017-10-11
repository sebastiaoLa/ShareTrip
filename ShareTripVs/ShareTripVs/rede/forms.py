from models import *

from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,UsernameField

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','username','email','cpf','telefone','password1','password2')
        #widgets = {
        #    'senha': PasswordInput(),
        #}

class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','is_staff','is_superuser', 'telefone', 'cpf', 'password1', 'password2')

class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

class BilheteCreateForm(ModelForm):
    class Meta:
        model = Bilhete
        fields = ('poltrona','viagem')
        

