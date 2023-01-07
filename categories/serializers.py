from rest_framework import serializers
import ipdb

from .models import Category

# from transactions.models import Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.UUIDField(read_only=True)
        model = Category
        fields = [
            "id",
            "name",
            "limit",
            "categories_transactions",
            "transactions_value",
        ]
        read_only_fields = ["id", "categories_transactions", "transactions_value"]
        depth = 1

    """def get_transactions_value(self, obj):
        total_transactions_value = 1
        for i in obj.categories_transactions.value:
            total_transactions_value += i
        return total_transactions_value"""

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
