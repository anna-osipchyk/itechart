from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"personal_data", views.PersonalDataList, basename="personal-data-list")

router1 = routers.DefaultRouter()
router1.register(r"full_employees", views.FullEmployeeView, basename="employee")
urlpatterns = router.urls
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("employees/", views.EmloyeesList.as_view(), name="employees-list"),
    path("registration", views.RegistrationAPIView.as_view(), name="user_registration"),
    path("login/", views.LoginAPIView.as_view(), name="user_login"),
    path("qs1/", views.period_of_times_companies),
    path("qs2f/", views.salary_increase_f),
    path("qs2/", views.salary_increase_transaction, name="salary-increase"),
    path("qs3", views.companies_creation, name="company-creation"),
    path("qs4", views.get_employees, name="get-employee"),
    path("full_employee", views.full_employees, name="full-employee"),
] + router1.urls

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
