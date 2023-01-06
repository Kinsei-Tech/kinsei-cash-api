from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_balance =models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    goal_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
