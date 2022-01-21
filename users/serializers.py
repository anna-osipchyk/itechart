from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateModel
        fields = ["updated_at", "created_at"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=2,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # class LoginSerializer(serializers.Serializer):
    #     """
    #     Authenticates an existing user.
    #     Email and password are required.
    #     Returns a JSON web token.
    #     """
    #     username = serializers.CharField(max_length=255, write_only=True)
    #     password = serializers.CharField(max_length=128, write_only=True)
    #
    #     # Ignore these fields if they are included in the request.
    #
    #     def validate(self, data):
    #         """
    #         Validates user data.
    #         """
    #         username = data.get('username', None)
    #         password = data.get('password', None)
    #
    #         if username is None:
    #             raise serializers.ValidationError(
    #                 'Username is required to log in.'
    #             )
    #
    #         if password is None:
    #             raise serializers.ValidationError(
    #                 'A password is required to log in.'
    #             )
    #
    #         user = authenticate(username=username, password=password)
    #
    #         if user is None:
    #             raise serializers.ValidationError(
    #                 'A user with this email and password was not found.'
    #             )
    #
    #         if not user.is_active:
    #             raise serializers.ValidationError(
    #                 'This user has been deactivated.'
    #             )
    #
    #         return {
    #             'username': username
    #         }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.

    def validate(self, data):
        def authenticate(username=None, password=None, **kwargs):
            from django.contrib.auth import get_user_model

            UserModel = get_user_model()
            if username is None:
                username = kwargs.get(UserModel.USERNAME_FIELD)
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                UserModel().set_password(password)

        username = data.get("username", None)
        password = data.get("password", None)
        if username is None:
            raise serializers.ValidationError("Username is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")
        user = authenticate(username, password)

        if user is None:
            raise serializers.ValidationError("A user with this email and password was not found.")

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        return {
            "username": user.username,
        }


class EmployeeProfileSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.SerializerMethodField("get_date_of_birth")
    home_address = serializers.SerializerMethodField("get_home_address")
    salary = serializers.SerializerMethodField("get_salary")

    def get_date_of_birth(self, employee):
        return employee.data.date_of_birth

    def get_home_address(self, employee):
        return employee.data.home_address

    def get_salary(self, employee):
        return employee.data.salary

    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        # employee = validated_data.pop('employee')
        date_of_birth = validated_data.pop("date_of_birth")
        home_address = validated_data.pop("home_address")
        salary = validated_data.pop("salary")
        employee = Employee.objects.create(**validated_data)
        PersonalData.objects.create(
            employee=employee,
            salary=salary,
            date_of_birth=date_of_birth,
            home_address=home_address,
        )
        return employee


class BirthdaySerializer(serializers.Serializer):
    date = serializers.DateField()
    number = serializers.IntegerField()


class SelectionSerializer(serializers.Serializer):
    date1 = serializers.DateField()
    date2 = serializers.DateField()


class GetCompaniesSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    latest = serializers.DateField()
