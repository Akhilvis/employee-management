import csv
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from .utils import *
from .forms import *
from .csv import CSVProcess
from .models import *

from django.views.generic import ListView, TemplateView, View, DetailView
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
        employee = data.get('employee', None)
        target_department_id = data.get('target_dept', None)

        if employee and target_department_id:
            target_department = Section.objects.get(id=target_department_id)
            employee = Employees.objects.get(id=employee)
            current_dept = employee.employeeservice.department
            employee.employeeservice.department  = target_department
            employee.employeeservice.save()
            Activities.mark_activity('{name} transferred from {current_dept} to {target_dept}'.format(name=employee.name, current_dept=current_dept, target_dept=target_department.section))
            self.context['message'] = 'Employee Transferred successfully' 
            self.context['status'] = 'success' 

        else:
            self.context['message'] = 'Select employee and department' 
            self.context['status'] = 'danger' 

        
        return render(request, self.template_name, self.context)




class IUTReliveListView(LoginRequiredMixin, View):
    template_name = "contactsapp/iut_relieve.html"
    employee = Employees()
    context = {}
    
    def get(self, request):
        self.context['message'] = ''
        self.context['employees'] = self.employee.get_all_employees()
        self.context['ex_employees'] = self.employee.get_all_employees(is_current_employee=False)

        return render(request, self.template_name, self.context)
    
    def post(self, request):
        data = request.POST
        employee = data.get('employee', None)
        remark = data.get('remark', None)

        if employee and remark:
            employee = Employees.objects.get(id=employee)
            employee.employeeservice.is_current_employee = False
            employee.employeeservice.exit_remark = remark
            employee.employeeservice.save()
            Activities.mark_activity('{remark} marked against {name}'.format(remark=remark ,name=employee.name))

            self.context['message'] = 'Exit marked successfully!' 
            self.context['status'] = 'success' 
        else:
            self.context['message'] = 'Select employee and add remark!' 
            self.context['status'] = 'danger' 

        return render(request, self.template_name, self.context)

from django.contrib import messages


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    # specify the model to use
    model = Employees
  
    # override context data
    def get_context_data(self, *args, **kwargs):
        context = super(EmployeeDetailView,
             self).get_context_data(*args, **kwargs)
        # add extra field 
        context["sections"] = Section.objects.all()       
        return context
    
    def post(self, request, pk):
          instance = get_object_or_404(Employees, pk=pk)
          print(request.POST)
          input_data = request.POST.dict()
          form = EmployeesUpdateForm(instance=instance, data=input_data)

          if form.is_valid():
            obj  = form.save()
            service_instance = get_object_or_404(EmployeeService, employee=instance)
            print(999, input_data['department'])
            input_data['department'] = get_object_or_404(Section, pk=input_data['department'])

            service_form = EmployeeServiceUpdateForm(instance=service_instance, data=input_data)
            if service_form.is_valid():
                service_form.save()
            else:
                print(service_form.errors.as_json())
            return redirect('employee_detail_view', instance.pk)
          else:
            print("=========================error====", form.errors)
