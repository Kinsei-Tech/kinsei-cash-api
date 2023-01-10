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

        try:
            category = Category.objects.get(
                name=category_value, user=request.user)
        except Category.DoesNotExist:
            category_value = {"name": category_value}
            category = CategorySerializer(data=category_value)
            category.is_valid(raise_exception=True)
            category.save(user=request.user)
        serializer = TransactionSerializer(data=new_data_csv, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            category_id=category.data['id'], user=self.request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
        # return Response({"msg": "extract successfully added"}, status.HTTP_201_CREATED)


class TransactionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        category_value = self.request.data.get("category", False)
        if category_value:
            category = Category.objects.get(
                name=category_value, user=request.user)
            self.request.data.update({"category": category})
        else:

            return Response(
                {"msg": "Missing category field"}, status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """getUser = User.objects.get()
        numberFloat = float(self.request.data["value"])
        if getUser:
            if self.request.data["type"] == "cashin":
                getUser.current_balance = float(
                    getUser.current_balance) + numberFloat
                getUser.save()
            else:
                getUser.current_balance = float(
                    getUser.current_balance) - numberFloat
                getUser.save() """
        user_value = self.request.user
        category = self.request.data.get("category")
        serializer.save(category=category, user=user_value)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def update(self, request, *args, **kwargs):
        category_value = self.request.data.get("category", False)
        if category_value:
            category = Category.objects.get_or_create(name=category_value)[0]
            self.request.data.update({"category": category})
        else:
            return Response(
                {"msg": "Missing category field"}, status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        user_value = self.request.user
        category = self.request.data.get("category")
        serializer.save(category=category, user=user_value)
