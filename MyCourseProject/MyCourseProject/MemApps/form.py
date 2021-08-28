from django import forms
from .models import Memasik, MemIntermediate


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=25)
    password = forms.CharField(max_length=255)
    date = forms.DateField()
    email = forms.EmailField()


class LoginForm(forms.Form):
    login = forms.CharField(max_length=25)
    password = forms.CharField(max_length=255)


class ImageForm(forms.ModelForm):
    class Meta:
        model = MemIntermediate
        fields = ['url_image', ]


class ImageFormMain(forms.Form):
    url_image = forms.ImageField()
    tags = forms.CharField(max_length=255)
    date_mem = forms.DateTimeField()



class GalleryForm(forms.Form):
    class Meta:
        model = Memasik
        fields = ['id_mem', 'id_user']
