from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index, name='main-view'),
    path('upload-csv', upload_csv, name='upload_csv'),
    path('csv-data-upload', csv_process, name='csv_process'),

]