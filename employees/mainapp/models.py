from django.db import models


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=30)
    web_site = models.URLField(verbose_name='website')
    email = models.EmailField()
    logo = models.ImageField(upload_to='media/logos')
    post_index = models.IntegerField(verbose_name='post index')

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    job_position = models.CharField(max_length=40, verbose_name='job position')
    is_manager = models.BooleanField(default=False, verbose_name='is manager')
    is_admin = models.BooleanField(default=False, verbose_name='is admin')
    company = models.ForeignKey('Company', related_name='employees', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, verbose_name='phone number')

    class Meta:
        indexes = [
            models.Index(fields=['name', 'surname']),
        ]

    def __str__(self):
        return f'{self.name} {self.surname}'


class PersonalData(models.Model):
    employee = models.OneToOneField('Employee', related_name="data", on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(verbose_name='date of birth')
    home_address = models.CharField(max_length=150, verbose_name="address")
    salary = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.employee.name


class Bank(models.Model):
    name = models.CharField(max_length=30)
    web_site = models.URLField(verbose_name='website')
    email = models.EmailField()

    def __str__(self):
        return self.name


class BankCompany(models.Model):
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, related_name='bank', null=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, related_name='company', null=True)

    def __str__(self):
        return f'{self.bank.name}-{self.company.name}'
