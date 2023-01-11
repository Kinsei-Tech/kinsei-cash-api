from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

User: AbstractUser = get_user_model()


def create_user_with_token(user_data=None) -> tuple[AbstractUser, RefreshToken]:
    if not user_data:
        user_data = {
            "name": "Laís Bomtempo",
            "username": "laissm",
            "email": "lais_bomtempo@mail.com",
            "password": "1234",
            "total_balance": 5000,
            "goal_balance": 1000,
        }

    user = User.objects.create_user(**user_data)
    user_token = RefreshToken.for_user(user)

    return user, user_token
