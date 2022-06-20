from django import forms
from django.db import models
from .models import EmployeeService, Employees


class UploadFileForm(forms.Form):
    csv = forms.FileField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class EmployeesUpdateForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['name', 'blood_group', 'mobile']

class EmployeeServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeService
        fields = ['employee', 'membership', 'department', 'designation']