from rest_framework import serializers
from .models import Transaction
from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "List Transactions Example",
            value={
                "name": "Bolacha",
                "type": "cashout",
                "date": "2023-01-11T21:58:32.804Z",
                "description": "My description",
                "value": "8.50",
                "category": "food",
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            },
        ),
        OpenApiExample(
            "Post Transaction Example",
            value={
                "name": "Bolacha",
                "type": "cashout",
                "date": "2023-01-11T21:58:32.804Z",
                "description": "My description",
                "value": "8.50",
                "category": "food",
            },
        ),
        OpenApiExample(
            "Request Patch Transaction Example",
            value={
                "name": "Bolacha Trakinas",
                "type": "cashin",
                "description": "My description 2",
                "value": "20.50",
                "category": "food",
            },
        ),
        OpenApiExample(
            "Response Patch Transaction Example",
            value={
                "name": "Bolacha Trakinas",
                "type": "cashin",
                "description": "My description 2",
                "value": "20.50",
                "category": "food",
                "user_id": "359f99b2-2c14-4666-b275-ca1f5dc3a504",
                "id": "9decf24d-c8b8-4ba7-bd51-b8b54b64a011",
            },
        ),
    ]
)
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
