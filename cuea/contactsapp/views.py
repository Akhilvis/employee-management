from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from .utils import *
from .forms import *
from .csv import CSVReader
from .models import *

# Create your views here.



def index(request):
    return render(request, 'index.html')

def upload_csv(request):
    return render(request, 'uploadcsv.html')

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
    return render(request, 'uploadcsv.html', {'success_message': success_message})

def list_employees(request):
    employees = Employees.objects.select_related('employeeservice').select_related('employeevote').all()
    return render(request, 'list_employees.html', {'employees': employees})

def search_employee(request):
    seach_key = request.POST.get('search_keyword')
    print(seach_key)

    searched_employees = Employees.objects.select_related('employeeservice').select_related('employeevote').filter(
            Q(name__icontains=seach_key) | Q(sex__icontains=seach_key) | Q(employeeservice__designation__icontains=seach_key)
        )
    return render(request, 'list_employees.html', {'employees': searched_employees})
