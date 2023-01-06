from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    total_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True)
    current_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    goal_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True)
