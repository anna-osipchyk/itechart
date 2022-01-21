# users/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from companies.models import Company, DateModel
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Указанное имя пользователя должно быть установлено")

        if not email:
            raise ValueError("Данный адрес электронной почты должен быть установлен")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)

        db_name = settings.DATABASES["default"]["NAME"]
        user.save(using=db_name)
        return user

    def create_user(self, username, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("company_id", 1)
        extra_fields.setdefault("is_authenticated", True)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("company_id", 1)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class Employee(AbstractUser):
    job_position = models.CharField(max_length=40, verbose_name="job position")
    is_manager = models.BooleanField(default=False, verbose_name="is manager")
    company = models.ForeignKey(Company, related_name="employees", on_delete=models.CASCADE, default=1)
    phone_number = models.CharField(max_length=30, verbose_name="phone number")
    objects = UserManager()

    @classmethod
    def user_created(cls, user, request):
        from users.forms import CustomUserCreationForm

        form = CustomUserCreationForm(request.POST)
        user.job_position = form.data.get("job_position", None)
        user.save()
        pass

    class Meta:
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
        ]

    def __str__(self):
        return f"{self.username}"

class PersonalData(DateModel):
    employee = models.OneToOneField(Employee, related_name="data", on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(verbose_name="date of birth")
    home_address = models.CharField(max_length=150, verbose_name="address")
    salary = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.employee.username
