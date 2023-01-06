from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.UUIDField(read_only=True)
        model = Transaction
        fields = [
            "name",
            "type",
            "date",
            "description",
            "value",
            "category_id",
            "id",
        ]
        depth = 1
