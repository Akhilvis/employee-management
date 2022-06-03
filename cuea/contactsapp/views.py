from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from .utils import *
from .forms import *
from .csv import CSVReader
from .models import *

from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class LoginView(View):
    template_name = "contactsapp/login.html"
    
    def get(self, request):
        return render(request, self.template_name)
        
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard-view')
        message = 'Login failed!'
        return render(request, self.template_name, context={'message': message})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "contactsapp/index.html"

def index(request):
    return render(request, 'contactsapp/index.html')

def upload_csv(request):
    return render(request, 'contactsapp/uploadcsv.html')

def csv_process(request):
    csv_data = request.FILES['csv']
    if csv_data.name.split('.')[-1] != 'csv':
        upload_error = 'Invalid File Type'
        return render(request, 'uploadcsv.html', {'upload_error': upload_error})
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(csv_data)
            success_message = 'Uploaded Successfuly'
            csv_reader = CSVReader()
            csv_reader.feed_db()
    return render(request, 'contactsapp/uploadcsv.html', {'success_message': success_message})

class EmployeesListView(LoginRequiredMixin, ListView):
    paginate_by = 20
    employee_object = Employees()

    def get_queryset(self, *args, **kwargs):
        url_params = self.request.GET
        return self.employee_object.get_all_employees()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_data'] = self.employee_object.get_filter_popup_data()
        return context

class FilterEmployeeListView(LoginRequiredMixin, ListView):
    employee_object = Employees()

    def get_queryset(self):
        return self.employee_object.get_filtered_result(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_data'] = self.employee_object.get_filter_popup_data()
        return context

class SearchEmployeeListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        seach_key = self.request.GET.get('search_keyword')
        employee_object = Employees()
        return employee_object.get_searched_employee(seach_key)
