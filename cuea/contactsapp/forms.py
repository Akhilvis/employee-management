from django import forms

class UploadFileForm(forms.Form):
    csv = forms.FileField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()