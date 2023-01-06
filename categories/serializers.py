from rest_framework import serializers


from .models import Category

# from transactions.models import Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "limit",
            "is_healthy",
            "categories_transactions",
            "user",
        ]
        read_only_fields = ["id", "is_healthy", "categories_transactions", "user"]
        depth = 1

    def get_is_healthy(self, obj: Category):
        transactions_value = 1000
        if obj.limit < transactions_value and obj.limit > 0:
            return False

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
