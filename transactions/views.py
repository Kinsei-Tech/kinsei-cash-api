from rest_framework.views import APIView, status
from rest_framework.response import Response
import csv
import io
import json
import ipdb
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Transaction
from .serializers import TransactionSerializer
from users.models import User
from categories.serializers import CategorySerializer

from categories.models import Category


def csv_data_handling(csv):
    new_data_csv = []
    for transaction in csv:
        transaction_str = str(transaction).lower().replace("'", '"')
        transaction_dict = json.loads(transaction_str)
        del transaction_dict["identificador"]
        transaction_dict["value"] = transaction_dict.pop("valor")
        transaction_dict["value"] = float(transaction_dict["value"])
        transaction_dict["category"] = "other"
        if transaction_dict["value"] < 0:
            transaction_dict["type"] = "cashout"
        else:
            transaction_dict["type"] = "cashin"
        transaction_dict["date"] = transaction_dict.pop("data")
        transaction_dict["description"] = transaction_dict.pop("descrição")
        name_Find = transaction_dict["description"].find("-")
        transaction_dict["name"] = transaction_dict["description"][0:name_Find]

        new_data_csv.append(transaction_dict)
    return new_data_csv


class ExcelAutoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        doc_request = request.FILES["file"]
        file = doc_request.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(file))
        data_csv = [line for line in reader]
        new_data_csv = csv_data_handling(data_csv)

        category_value = new_data_csv[0]["category"]
        for data in new_data_csv:
            category_value = data["category"]
            try:
                category = Category.objects.get(
                    name=category_value, user=self.request.user)
                getUser = User.objects.get(id=self.request.user.id)
                serializer = TransactionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(category=category, user=getUser)
            except Category.DoesNotExist:
                category_value = {"name": category_value}
                category = CategorySerializer(data=category_value)
                category.is_valid(raise_exception=True)
                category.save(user=self.request.user)
                category_instance = Category.objects.get(
                    id=category.data['id'])
                getUser = User.objects.get(id=self.request.user.id)
                serializer = TransactionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(category=category_instance, user=getUser)

        return Response({"msg": "extract successfully added"}, status.HTTP_201_CREATED)


class TransactionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        category_value = self.request.data.get("category", False)
        if not category_value:
            return Response(
                {"msg": "Missing category field"}, status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        category_value = self.request.data.get("category", False)
        user_value = self.request.user
        try:
            category = Category.objects.get(
                name=category_value, user=self.request.user)
            serializer.save(category=category, user=user_value)
        except Category.DoesNotExist:
            category_value = {"name": category_value}
            category = CategorySerializer(data=category_value)
            category.is_valid(raise_exception=True)
            category.save(user=self.request.user)
            category_instance = Category.objects.get(id=category.data['id'])
            getUser = User.objects.get(id=self.request.user.id)
            numberFloat = float(self.request.data["value"])
            serializer.save(category=category_instance, user=user_value)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def update(self, request, *args, **kwargs):
        category_value = self.request.data.get("category", False)
        if not category_value:
            return Response(
                {"msg": "Missing category field"}, status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        category_value = self.request.data.get("category", False)
        user_value = self.request.user
        try:
            category = Category.objects.get(
                name=category_value, user=self.request.user)
            serializer.save(category=category, user=user_value)
        except Category.DoesNotExist:
            category_value = {"name": category_value}
            category = CategorySerializer(data=category_value)
            category.is_valid(raise_exception=True)
            category.save(user=self.request.user)
            category_instance = Category.objects.get(id=category.data['id'])
            serializer.save(category=category_instance, user=user_value)
