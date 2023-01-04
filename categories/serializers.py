from rest_framework import serializers


from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "limit", "is_healthy", "transactions"]
        read_only_fields = ["id", "transactions"]

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
