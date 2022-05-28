from django import forms

class UploadFileForm(forms.Form):
    csv = forms.FileField()