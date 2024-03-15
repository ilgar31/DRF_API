from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, EmailInput


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': EmailInput(),
        }