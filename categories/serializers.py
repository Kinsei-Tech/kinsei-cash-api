from rest_framework import serializers
import ipdb

from .models import Category
from transactions.models import Transaction

from transactions.models import Transaction


class CategorySerializer(serializers.ModelSerializer):

    is_healthy = serializers.SerializerMethodField()
    money_available_category = serializers.SerializerMethodField()

    class Meta:
        id = serializers.UUIDField(read_only=True)
        model = Category
        fields = [
            "id",
            "name",
            "limit",
            "categories_transactions",
            "money_available_category",
            "is_healthy",
        ]
        read_only_fields = [
            "id",
            "categories_transactions",
            "money_available_category",
            "is_healthy",
        ]
        extra_kwargs = {
            "is_healthy": {"read_only": True},
            "money_available_category": {"read_only": True},
        }
        depth = 1

    def get_money_available_category(self, obj: Category):
        transactions = Transaction.objects.all()
        total_value = 0
        if obj.limit == 0:
            return "Please define a limit first, so we can know how much money do you still have available in this category."
        else:
            for i in transactions:
                if i.category_id == obj.id and i.type == "cashin":
                    total_value += i.value
                elif i.category_id == obj.id and i.type == "cashout":
                    total_value -= i.value
            return obj.limit + total_value

    def get_is_healthy(self, obj: Category):
        if (
            type(self.get_money_available_category(obj)) == str
            or float(self.get_money_available_category(obj)) >= 0
        ):
            return True
        else:
            return False

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
