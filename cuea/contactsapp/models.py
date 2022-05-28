from django.db import models

class Employees(models.Model):
    pf_number = models.IntegerField()
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=30, default="Male")
    blood_group = models.CharField(max_length=10)
    adddress = models.TextField()
    district = models.CharField(max_length=20)
    pan_mun_cop = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name 


class EmployeeService(models.Model):

    MEMBERSHIP_CHOICES = (
        ("Association", "Association"),
        ("Union", "Union"),
        ("Neuatral", "Neuatral"),
    )

    employee = models.OneToOneField(Employees, on_delete=models.CASCADE, primary_key=True,)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    membership = models.CharField(
                    max_length = 30,
                    choices = MEMBERSHIP_CHOICES,
                    default = 'Neuatral'
                    )
    
    def __str__(self):
        return '{} - Service'.format(self.employee) 

class EmployeeVote(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE, primary_key=True,)
    legislative_assembly = models.CharField(max_length=30)
    loksabha_constituency = models.CharField(max_length=30)
    voters_id = models.CharField(max_length=30)
    deshabhimani_sub = models.BooleanField(default=False)
    subscription_amount = models.IntegerField()

