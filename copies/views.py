from .models import Copy
from books.models import Book
from .serializers import CopySerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

# from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Create your views here.
class CopyView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        pk = self.request.data.pop("book")
        book = get_object_or_404(Book, pk=pk)
        serializer.save(book=book)
