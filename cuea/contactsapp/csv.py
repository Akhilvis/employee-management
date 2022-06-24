import csv
import datetime
import pandas as pd
from django.http import HttpResponse

from .models import *

class CSVProcess:
    
    def __init__(self):
        self.csv_file = 'employee_csv.csv'
    
    def feed_db(self):
        df = pd.read_csv(self.csv_file)
        for i, emp in df.iterrows():
            employee = Employees()
            if employee.is_old_employee(emp.PFNo):
                employee = Employees.objects.get(pf_number = emp.PFNo)
            
            try:

                employee.name = emp.Name
                employee.pf_number = emp.PFNo
                employee.sex = emp.Sex
                employee.mobile = emp.Mob
                employee.blood_group = emp.Blood
                employee.address = emp.Address
                employee.district = emp.District
                employee.pan_mun_cop = emp.Pan_Mun_Cor
                employee.pin_code = emp.PinCode
                employee.save()

                employee_service = EmployeeService()
                employee_service.employee = employee
                employee_service.designation = emp.Designation
                try:
                    employee_service.department = Section.objects.get(section=emp.Dept)
                except:
                    return False, '{pf} - Wrong Department!'.format(pf=emp.PFNo)
                employee_service.membership = emp.Membership
                employee_service.date_of_entry = self.date_parsing(emp.DoE)
                employee_service.date_of_retire = self.date_parsing(emp.DoR)
                employee_service.save()

                employee_vote = EmployeeVote()
                employee_vote.employee = employee
                employee_vote.legislative_assembly = emp.LegislativeAssembly
                employee_vote.loksabha_constituency = emp.LokSabhaConstituency
                employee_vote.voters_id = emp.VotersId
                employee_vote.deshabhimani_sub = emp.Deshabimanisubscription
                employee_vote.subscription_amount = emp.Yearlysubscription
                employee_vote.save()
            
            except Exception as error:
                print("error>>>>>  ",error)
                return False, '{pf} - Wrong Input!'.format(pf=emp.PFNo)

        return True,None

    def date_parsing(self, date_string):
        year, month, date = date_string.split("-")
        return datetime.date(int(year), int(month), int(date))

    def export_csv(self, url_params):
        output = []
        response = HttpResponse (content_type='text/csv')
        writer = csv.writer(response)
        employee = Employees()
        employee.get_filtered_result(url_params)
        query_set = employee.get_filtered_result(url_params)
    
        #Header
        writer.writerow(['Sl No.', 'PFNo', 'Name', 'Sex', 'Designation', 'Dept', 'Blood', 'DoE', 'DoR', 'Membership', 'Mob', 'email', 
        'Address', 'District', 'PinCode', 'VotersId', 'Pan_Mun_Cor', 'LegislativeAssembly', 'LokSabhaConstituency', 'other Religious/ political/ social orgnanisations', 'Deshabimanisubscription'
        , 'Yearlysubscription', 'Unit'])
        for num, emp in enumerate(query_set, start=1):
            output.append([num, emp.pf_number, emp.name, emp.sex, emp.employeeservice.designation, emp.employeeservice.department.section, emp.blood_group, emp.employeeservice.date_of_entry,emp.employeeservice.date_of_retire, emp.employeeservice.membership,
            emp.mobile, 'email', emp.address, emp.district, emp.pin_code, emp.employeevote.voters_id, 
            emp.pan_mun_cop, emp.employeevote.legislative_assembly, emp.employeevote.loksabha_constituency
            , '', emp.employeevote.deshabhimani_sub, emp.employeevote.subscription_amount, 
            emp.employeeservice.department.unit
            ])
        #CSV Data
        writer.writerows(output)
        return response





