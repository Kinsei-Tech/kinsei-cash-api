import uuid
from django.db import models


class CategoryName(models.TextChoices):
    house_bills = "house bills"
    leisure = "leisure"
    education = "education"
    investment = "investment"
    health = "health"
    travel = "travel"
    self_care = "self_care"
    clothes = "clothes"
    gifts = "gifts"
    transportation = "transportation"
    food = "food"
    donation = "donation"
    other = "other"


class Category(models.Model):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    
    name = models.CharField(
        max_length=20, choices=CategoryName.choices, default=CategoryName.other
    )
    limit = models.FloatField(default=0)
    transactions_value = models.FloatField(default=0)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="category",
    )
