from rest_framework import serializers
from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        book = BookSerializer(read_only=True)

        model = Copy
        fields = ["id", "avaliable", "book"]
