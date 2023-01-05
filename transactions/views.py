from rest_framework.views import APIView, status
from rest_framework.response import Response
import csv
import io
import json
import ipdb
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.


def csv_data_handling(csv):
    new_data_csv = []
    for transaction in csv:
        transaction_str = str(transaction).lower().replace("'", '"')
        transaction_dict = json.loads(transaction_str)
        del transaction_dict['identificador']
        transaction_dict['value'] = transaction_dict.pop('valor')
        transaction_dict['value'] = float(transaction_dict['value'])
        transaction_dict['category'] = 'other'
        if transaction_dict['value'] < 0:
            transaction_dict['type'] = 'cashout'
        else:
            transaction_dict['type'] = 'cashin'
        transaction_dict['date'] = transaction_dict.pop('data')
        transaction_dict['description'] = transaction_dict.pop(
            'descrição')
        name_Find = transaction_dict['description'].find('-')
        transaction_dict['name'] = transaction_dict['description'][0:name_Find]

        new_data_csv.append(transaction_dict)
    return new_data_csv


class ExcelAutoView(APIView):

    def post(self, request):
        doc_request = request.FILES['file']
        file = doc_request.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        data_csv = [line for line in reader]
        new_data_csv = csv_data_handling(data_csv)

        return Response(new_data_csv)
        
        
class TransactionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = TransactionSerializer
    # queryset = Transaction
    queryset = Transaction.objects.all()

