from rest_framework import serializers
import ipdb

from .models import Category

# from transactions.models import Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "limit", "categories_transactions"]
        read_only_fields = ["id", "categories_transactions"]
        extra_kwargs = {"is_healthy": {"read_only": True}}
        depth = 1

    def get_is_healthy(self, obj: Category):
        ipdb.set_trace()
        return False

        """if obj.limit < transactions_value and obj.limit > 0:
            return False"""

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
