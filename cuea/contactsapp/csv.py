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
            if employee.is_old_employee(emp.PFNo):
                employee = Employees.objects.get(pf_number = emp.PFNo)

            employee.name = emp.Name
            employee.pf_number = emp.PFNo
            employee.sex = emp.Sex
            employee.mobile = emp.Mob
            employee.blood_group = emp.Blood
            employee.adddress = emp.Address
            employee.district = emp.District
            employee.pan_mun_cop = emp.Pan_Mun_Cor
            employee.save()

            employee_service = EmployeeService()
            employee_service.employee = employee
            employee_service.designation = emp.Designation
            employee_service.department = emp.Dept
            employee_service.membership = emp.Membership
            employee_service.save()

            employee_vote = EmployeeVote()
            employee_vote.employee = employee
            employee_vote.legislative_assembly = emp.LegislativeAssembly
            employee_vote.loksabha_constituency = emp.LokSabhaConstituency
            employee_vote.voters_id = emp.VotersId
            employee_vote.deshabhimani_sub = emp.Deshabimanisubscription
            employee_vote.subscription_amount = emp.Yearlysubscription
            employee_vote.save()






