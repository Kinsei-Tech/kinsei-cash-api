from .serializers import CategorySerializer
from .models import Category
from transactions.models import Transaction
from .permissions import IsAccountOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_list_or_404


class CategoryView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, *args, **kwargs):
        route_parameter = self.request.query_params.get("is_healthy", False)
        expense = self.request.query_params.get("expense", False)
        user_categories = Category.objects.filter(user=self.request.user)
        serializer = self.serializer_class(user_categories, many=True)

        if route_parameter == "True" or route_parameter == "False":
            validacao = route_parameter == "True"
            lista = [category for category in serializer.data if category.get(
                "is_healthy") == validacao]
            return Response(lista)

        if expense == "higher":
            lista = [category for category in serializer.data]
            category_order = sorted(
                lista, key=lambda category: category['total_expenses_category'])
            return Response(category_order[-1])

        if expense == "lower":
            lista = [category for category in serializer.data]
            category_order = sorted(
                lista, key=lambda category: category['total_expenses_category'])
            return Response(category_order[0])

        return super().list(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ResetCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    def delete(self, request: Request, pk) -> Response:
        transactions = get_list_or_404(Transaction, category_id=pk)

        for transaction in transactions:
            self.check_object_permissions(request, transaction)
            transaction.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
