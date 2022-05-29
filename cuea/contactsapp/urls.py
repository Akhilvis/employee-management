from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index, name='main-view'),
    path('upload-csv', upload_csv, name='upload_csv'),
    path('csv-data-upload', csv_process, name='csv_process'),
    path('employees', list_employees, name='list_employees'),
    path('search-employee', search_employee, name='search_employee'),

]