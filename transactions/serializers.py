from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["name", "type", "date", "description", "value"]

        read_only_fields = {
            "id",
        }

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)
