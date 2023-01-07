from rest_framework import serializers
import ipdb

from .models import Category

# from transactions.models import Transaction


class CategorySerializer(serializers.ModelSerializer):

    is_healthy = serializers.SerializerMethodField("get_is_healthy")
    class Meta:
        id = serializers.UUIDField(read_only=True)
        model = Category
        fields = [
            "id",
            "name",
            "limit",
            "categories_transactions",
            "transactions_value",
            "is_healthy",
        ]
        read_only_fields = [
            "id",
            "categories_transactions",
            "transactions_value",
            "is_healthy",
        ]
        extra_kwargs = {"is_healthy": {"read_only": True}}
        depth = 1

    def get_is_healthy(self, obj: Category):
        if obj.limit <= obj.transactions_value:
            return True
        return False

    """def get_transactions_value(self, obj):
        total_transactions_value = 1
        for i in obj.categories_transactions.value:
            total_transactions_value += i
        return total_transactions_value"""

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
