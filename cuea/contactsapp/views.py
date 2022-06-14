import csv
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from .utils import *
from .forms import *
from .csv import CSVProcess
from .models import *

from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class LoginView(View):
    template_name = "contactsapp/login.html"
    
    def get(self, request):
        # sections_set = set()
        # f = open("sections_list.txt", "r")
        # for line in f.readlines():
        #     sections_set.add(line.strip())
        # for section in sections_set:
        #     unit = Unit.objects.first()
        #     Section.objects.create(section=section, unit=unit)
        
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
    employee_object = Employees()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_data'] = self.employee_object.get_dashboard_data()
        return context

class UploadCSView(LoginRequiredMixin, View):

        template_name = "contactsapp/uploadcsv.html"
        def get(self, request):
            return render(request, self.template_name)
        
        def post(self, request):
            csv_data = request.FILES['csv']
            if csv_data.name.split('.')[-1] != 'csv':
                upload_error = 'Invalid File Type'
                return render(request, self.template_name, {'upload_error': upload_error})
            if request.method == 'POST':
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    handle_uploaded_file(csv_data)
                    success_message = 'Uploaded Successfuly'
                    csv_reader = CSVProcess()
                    status, error_message = csv_reader.feed_db()
                    if status:
                        return render(request, self.template_name, {'success_message': success_message})
                    else:
                        return render(request, self.template_name, {'upload_error': error_message})

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

class RetiredEmployeesListView(LoginRequiredMixin, ListView):
    template_name = 'contactsapp/retired_list.html'
    employee_object = Employees()

    def get_queryset(self, *args, **kwargs):
        url_params = self.request.GET
        return self.employee_object.get_all_employees(is_retired=True)

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


class ExportCSView(LoginRequiredMixin, View):
    def get(self, request):
        csv_processor = CSVProcess()
        return csv_processor.export_csv(self.request.GET)


class TransferListView(LoginRequiredMixin, View):
    template_name = "contactsapp/transfer.html"
    sections = Section()
    employee = Employees()
    context = {}
    
    def get(self, request):
        self.context['sections'] = self.sections.get_all_sections()
        self.context['employees'] = self.employee.get_all_employees()
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        data = request.POST
        print(data)
        employee = data.get('employee', None)
        target_department_id = data.get('target_dept', None)

        if employee and target_department_id:
            target_department = Section.objects.get(id=target_department_id)
            employee = Employees.objects.get(id=employee)
            employee.employeeservice.department  = target_department
            employee.employeeservice.save()
            self.context['success'] = 'Employee Transferred successfully' 

        else:
            self.context['error'] = 'Select employee and department' 
        
        return render(request, self.template_name, self.context)




