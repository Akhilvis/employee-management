from django.shortcuts import render
from django.http import HttpResponse
from .utils import *
from .forms import *
from .csv import CSVReader
# Create your views here.



def index(request):
    return render(request, 'index.html')

def upload_csv(request):
    return render(request, 'uploadcsv.html')

def csv_process(request):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  ',request.FILES.get('csv[]'))
    csv_data = request.FILES['csv']
    print(csv_data.name.split('.')[-1])
    if csv_data.name.split('.')[-1] != 'csv':
        print("INvalid file type")
        upload_error = 'Invalid File Type'
        return render(request, 'uploadcsv.html', {'upload_error': upload_error})
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(csv_data)
            print("uploaded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            success_message = 'Uploaded Successfuly'
            csv_reader = CSVReader()
            csv_reader.feed_db()
    return render(request, 'uploadcsv.html', {'success_message': success_message})
