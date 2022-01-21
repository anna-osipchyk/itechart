# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Employee, PersonalData


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Employee
    list_display = ['username', 'job_position']
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_manager', 'username', 'job_position', 'company', 'phone_number')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'username', 'job_position', 'is_manager', 'company',
                'phone_number')}
         ),
    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email')

    filter_horizontal = ()


admin.site.register(Employee, CustomUserAdmin)
admin.site.register(PersonalData)
