from .models import Copy
from books.models import Book
from .serializers import CopySerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from users.permissions import IsAccountEmployee


class CopyView(generics.ListCreateAPIView):
    permission_classes = [IsAccountEmployee]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        pk = self.request.data.pop("book")
        book = get_object_or_404(Book, pk=pk)
        serializer.save(book=book)
