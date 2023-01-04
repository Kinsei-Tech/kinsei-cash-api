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
            "id",
        ]

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)
