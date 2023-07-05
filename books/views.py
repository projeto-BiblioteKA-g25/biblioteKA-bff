from .models import Book
from .serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from users.permissions import IsAccountEmployeeExceptGet


class BookView(generics.ListCreateAPIView):
    permission_classes = [
        IsAccountEmployeeExceptGet,
    ]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAccountEmployeeExceptGet,
    ]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
