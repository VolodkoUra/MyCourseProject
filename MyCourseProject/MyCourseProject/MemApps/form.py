from django import forms
from .models import Memasik, MemIntermediate


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=25)
    password = forms.CharField(max_length=255, min_length=6)
    date = forms.DateField()
    email = forms.EmailField()


class LoginForm(forms.Form):
    login = forms.CharField(max_length=25)
    password = forms.CharField(max_length=255)


class GalleryForm(forms.Form):
    class Meta:
        model = Memasik
        fields = ['id_mem', 'id_user']
