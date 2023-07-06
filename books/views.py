from .models import Book
from .serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from users.permissions import IsAccountEmployeeExceptGet
from drf_spectacular.utils import extend_schema


class BookView(generics.ListCreateAPIView):
    permission_classes = [
        IsAccountEmployeeExceptGet,
    ]
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(
        operation_id="book_post",
        description="Rota para criar um livro sendo necessário autenticação | token e permissão de acesso",
        summary="Criar livro",
        tags=["books"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="books_get",
        description="Rota para listar livros endo necessário autenticação | token e permissão de acesso",
        summary="Listar livros",
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
        operation_id="book_get_id",
        description="Rota para capturar um livro específico por ID  sendo necessário autenticação | token e permissão de acesso",
        summary="Listar livro por ID",
        tags=["books"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="book_put_id",
        description="Rota para atualizar todos os dados de um livro específico por ID sendo necessário autenticação | token e permissão de acesso",
        summary="Atualizar todos os dados do livro por ID",
        tags=["books"],
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="book_update_id",
        description="Rota para atualizar os dados de um livro específico por ID sendo necessário autenticação | token e permissão de acesso",
        summary="Atualizar livro por ID",
        tags=["books"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="book_delete_id",
        description="Rota para excluir um livro específico por ID sendo necessário autenticação | token e permissão de acesso",
        summary="Excluir livro por ID",
        tags=["books"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
