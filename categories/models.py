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

    name = models.CharField(
        max_length=20, choices=CategoryName.choices, default=CategoryName.other
    )
    limit = models.FloatField(default=0)
    is_healthy = models.BooleanField(default=True)