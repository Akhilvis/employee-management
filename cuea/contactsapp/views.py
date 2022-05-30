from django.shortcuts import render
from django.http import HttpResponse

from .utils import *
from .forms import *
from .csv import CSVReader
from .models import *

from django.views.generic import ListView

# Create your views here.



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

class EmployeesListView(ListView):
    paginate_by = 20
    def get_queryset(self):
        employee_object = Employees()
        return employee_object.get_all_employees()

class SearchEmployeeListView(ListView):
    def get_queryset(self):
        seach_key = self.request.GET.get('search_keyword')
        employee_object = Employees()
        return employee_object.get_searched_employee(seach_key)
