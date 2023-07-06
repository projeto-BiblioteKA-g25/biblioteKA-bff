from books.serializers import BookSerializer
from books.models import Book
from .serializers import CopySerializer
from .models import Copy
from rest_framework import generics
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

class CopyView(generics.ListAPIView):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    @extend_schema(
        operation_id="copy_post",
        description="Rota para registrar a disponibilidade de um exemplar (cópia) de um livro. Para isso o usuário precisa estar autenticado como empregado",
        summary="Registrar disponibilidade",
        tags=["copies"],
    )

    def perform_create(self, serializer):
        pk = self.request.data.pop("book")
        book = get_object_or_404(Book, pk=pk)
        serializer.save(book=book)

    # def get_book(self, obj):
    #     book = obj.book
    #     serializer = BookSerializer(book)
    #     return serializer.data

    @extend_schema(
        operation_id="copy_get",
        description="Rota para obter todos os exemplares (cópias) dos livros contendo o status atual de sua disponibilidade",
        summary="Verificar disponibilidade de todos os livros",
        tags=["copies"],
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def get_book(self, obj):
        book = obj.book
        serializer = BookSerializer(book)
        return Copy.objects.all(serializer.data) 


class CopyBookByIdView(generics.ListCreateAPIView):
    @extend_schema(
        operation_id="copy_post_id_book",
        description="Rota para registrar a disponibilidade de um exemplar (cópia) através do ID de um livro. Para isso o usuário precisa estar autenticado como empregado",
        summary="Registrar disponibilidade de um livro específico",
        tags=["copies"],
    )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(book=self.kwargs.get("pk"))

    @extend_schema(
        operation_id="copy_get_id_book",
        description="Rota para obter um exemplar (cópia) por ID do livro contendo o status atual de sua disponibilidade",
        summary="Verificar disponibilidade de um livro específico",
        tags=["copies"],
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.employee:
            return Copy.objects.all()

        return Copy.objects.filter(book=self.kwargs.get("pk"))
