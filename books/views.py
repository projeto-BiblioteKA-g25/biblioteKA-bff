from .models import Book
from .serializers import BookSerializer
from rest_framework import generics
from users.permissions import IsAccountEmployeeExceptGet
from drf_spectacular.utils import extend_schema


class BookView(generics.ListCreateAPIView):
    permission_classes = [
        IsAccountEmployeeExceptGet,
    ]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(
        operation_id="book_post",
        description="Rota para registrar um livro com necessidade de autenticação | token e permissão de empregado, sendo assim, o usuário deverá ser um empregado",
        summary="Registrar um livro",
        tags=["books"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="books_get",
        description="Rota para listar todos os livros sem necessidade de autenticação | token e permissão de usuário, nesse sentido, qualquer pessoa poderá acessar essa rota",
        summary="Listar todos os livros",
        tags=["books"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAccountEmployeeExceptGet,
    ]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(
        exclude=True,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="book_update_id",
        description="Rota para atualizar qualquer campo de um livro específico por ID. Há necessidade de autenticação | token e permissão de empregado, nesse sentido, somente o empregado poderá acessar essa rota",
        summary="Atualizar dados de um livro por ID",
        tags=["books"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="book_delete_id",
        description="Rota para excluir um livro específico por ID. Há necessidade de autenticação | token e permissão de empregado, nesse sentido, somente o empregado poderá acessar essa rota",
        summary="Excluir um livro por ID",
        tags=["books"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
