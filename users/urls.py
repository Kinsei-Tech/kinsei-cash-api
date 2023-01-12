from django.urls import path, include
from . import views
from .views import ChangePasswordView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<uuid:pk>/", views.UserDetailView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
]
