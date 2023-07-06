from rest_framework import serializers
from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Copy
        fields = [
            "id",
            "avaliable",
            "book",
        ]

    def get_book(self, obj):
        book = obj.book
        serializer = BookSerializer(book)
        return serializer.data

    def create(self, validated_data):
        copy = Copy.objects.create(**validated_data)
        return copy
