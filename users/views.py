from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework import generics, status
from .permissions import IsAccountOwner
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    serializer_class = UserSerializer
    queryset = User.objects.all()


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status:": "sucess",
                "code": status.HTTP_200_OK,
                "message": "Password updated sucessfully",
                # "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendFormEmail(View):
    def get(self, request):

        # Get the form data
        name = request.GET.get("name", None)
        email = request.GET.get("email", None)
        message = request.GET.get("message", None)

        # Send Email
        send_mail(
            "Subject - Django Email Testing",
            "Hello " + name + ",\n" + message,
            "sender@example.com",  # Admin
            [
                email,
            ],
        )

        # Redirect to same page after form submit
        messages.success(request, ("Email sent successfully."))
        return redirect("home")
