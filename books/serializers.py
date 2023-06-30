from rest_framework import serializers
from .models import Book
# from users.serializers import UserSerializer

class BookSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "publishing_date",
            "author",
            "pages"       
        ]
    
    # def get_user(self, obj):
    #     user = obj.user
    #     serializer = UserSerializer(user)
    #     return serializer.data
    
    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book
