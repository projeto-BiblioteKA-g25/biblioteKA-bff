from rest_framework.generics import ListCreateAPIView
from .models import User
from books.models import Book
from copies.models import Copy
from .serializers import UserSerializer
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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .exceptions import NotFollowBookError


class UserView(ListCreateAPIView):
    permission_classes = [IsAccountEmployeExceptPost]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="user_post",
        description="Rota para criar um usuário sem necessidade de autenticação | token, podendo ser um empregado ou estudante",
        summary="Criar usuário",
        tags=["users"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="users_get",
        description="Rota para listar usuários com necessidade de autenticação | token. Esta rota é habilitada somente para empregados",
        summary="Listar todos os usuários",
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
        description="Rota para capturar um usuário sendo necessáio que o usuário esteja autenticado | token e com permissão de acesso, sendo assim, é necessário que usuário seja o dono da conta ou seja um empregado.",
        summary="Capturar usuário por ID",
        tags=["users"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="user_delete_id",
        description="Rota para excluir um usuário sendo necessário que o usuário esteja autenticado | token e com permissão de acesso. Sendo assim, o usuário pode ser o dono da conta ou um empregado com autorização para realizar a exclusão",
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
        description="Rota para capturar livros seguidos pelo ID do usuário.  Para isso é necessário que o usuário esteja autenticado | token e com permissão de acesso. Sendo assim este usuário precisa ser o dono da conta",
        summary="Capturar usuário por ID associado aos livros",
        tags=["users"],
        exclude=True,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="user_update_books_by_id",
        description="Rota para seguir livros, sendo necessário a indicação do ID do usuário na URL e no campo 'following' os ID's do livros que serão seguidos. Apenas o usuário poderá acrescentar os livros que deseja seguir no seu campo 'following'. Para isso é necessário que o usuário esteja autenticado | token e com permissão de acesso.",
        summary="Seguir livro por ID associado ao usuário",
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

            copy = Copy.objects.filter(book=book).first()

            if copy and copy.avaliable:
                subject = "O seu livro favorito está disponível para empréstimo!"
                message = f'O livro "{book.title}" agora está disponível para empréstimo! Dirija-se à BiblioteKA para garantir a sua cópia.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(
                    subject, message, from_email, recipient_list, fail_silently=False
                )

        serializer.save()

    @extend_schema(
        operation_id="user_delete_books_by_id",
        description="Rota para excluir os livros que o usuário deseja deixar de seguir.  Para isso é necessário que o usuário esteja autenticado | token e com permissão de acesso. Sendo assim, o usuário precisa ser o dono da conta",
        summary="Excluir livro seguido por ID associado ao usuário",
        tags=["users"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        user = self.request.user
        following = self.request.data.pop("following")
        for id in following:
            book = get_object_or_404(Book, id=id)

            if not book in user.following.all():
                raise NotFollowBookError("You don't follow this book")

            user.following.remove(book)

    @extend_schema(
        operation_id="user_retrive_put",
        description="Rota para seguir livros, sendo necessário a indicação do ID do usuário na URL e no campo 'following' os ID's do livros que serão seguidos. Apenas o usuário poderá acrescentar os livros que deseja seguir no seu campo 'following'. Para isso é necessário que o usuário esteja autenticado | token e com permissão de acesso.",
        summary="Alterar todos os dados de um usuários específico por ID",
        tags=["users"],
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserLoginView(TokenObtainPairView):
    @extend_schema(
        operation_id="user_login_post",
        description="Rota para logar usuários sem necessidade de autenticação | token",
        summary="Logar usuários",
        tags=["login"],
    )
    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
