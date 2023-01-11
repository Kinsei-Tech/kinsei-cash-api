from rest_framework.views import APIView, status
from rest_framework.response import Response
import csv
import io
import json
import ipdb
from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Transaction
from .serializers import TransactionSerializer
from users.models import User
from categories.serializers import CategorySerializer
from django.shortcuts import get_object_or_404

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
                getUser = User.objects.get(id=self.request.user.id)
                numberFloat = float(data["value"])
                if getUser:
                    if data["type"] == "cashin":
                        getUser.current_balance = (
                            float(getUser.current_balance) + numberFloat
                        )
                        getUser.save()
                    else:
                        getUser.current_balance = (
                            float(getUser.current_balance) - numberFloat
                        )
                        getUser.save()
                # ipdb.set_trace()
                serializer = TransactionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(category=category, user=getUser)
            except Category.DoesNotExist:
                category_value = {"name": category_value}
                category = CategorySerializer(data=category_value)
                category.is_valid(raise_exception=True)
                category.save(user=self.request.user)
                category_instance = Category.objects.get(id=category.data["id"])
                getUser = User.objects.get(id=self.request.user.id)
                numberFloat = float(data["value"])
                if getUser:
                    if data["type"] == "cashin":
                        getUser.current_balance = (
                            float(getUser.current_balance) + numberFloat
                        )
                        getUser.save()
                    else:
                        getUser.current_balance = (
                            float(getUser.current_balance) - numberFloat
                        )
                        getUser.save()
                #
                serializer = TransactionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(category=category_instance, user=getUser)

        return Response({"msg": "extract successfully added"}, status.HTTP_201_CREATED)


class TransactionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        # high_values = self.kwargs['high_values']
        # ipdb.set_trace()
        if self.request.query_params.get("type", False):
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
            # return self.queryset.filter(type='cashout', user=self.request.user).order_by('-value')[0:high_values]
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        category_value = self.request.data.get("category", False)
        if not category_value:
            return Response(
                {"msg": "Missing category field"}, status.HTTP_400_BAD_REQUEST
            )
        getUser = User.objects.get(id=self.request.user.id)
        numberFloat = float(self.request.data["value"])
        if getUser:
            if self.request.data["type"] == "cashin":
                getUser.current_balance = float(getUser.current_balance) + numberFloat
                getUser.save()
            else:
                getUser.current_balance = float(getUser.current_balance) - numberFloat
                getUser.save()
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        category_value = self.request.data.get("category", False)
        user_value = self.request.user
        try:
            category = Category.objects.get(name=category_value, user=self.request.user)
            getUser = User.objects.get(id=self.request.user.id)
            numberFloat = float(self.request.data["value"])
            if getUser:
                if self.request.data["type"] == "cashin":
                    getUser.current_balance = (
                        float(getUser.current_balance) + numberFloat
                    )
                    getUser.save()
                else:
                    getUser.current_balance = (
                        float(getUser.current_balance) - numberFloat
                    )
                    getUser.save()
            serializer.save(category=category, user=user_value)
        except Category.DoesNotExist:
            category_value = {"name": category_value}
            category = CategorySerializer(data=category_value)
            category.is_valid(raise_exception=True)
            category.save(user=self.request.user)
            category_instance = Category.objects.get(id=category.data["id"])
            getUser = User.objects.get(id=self.request.user.id)
            numberFloat = float(self.request.data["value"])
            if getUser:
                if self.request.data["type"] == "cashin":
                    getUser.current_balance = (
                        float(getUser.current_balance) + numberFloat
                    )
                    getUser.save()
                else:
                    getUser.current_balance = (
                        float(getUser.current_balance) - numberFloat
                    )
                    getUser.save()
            serializer.save(category=category_instance, user=user_value)
        # user_value = self.request.user


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def update(self, request, *args, **kwargs):
        category_value = self.request.data.get("category", False)
        if category_value:
            category = Category.objects.get_or_create(name=category_value, user=self.request.user)[0]
            self.request.data.update({"category": category})

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.request.user
        if self.request.data.get("value", False):
            numberFloat = float(self.request.data["value"])
            if self.request.data["type"] == "cashin":
                user.current_balance = float(user.current_balance) + numberFloat
            else:
                user.current_balance = float(user.current_balance) - numberFloat
            user.save()
            serializer.save(user=user)

    # def perform_update(self, serializer):

    #     category_value = self.request.data.get("category", False)
    #     user_value = self.request.user
    #     try:
    #         # ipdb.set_trace()
    #         category = Category.objects.get(name=category_value, user=self.request.user)
    #         ipdb.set_trace()
    #         if self.request.data.get("value", False):
    #             numberFloat = float(self.request.data["value"])
    #             getUser = User.objects.get(id=self.request.user.id)
    #             if getUser:
    #                 if self.request.data["type"] == "cashin":
    #                     getUser.current_balance = (
    #                         float(getUser.current_balance) + numberFloat
    #                     )
    #                     getUser.save()
    #             else:
    #                 getUser.current_balance = (
    #                     float(getUser.current_balance) - numberFloat
    #                 )
    #                 getUser.save()
    #         serializer.save(category=category, user=user_value)
    #     except Category.DoesNotExist:
    #         category_value = {"name": category_value}
    #         category = CategorySerializer(data=category_value)
    #         category.is_valid(raise_exception=True)
    #         category.save(user=self.request.user)
    #         category_instance = Category.objects.get(id=category.data["id"])
    #         if self.request.data.get("value", False):
    #             getUser = User.objects.get(id=self.request.user.id)
    #             numberFloat = float(self.request.data["value"])
    #             if getUser:
    #                 if self.request.data["type"] == "cashin":
    #                     getUser.current_balance = (
    #                         float(getUser.current_balance) + numberFloat
    #                     )
    #                     getUser.save()
    #             else:
    #                 getUser.current_balance = (
    #                     float(getUser.current_balance) - numberFloat
    #                 )
    #                 getUser.save()
    #         serializer.save(category=category_instance, user=user_value)


""" class TransactionFilterView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        high_values = self.kwargs['high_values']
        ipdb.set_trace()
        if self.request.query_params[hi]:
        if high_values:
            return self.queryset.filter(
                date__gte=datetime.today()-timedelta(days=30), type='cashout', user=self.request.user
            ).order_by('value')[0:high_values]
            return self.queryset.filter(type='cashout', user=self.request.user).order_by('-value')[0:high_values]
        return self.queryset.filter(type='cashout', user=self.request.user).order_by('-value') """
