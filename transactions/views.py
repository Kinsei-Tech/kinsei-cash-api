from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.


class TransactionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = TransactionSerializer
    # queryset = Transaction
    queryset = Transaction.objects.all()
