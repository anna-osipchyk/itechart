from rest_framework import serializers
from .models import *


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class CompaniesListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        companies = []
        for item in validated_data:
            name, web_site, post_index = item.get("name"), item.get("web_site"), item.get("post_index")
            company = Company(name=name, web_site=web_site, post_index=post_index)
            companies.append(company)
        obj = Company.objects.bulk_create(companies)
        for company, item in zip(obj, validated_data):
            company.bank.set(item.get("bank"))
        return obj


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        list_serializer_class = CompaniesListSerializer
