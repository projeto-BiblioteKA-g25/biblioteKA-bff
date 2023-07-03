from rest_framework import serializers
from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        book_id = BookSerializer(read_only=True)

        model = Copy
        fields = ["id", "quantity", "avaliable", "book_id"]
