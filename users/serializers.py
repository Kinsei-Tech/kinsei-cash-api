from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    is_healthy = serializers.SerializerMethodField("get_is_healthy")

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "password",
            "is_active",
            "total_balance",
            "current_balance",
            "goal_balance",
            "is_healthy"
        ]
        read_only_fields = ['is_active', "current_balance", "is_healthy"]
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "is_healthy": {"read_only": True}
        }

    def get_is_healthy(self, obj: User):
        if obj.current_balance >= obj.goal_balance:
            return True
        return False

    def create(self, validated_data: dict) -> User:
        if "total_balance" in validated_data:
            total_balance = validated_data["total_balance"]
            validated_data["current_balance"] = total_balance
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        if "total_balance" in validated_data:
            del validated_data["total_balance"]

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
