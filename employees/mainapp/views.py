from django.shortcuts import render, HttpResponse
from django.views.generic import *
# Create your views here.
class BaseView(View):
    def get(self, request):
        return HttpResponse('Добро пожаловать!')