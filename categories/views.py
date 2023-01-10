from .serializers import CategorySerializer
from .models import Category
from transactions.models import Transaction
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


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    
class ResetCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request: Request, pk ) -> Response:
        transactions = get_list_or_404(Transaction, category_id = pk)

        for transaction in transactions:
            self.check_object_permissions(request, transaction)
            transaction.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    

        