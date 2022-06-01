from unicodedata import name
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login-view'),
    path('logout', LogoutView.as_view(), name='logout-view'),

    path('dashboard', DashboardView.as_view(), name='dashboard-view'),

    path('upload-csv', upload_csv, name='upload_csv'),
    path('csv-data-upload', csv_process, name='csv_process'),
    path('employees', EmployeesListView.as_view(), name="list_employee_view"),
    path('search-employee', SearchEmployeeListView.as_view(), name='search_employee'),

]