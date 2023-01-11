from transactions.models import Transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from tests.factories import create_user_with_token

User: AbstractUser = get_user_model()


def create_transaction(
    user: AbstractUser = None,
    transaction_data: dict = None,
) -> Transaction:

    if not user:
        user, user_token = create_user_with_token()

    if not transaction_data:
        transaction_data = {
            "type": "cashout",
            "name": "aluguel",
            "value": 1500,
            "category": "house_bills",
        }

    transaction = Transaction.objects.create(**transaction_data, user=user)

    return transaction
