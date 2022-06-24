from enum import unique
from functools import total_ordering
from django.db import models
from django.db.models import Q
from django.db import connection

from .managers import *


class Unit(models.Model):
    unit = models.IntegerField()

    def __str__(self):
        return '{unit}'.format(unit=self.unit) 

class Section(models.Model):
    section = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def get_all_sections(self):
        return Section.objects.all()

    def __str__(self):
        return '{section} - {unit}'.format(section=self.section, unit=self.unit) 


class Employees(models.Model):
    pf_number = models.IntegerField()
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=30, default="M")
    blood_group = models.CharField(max_length=10)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    district = models.CharField(max_length=20)
    pan_mun_cop = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=20)

    def is_old_employee(self, pf_num):
        return Employees.objects.filter(pf_number = pf_num).exists()
    
    def get_all_employees(self, is_retired=False, is_current_employee = True):
        return Employees.objects.select_related('employeeservice').select_related('employeevote').filter(employeeservice__is_retired=is_retired, employeeservice__is_current_employee=is_current_employee).defer('address')

    def get_searched_employee(self, seach_key):
        searched_employees = Employees.objects.select_related('employeeservice').select_related('employeevote').filter(Q(employeeservice__is_retired=False, employeeservice__is_current_employee=True)&
                    Q(name__icontains=seach_key) | Q(sex__icontains=seach_key) | Q(employeeservice__designation__icontains=seach_key)
                    | Q(blood_group__icontains=seach_key) | Q(address__icontains=seach_key)|
                    Q(district__icontains=seach_key) | Q(pan_mun_cop__icontains=seach_key)|
                    Q(employeevote__loksabha_constituency__icontains=seach_key)|
                    Q(employeevote__deshabhimani_sub__icontains=seach_key)|  
                    Q(mobile__icontains=seach_key)|
                    Q(employeeservice__department__section__icontains=seach_key) | 
                    Q(employeeservice__membership__icontains=seach_key)|
                    Q(employeevote__legislative_assembly__icontains=seach_key) 

                ).defer('address')
        return searched_employees
    
    def get_filter_popup_data(self):
        filter_data = {}
        filter_data = list(Employees.objects.values('sex', 'blood_group', 'employeeservice__designation', 'employeeservice__department', 'employeeservice__membership', 'employeevote__deshabhimani_sub').distinct())
        unique_keywords = {filtertkey: set() for filtertkey in ['sex', 'blood_group', 'employeeservice__designation', 'employeeservice__department', 'employeeservice__membership', 'employeevote__deshabhimani_sub']}

        for data in filter_data:
            for key in data.keys():
                unique_keywords[key].add(data[key])
        
        new_keys = {'sex':'Gender', 'blood_group':'Blood Group', 'employeeservice__designation':'Designation', 'employeeservice__department':'Department', 'employeeservice__membership': 'Membership', 'employeevote__deshabhimani_sub': 'Deshabhimani Subscription'}
        unique_keywords = dict((new_keys[key], value) for (key, value) in unique_keywords.items())
       
        return unique_keywords
    
    def get_filtered_result(self, parameter_object):
        new_keys = {'Gender': 'sex', 'Blood Group': 'blood_group', 'Designation':'employeeservice__designation', 'Department':'employeeservice__department', 'Membership': 'employeeservice__membership', 'Deshabhimani Subscription':'employeevote__deshabhimani_sub'}
        query_dict = {new_keys[key]:value for key,value in parameter_object.items()}
        query_dict['employeeservice__is_retired'] = False
        query_dict['employeeservice__is_current_employee'] = True
        filtered_queryset = Employees.objects.select_related('employeeservice').select_related('employeevote').filter(**query_dict)
        return filtered_queryset

    def get_dashboard_data(self):
        dashboard_data = {}
        dashboard_data['total_employees'] = Employees.objects.count()
        dashboard_data['association_members_count'] =  EmployeeService.dashboard.association_mem_count()
        dashboard_data['union_members_count'] =  EmployeeService.dashboard.union_mem_count()
        dashboard_data['no_membership_count'] =  EmployeeService.dashboard.no_membership_count()
        dashboard_data['deshabhimani_mem_count'] = EmployeeVote.dashboard.deshabhimani_mem_count()
        dashboard_data['deshabhimani_sub_amount'] = EmployeeVote.dashboard.deshabhimani_sub_amount()

        #retirement dues
        dashboard_data['retire_due_employees'] = EmployeeService.dashboard.mark_retirement()

        #upcomig retirement
        dashboard_data['upcoming_retirements'] = EmployeeService.dashboard.upcoming_retirements()

 
        dashboard_data['activities'] = Activities.get_activities()

        return dashboard_data
    
    def __str__(self):
        return self.name 


class EmployeeService(models.Model):

    MEMBERSHIP_CHOICES = (
        ("Association", "Association"),
        ("Union", "Union"),
        ("Neutral", "Neutral"),
    )

    employee = models.OneToOneField(Employees, on_delete=models.CASCADE, primary_key=True,)
    designation = models.CharField(max_length=50)
    department = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    membership = models.CharField(
                    max_length = 30,
                    choices = MEMBERSHIP_CHOICES,
                    default = 'Neuatral'
    )
    date_of_entry = models.DateField(null=True)
    date_of_retire = models.DateField(null=True)
    is_retired =  models.BooleanField(default=False)
    is_current_employee =  models.BooleanField(default=True)
    exit_remark = models.CharField(max_length=50, default="Retired")

    objects = models.Manager()
    dashboard = DashboardManager()
    

    def __str__(self):
        return '{0} - {1}'.format(self.employee, self.department) 

class EmployeeVote(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE, primary_key=True,)
    legislative_assembly = models.CharField(max_length=30)
    loksabha_constituency = models.CharField(max_length=30)
    voters_id = models.CharField(max_length=30)
    deshabhimani_sub = models.CharField(default="No Sub", max_length=30)
    subscription_amount = models.CharField(max_length=20)

    def __str__(self):
        return '{} - Vote'.format(self.employee) 
    
    dashboard = VoteManager()

class Activities(models.Model):
    activity = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True)


    @classmethod
    def mark_activity(cls, activity_string):
        cls.objects.create(activity = activity_string)
    
    @classmethod
    def get_activities(cls):
        return cls.objects.values('activity', 'datetime').order_by('-id')[:10]

    
