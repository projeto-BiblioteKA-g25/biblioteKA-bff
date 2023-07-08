from books.models import Book
from users.permissions import IsAccountEmployeeExceptGet, IsAccountEmployee
from .serializers import CopySerializer
from .models import Copy
from rest_framework import generics
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


class CopyView(generics.ListCreateAPIView):
    permission_classes = [IsAccountEmployeeExceptGet]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    @extend_schema(
        operation_id="copy_post",
        description="Rota para registrar a disponibilidade de um exemplar (cópia) de um livro. Para isso o usuário precisa estar autenticado como empregado",
        summary="Registrar disponibilidade de um exemplar (livro)",
        tags=["copies"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        pk = self.request.data.pop("book")
        book = get_object_or_404(Book, pk=pk)
        serializer.save(book=book)

    @extend_schema(
        operation_id="copy_get",
        description="Rota para obter todos os exemplares (cópias) dos livros contendo o status atual de sua disponibilidade. Para isso o usuário não precisa de autenticação nem de permissão, sendo assim, qualquer pessoa pode acessar essa rota",
        summary="Verificar disponibilidade de todos os livros",
        tags=["copies"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CopyDetailView(generics.UpdateAPIView):
    permission_classes = [IsAccountEmployee]
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    @extend_schema(
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="copy_update_id",
        description="Rota para atualizar qualquer campo de um exemplar (cópia) de um livro específico por ID, contendo o status atual de sua disponibilidade. Para isso o usuário  precisa de autenticação e ter permissão de empregado para realizar as alterações",
        summary="Atualizar dados de copies",
        tags=["copies"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
