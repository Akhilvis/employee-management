from unicodedata import name
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login-view'),
    path('logout', LogoutView.as_view(), name='logout-view'),

    path('dashboard', DashboardView.as_view(), name='dashboard-view'),

    path('upload-csv', UploadCSView.as_view(), name='upload_csv'),

    path('employees', EmployeesListView.as_view(), name="list_employee_view"),
    path('retired', RetiredEmployeesListView.as_view(), name="list_retired_employee_view"),
    path('transfer', TransferListView.as_view(), name="transfer_employee_view"),

    path('search-employee', SearchEmployeeListView.as_view(), name='search_employee'),
    path('filter-employees', FilterEmployeeListView.as_view(), name="filter_list_employee_view"),
    path('exportcsv', ExportCSView.as_view(), name="export-csv"),

]