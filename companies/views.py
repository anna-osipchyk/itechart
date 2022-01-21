from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.response import Response

from companies.serializers import *


class CompaniesList(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]


@api_view(http_method_names=['GET'])
def show_bank_list():
    banks = Bank.objects.all()
    serializer = BankSerializer(instance=banks, many=True)
    return Response(serializer.data)
