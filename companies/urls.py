from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('companies/', views.CompaniesList.as_view(), name='companies-list'),
    path('banks/', views.show_bank_list, name='banks-list'),

]
