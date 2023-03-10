import uuid
from django.db import models


class TypeChoice(models.TextChoices):
    CASHIN = "cashin"
    CASHOUT = "cashout"


class Transaction(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    type = models.CharField(
        choices=TypeChoice.choices,
        default=TypeChoice.CASHIN,
        max_length=8,
    )
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=256, null=True)
    value = models.DecimalField(max_digits=1000, decimal_places=2, default=0)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.CASCADE,
        related_name="categories_transactions",
    )
