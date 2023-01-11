from rest_framework import serializers
import ipdb

from .models import Category
from transactions.models import Transaction

from transactions.models import Transaction


class CategorySerializer(serializers.ModelSerializer):

    is_healthy = serializers.SerializerMethodField("get_is_healthy")
    total_value_category = serializers.SerializerMethodField(
        "get_total_value_category")

    class Meta:
        id = serializers.UUIDField(read_only=True)
        model = Category
        fields = [
            "id",
            "name",
            "limit",
            "categories_transactions",
            "total_value_category",
            "is_healthy",
        ]
        read_only_fields = [
            "id",
            "categories_transactions",
            "total_value_category",
            "is_healthy",
        ]
        extra_kwargs = {
            "is_healthy": {"read_only": True},
            "total_value_category": {"read_only": True},
        }
        depth = 1

    def get_total_value_category(self, obj: Category):
        transactions = Transaction.objects.all()
        total_value = 0
        for i in transactions:
            if i.category_id == obj.id:
                total_value += i.value
        return total_value

    def get_is_healthy(self, obj: Category):
        if (

            float(obj.limit) <= self.get_total_value_category(obj)
            and float(obj.limit) > 0
            and obj.name != "cashin"
        ):

            return False
        elif (
            float(obj.limit) >= self.get_total_value_category(obj)
            and float(obj.limit) > 0
            and obj.name == "cashin"
        ):
            return True
        else:
            return True

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
