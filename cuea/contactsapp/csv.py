import pandas as pd
from .models import *

class CSVReader:
    
    def __init__(self):
        self.csv_file = 'employee_csv.csv'
    
    def feed_db(self):
        df = pd.read_csv(self.csv_file)
        print(df.head())
        for i, emp in df.iterrows():
            print(i,emp)
            employee = Employees()
            employee.name = emp.Name
            employee.pf_number = emp.PFNo
            employee.sex = emp.Sex
            employee.blood_group = emp.Blood
            employee.adddress = emp.Address
            employee.district = emp.District
            employee.pan_mun_cop = emp.Pan_Mun_Cor
            employee.save()

            employee_service = EmployeeService()
            employee_service.employee = employee
            employee_service.designation = emp.Designation
            employee_service.department = emp.Dept
            employee_service.membership = "Association"
            employee_service.save()






