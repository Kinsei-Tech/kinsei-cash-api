from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Transaction
        fields = [
            "name",
            "type",
            "date",
            "description",
            "value",
            "category",
            "user_id",
            "id",
        ]
        depth = 1
