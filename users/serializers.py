from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from books.serializers import BookSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "employee",
            "is_active",
            "block_end_date",
            "following",
        ]
        extra_kwargs = {
            "following": {"read_only": True},
            "password": {"write_only": True},
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
        deth = 1

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "employee",
            "is_active",
            "block_end_date",
            "following",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
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
        deth = 1

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)
