from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from categories.models import Category
from .models import Transaction
from .serializers import TransactionSerializer
from categories.serializers import CategorySerializer
from categories.permissions import IsAccountOwner
from datetime import datetime, timedelta
import csv
import io
import json
import ipdb


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
            transaction_dict["value"] = transaction_dict["value"] * -1
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
                    name=category_value, user=self.request.user
                )
                serializer = TransactionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(category=category, user=request.user)
            except Category.DoesNotExist:
                category_value = {"name": category_value}
                category = CategorySerializer(data=category_value)
                category.is_valid(raise_exception=True)
                category.save(user=self.request.user)
                category_instance = Category.objects.get(
                    id=category.data["id"])
                serializer = TransactionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(category=category_instance, user=request.user)

        return Response({"msg": "extract successfully added"}, status.HTTP_201_CREATED)


class TransactionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        filters = self.request.query_params.get("type", False)

        if filters:
            type_params = self.request.query_params.get("type", False)
            high_params = self.request.query_params.get("high", None)
            lower_params = self.request.query_params.get("lower", None)

            if high_params:
                return self.queryset.filter(
                    date__gte=datetime.today() - timedelta(days=30),
                    type=type_params,
                    user=self.request.user,
                ).order_by("-value")[0: int(high_params)]
            elif lower_params:
                return self.queryset.filter(
                    date__gte=datetime.today() - timedelta(days=30),
                    type=type_params,
                    user=self.request.user,
                ).order_by("value")[0: int(lower_params)]
            else:
                return self.queryset.filter(
                    date__gte=datetime.today() - timedelta(days=30),
                    type=type_params,
                    user=self.request.user,
                ).order_by("-value")[0:]
        return self.queryset.filter(user=self.request.user)

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
            category_instance = Category.objects.get(id=category.data["id"])
            serializer.save(category=category_instance, user=user_value)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsAccountOwner]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def update(self, request, *args, **kwargs):
        category_value = self.request.data.get("category", False)
        if category_value:
            try:
                category = Category.objects.get(
                    name=category_value, user=self.request.user
                )
                self.request.data.update({"category": category})
            except Category.DoesNotExist:
                category_value = {"name": category_value}
                category = CategorySerializer(data=category_value)
                category.is_valid(raise_exception=True)
                category.save(user=self.request.user)
                category_instance = Category.objects.get(
                    id=category.data["id"])
                self.request.data.update({"category": category_instance})
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.data.get("category", False):
            serializer.save(category=self.request.data["category"])
        return serializer.save()
