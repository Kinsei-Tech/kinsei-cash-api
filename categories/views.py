# from .serializers import CategorySerializer
# from .models import Category
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework import generics


# class CategoryView(generics.ListCreateAPIView):
#    authentication_classes = [JWTAuthentication]
#    permission_classes = [IsAuthenticatedOrReadOnly]
#    serializer_class = CategorySerializer
#   queryset = Category.objects.all()

#    def perform_create(self, serializer):
#        return serializer.save(transaction_id=self.request.user.id)
