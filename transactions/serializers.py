from rest_framework import serializers

from .models import Transaction

from categories.models import Category
import ipdb


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
            "category_"
            "id",
        ]

    """ def create(self, validated_data):
        ipdb.set_trace()
        return Transaction.objects.create(**validated_data) """
