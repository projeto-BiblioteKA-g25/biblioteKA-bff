from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "employee",
            "is_blocked",
            "block_end_date",
            "following",
        ]

        extra_kwargs = {
            "following": {"read_only": True},
            "password": {"write_only": True},
            "is_blocked": {"read_only": True},
            "block_end_date": {"read_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email": {
                "validators": [
                    UniqueValidator(queryset=User.objects.all()),
                ],
            },
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    recipient_list = serializers.ListField()
