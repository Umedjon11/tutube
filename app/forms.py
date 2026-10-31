from django.forms import Form, ModelForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import *


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields= ['username', 'email', 'password']

    def clean(self):
        data = super().clean()

        if User.objects.filter(username = self.cleaned_data.get('username')).exists():
            raise ValidationError('This username is already taken!')

        return data

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
            is_active = False
        )

        return user


class LoginForm(Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=1000, widget=forms.PasswordInput, required=True)

    def clean(self):
        data = super().clean()
        
        user = authenticate(
            username = self.cleaned_data.get('username'),
            password = self.cleaned_data.get('password')
        )

        if not user:
            raise ValidationError('Incorect username or password!')
        else:
            self.user = user

        return data


class CreateVideoForm(ModelForm):
    class Meta:
        model = Video
        fields= ['file', 'category', 'title', 'description', 'type']


class UpdateVideoForm(ModelForm):
    class Meta:
        model = Video
        fields= ['file', 'category', 'title', 'description', 'type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['file'].required = False


class CreatePlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields= ['title']
