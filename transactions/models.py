import uuid
from django.db import models


class TypeChoice(models.TextChoices):
    cashin = "cashin"
    cashout = "cashout"


class Transaction(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    type = models.CharField(
        choices=TypeChoice.choices,
        default=TypeChoice.cashin,
        max_length=8,
    )
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=256, null=True)
    value = models.FloatField()

    # user = models.ForeignKey(
    #     "users.User",
    #     on_delete=models.CASCADE,
    #     related_name="transactions",
    # )

    # category = models.ForeignKey(
    #     "categories.Category",
    #     on_delete=models.CASCADE,
    #     related_name="categories_transactions",
    # )
