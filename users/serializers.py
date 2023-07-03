from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from books.serializers import BookSerializer


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password',
                  'employee', 'is_active', 'block_end_date']
        extra_kwargs = {
            'username': {'validators': [UniqueValidator(queryset=User.objects.all(), message='A user with that username already exists.')]},
            'email': {'validators': [UniqueValidator(queryset=User.objects.all())]},
            'password': {'write_only': True}
        }
