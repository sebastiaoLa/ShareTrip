from models import *

from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,UsernameField

class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['first_name'].widget.attrs['autofocus']=""

    class Meta:
        model = User
        fields = ('first_name','username','email','telefone','password1','password2')
        #widgets = {
        #    'senha': PasswordInput(),
        #}

class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','is_staff','is_superuser', 'telefone', 'password1', 'password2')

class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

class BilheteCreateForm(ModelForm):
    class Meta:
        model = Bilhete
        fields = ('poltrona','viagem')
        

