from rest_framework import serializers
from .models import User
from transactions.models import Transaction


class UserSerializer(serializers.ModelSerializer):

    is_healthy = serializers.SerializerMethodField("get_is_healthy")
    current_balance =serializers.SerializerMethodField("get_current_balance")

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
            "is_healthy": {"read_only": True},
            "current_balance": {"read_only": True}
        }


    def get_current_balance(self, obj: User):
        listTransactions = Transaction.objects.filter(user_id=obj.id)
        current_balance = "0.00"
        if float(obj.total_balance) > 0:
            current_balance = obj.total_balance
        for transaction in listTransactions:
            if transaction.type == "cashin":
                current_balance += transaction.value
            else:
                current_balance -= transaction.value
        return str(current_balance)


    def get_is_healthy(self, obj: User):
        if float(self.get_current_balance(obj)) >= float(obj.goal_balance):
            return True
        else:
            return False


    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


    def update(self, instance: User, validated_data: dict) -> User:
        if "total_balance" in validated_data:
            del validated_data["total_balance"]
        
        if "password" in validated_data:
            del validated_data["password"]

        instance.save()

        return instance
