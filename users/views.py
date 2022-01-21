from typing import Any
from hotfix.tasks import send
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.views.generic import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from companies.serializers import *
from users.serializers import *
from .serializers import LoginSerializer
from .serializers import RegistrationSerializer
from django.db.models import Q, F
from rest_framework.decorators import api_view


# Create your views here.
class BaseView(View):
    def get(self):
        return HttpResponse("Добро пожаловать!")


class PersonalDataList(viewsets.ModelViewSet):
    serializer_class = PersonalDataSerializer
    queryset = PersonalData.objects.all()


class EmloyeesList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(instance=employees, many=True)
        return Response(serializer.data)


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request: HttpRequest) -> Any:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: HttpRequest) -> Any:
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = Employee.objects.get(username=request.data["username"])
        send.delay(employee.email)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def period_of_times_companies(request: HttpRequest):
    if request.method == "GET":
        date1, date2 = request.GET.get("date1", ""), request.GET.get("date2", "")
        companies = Company.objects.filter(
            Q(created_at__gt=date1) & Q(created_at__lt=date2) & Q(updated_at__lt=date2)
        ).latest("updated_at")
        serializer = CompanySerializer(instance=companies)
        serializer_all = CompanySerializer(instance=Company.objects.all(), many=True)
        data = {
            "data": serializer.data,
            "date1": date1,
            "date2": date2,
            "all": serializer_all.data,
        }
        return Response(data)


@api_view(["POST"])
def salary_increase_transaction(request: HttpRequest) -> Any:
    if request.method == "POST":
        ser = BirthdaySerializer(request.POST)
        print(ser.data["date"])
        employees = PersonalData.objects.filter(date_of_birth=request.POST.data["date"])
        with transaction.atomic:
            for employee in employees:
                employee.update(salary=F("salary") + ser.data["number"])
        serializer = PersonalDataSerializer(instance=employees, many=True)
        data = {"data": serializer.data, "ser": ser.data}
        return Response(data)


@api_view(["POST"])
def salary_increase_f(request) -> Any:
    if request.method == "POST":
        ser = BirthdaySerializer(request.POST)
        PersonalData.objects.filter(date_of_birth=ser.data["date"]).update(salary=F("salary") + ser.data["number"])
        serializer = PersonalDataSerializer(
            instance=PersonalData.objects.filter(date_of_birth=ser.data["date"]),
            many=True,
        )
        s = PersonalDataSerializer(instance=PersonalData.objects.all(), many=True)
        data = {"data": serializer.data, "ser": ser.data, "s": s.data}
        return Response(data)


@api_view(["POST"])
def companies_creation(request) -> Any:
    serializer = CompanySerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
    return Response({"ser": serializer.data})


@api_view(["GET"])
def get_employees() -> Any:
    qs2 = Employee.objects.order_by("company_id", "-date_joined").distinct("company_id")
    serializer = EmployeeSerializer(instance=qs2, many=True)
    return Response(serializer.data)


class FullEmployeeView(viewsets.ModelViewSet):
    serializer_class = EmployeeProfileSerializer
    queryset = Employee.objects.all()


@api_view(["GET"])
def full_employees():
    # serializer = EmployeeProfileSerializer(request.data, many=True)
    # serializer.save()
    employees = Employee.objects.all()
    serializer = EmployeeProfileSerializer(instance=employees, many=True)
    return Response(serializer.data)
