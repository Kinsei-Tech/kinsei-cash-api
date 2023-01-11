from .serializers import CategorySerializer
from .models import Category
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics


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

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    
