from rest_framework import serializers
import ipdb
from .models import Category
from transactions.models import Transaction
from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "List Category Example",
            value={
                "id": "f7d17ccf-d44c-4765-826d-036a46fd2d9b",
                "name": "food",
                "limit": "200.00",
                "categories_transactions": [
                    {
                        "id": "1decf24d-c8b8-4ba7-bd51-b8b54b64a011",
                        "name": "Test",
                        "type": "cashout",
                        "date": "2023-01-11T20:00:10.300537Z",
                        "description": "My description",
                        "value": "10.00",
                        "user": "359f99b2-2c14-4666-b275-ca1f5dc3a504",
                        "category": "f7d27ccb-644c-4765-826d-036a46fd2d9b",
                    }
                ],
                "money_available_category": 3000.0,
                "is_healthy": True,
            },
        ),
        OpenApiExample(
            "Update Category Example",
            value={"value": "Put the value here"},
        ),
    ]
)
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
            return "Limit wasn't defined yet. Please define your limit, so we can know how much money do you have available in this category."
        else:
            for i in transactions:
                if i.category_id == obj.id and i.type == "cashout":
                    total_value -= i.value
                elif i.category_id == obj.id and i.type == "cashin":
                    total_value += i.value
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
