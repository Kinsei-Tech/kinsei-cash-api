import uuid
from django.db import models


class CategoryName(models.TextChoices):
    HOUSE_BILLS = "house bills"
    LEISURE = "leisure"
    EDUCATION = "education"
    INVESTMENT = "investment"
    HEALTH = "health"
    TRAVEL = "travel"
    SELF_CARE = "self_care"
    CLOTHES = "clothes"
    GIFTS = "gifts"
    TRANSPORTATION = "transportation"
    FOOD = "food"
    DONATION = "donation"
    OTHER = "other"


class Category(models.Model):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    name = models.CharField(
        max_length=20, choices=CategoryName.choices, default=CategoryName.OTHER
    )
    limit = models.DecimalField(max_digits=1000, decimal_places=2, default=0)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="category",
    )
