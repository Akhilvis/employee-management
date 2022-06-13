import datetime
from django.db import models

import contactsapp.models

class DashboardManager(models.Manager):
    def association_mem_count(self):
        return self.filter(membership='Association').count()
    
    def union_mem_count(self):
        return self.filter(membership='Union').count()

    def no_membership_count(self):
        return self.filter(membership='Neutral').count()
    
    def mark_retirement(self):
        retire_employees_queyset = self.filter(date_of_retire__lte=datetime.datetime.now(), is_retired=False)
        
        for retired_employee in retire_employees_queyset:
            contactsapp.models.Activities.mark_activity('{name} was retired on {date}'.format(name=retired_employee.employee.name, date=retired_employee.date_of_retire))
        retire_employees_queyset.update(is_retired=True)
       
        return self.filter(is_retired=True).order_by('-date_of_retire')
    
    def upcoming_retirements(self):
        retirement_threshold = datetime.timedelta(days = 32) + datetime.datetime.now()                        
        return self.filter(date_of_retire__lte=retirement_threshold, date_of_retire__gt=datetime.datetime.now())


class VoteManager(models.Manager):
    def deshabhimani_mem_count(self):
        return self.filter(deshabhimani_sub='Yes').count()
    
    def deshabhimani_sub_amount(self):
        subscription_amount = 0
        for mem in self.all():
            try:
                subscription_amount += int(mem.subscription_amount)
            except:
                pass
        return subscription_amount