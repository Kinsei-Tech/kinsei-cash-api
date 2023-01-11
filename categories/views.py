from .serializers import CategorySerializer
from .models import Category
from transactions.models import Transaction
from .permissions import IsAccountOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_list_or_404


class CategoryView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)

    
    # def get_queryset(self):
    #     route_parameter = self.request.GET.get("categories_transactions")

    #     if route_parameter:
    #         queryset = Category.objects.filter(is_healtry=True)
    #         return queryset
        
    #     return super().get_queryset()


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
