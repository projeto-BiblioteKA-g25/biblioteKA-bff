from rest_framework import serializers
from .models import Loan
from copies.serializers import CopySerializer
from users.serializers import UserSerializer


class LoanSerializer(serializers.ModelSerializer):
    copy = CopySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "loan_date",
            "return_date",
            "status",
            "copy",
            "user",
        ]
        extra_kwargs = {
            "loan_date": {"read_only": True},
            "return_date": {"read_only": True},
            "status": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Loan:
        return Loan.objects.create(**validated_data)
