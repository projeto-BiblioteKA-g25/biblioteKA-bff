from rest_framework.generics import ListCreateAPIView
from .models import User
from books.models import Book
from copies.models import Copy
from .serializers import UserSerializer, SendEmailSerializer
from django.shortcuts import get_object_or_404
from .permissions import (
    IsAccountOwnerOrEmployee,
    IsAccountEmployeExceptPost,
    IsAccountOwner,
)
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import extend_schema


class UserView(ListCreateAPIView):
    permission_classes = [IsAccountEmployeExceptPost]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="user_post",
        description="Rota para criar um usuário sem necessidade de autenticação | token",
        summary="Criar usuário",
        tags=["users"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="users_get",
        description="Rota para listar usuários sem necessidade de autenticação | token",
        summary="Listar usuários",
        tags=["users"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAccountOwnerOrEmployee]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="user_get_id",
        description="Rota para capturar um usuário sendo necessáio que o usuário esteja autenticado | token e com permissão de acesso",
        summary="Capturar usuário por ID",
        tags=["users"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="user_delete_id",
        description="Rota para excluir um usuário sendo necessáio que o usuário esteja autenticado | token e com permissão de acesso. Sendo assim este usuário pode ser o dono da conta ou um empregado com autonimia para realizar a exclusão",
        summary="Excluir usuário por ID",
        tags=["users"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserBookView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="user_retrive_books_by_id",
        description="Rota capturar os dados de usuários assosciados aos livros que estão sob seus cuidados.  Para isso é necessário que o usuário esteja autenticado | token e com permissão de acesso. Sendo assim este usuário precisa ser o dono da conta",
        summary="Capturar usuário por ID associado aos livros",
        tags=["users"],
        exclude=True,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="user_update_books_by_id",
        description="Rota atualizar os dados de usuários assosciados aos livros que estão sob seus cuidados.  Para isso é necessário que o usuário esteja autenticado | token e com permissão de acesso. Sendo assim este usuário precisa ser o dono da conta",
        summary="Atualizar usuário por ID associado aos livros",
        tags=["users"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.request.user
        following = self.request.data.pop("following")
        for id in following:
            book = get_object_or_404(Book, id=id)
            user.following.add(book)

            copy = get_object_or_404(Copy, book=book)
            
            if copy.avaliable:

                subject = 'O seu livro favorito está disponível para empréstimo!'
                message = f'O livro "{book.title}" agora está disponível para empréstimo! Dirija-se à BiblioteKA para garantir a sua cópia.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, from_email,
                          recipient_list, fail_silently=False)

        serializer.save()

    @extend_schema(
        operation_id="user_delete_books_by_id",
        description="Rota excluir os dados de usuários assosciados aos livros que estão sob seus cuidados.  Para isso é necessário que o usuário esteja autenticado | token e com permissão de acesso. Sendo assim este usuário precisa ser o dono da conta",
        summary="Excluir usuário por ID associado aos livros",
        tags=["users"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        user = self.request.user
        following = self.request.data.pop("following")
        for id in following:
            books = get_object_or_404(Book, id=id)
            user.following.remove(books)

    @extend_schema(
        operation_id="user_retrive_put",
        description="Rota para alterar todos os dados de um usuário específico através de sua ID (pk). É necessário ter autenticação | token e permissão. O usuário que realizar a exclusão precisa ser admin ou o usuário que é dono da conta",
        summary="Alterar todos os dados de um usuários específico por ID",
        tags=["users"],
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
