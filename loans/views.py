from datetime import datetime, timedelta
from rest_framework import generics
from .models import Loan
from copies.models import Copy
from books.models import Book
from users.models import User
from .serializers import LoanSerializer
from .exceptions import (
    SuspendedUserError,
    CopyUnavailableError,
    UserIsBlockedError,
)
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsAccountOwnerOrEmployee, IsAccountEmployee
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import extend_schema


class LoanView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @extend_schema(
        operation_id="loans_get",
        description="Rota para listar livros emprestados empréstimos. Não é necessário ter autenticação | token e permissão",
        summary="Listar empréstimos",
        tags=["loans"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LoanCreateView(generics.CreateAPIView):
    permission_classes = [IsAccountEmployee]
    authentication_classes = [JWTAuthentication]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @extend_schema(
        operation_id="loan__copy_post_id",
        description="Rota para registrar um empréstimo de livro de acordo com a disponilidade (avaliable) registrada na entidade copy é preciso fornnecer o ID do livro na rota. É necessário ter autenticação | token e permissão de emppregado",
        summary="Registrar empréstimo de livro por ID conforme disponibilidade",
        tags=["loans"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        date_now = datetime.now().date()
        date_return = date_now + timedelta(days=5)

        if date_return.weekday() == 5:
            date_return = date_return + timedelta(days=2)
        elif date_return.weekday() == 6:
            date_return = date_return + timedelta(days=1)

        user = self.request.user

        if user.is_blocked:
            raise SuspendedUserError(
                f"this user is suspended until date {user.block_end_date}"
            )

        copy = get_object_or_404(Copy, pk=self.kwargs["pk"])

        book = Book.objects.get(pk=copy.book.id)

        if book.quantity == 0:
            copy.avaliable = False
            book.save()
            raise CopyUnavailableError("This book copy is unavailable")

        else:
            book.quantity -= 1
            book.save()

            serializer.save(return_date=date_return, user=user, copy=copy)


class LoanDetailView(generics.UpdateAPIView):
    permission_classes = [IsAccountOwnerOrEmployee]
    authentication_classes = [JWTAuthentication]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @extend_schema(
        operation_id="loan_update_id",
        description="Rota para atualizar dados de um retorno de um empréstimo de livro, além disso, é necessário passar o ID do empréstimo na rota. É necessário ter autenticação | token e permissão de dono (estudante) ou empregado",
        summary="Atualizar empréstimo de livro por ID",
        tags=["loans"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="loan_update_total_id",
        description="Rota para atualizar todos os dados de um empréstimo de livro. É necessário ter autenticação | token e permissão de dono (estudante) ou empregado",
        summary="Atualizar todos os campos de empréstimo de livro",
        tags=["loans"],
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        loan = get_object_or_404(Loan, pk=self.kwargs["pk"])
        book = Book.objects.get(pk=loan.copy.book.id)
        copy = Copy.objects.get(pk=loan.copy.id)
        user = User.objects.get(pk=loan.user.id)

        date_now = datetime.now().date()
        date_return = loan.return_date
        block_end_date = date_now + timedelta(days=3)

        if date_now > date_return:
            if not user.is_blocked:
                user.is_blocked = True
                user.block_end_date = block_end_date
                user.save()

            pending_loans = Loan.objects.filter(user=user, status=False).exists()

            if not pending_loans:
                additional_block_days_after_return = 5
                user.block_end_date += timedelta(
                    days=additional_block_days_after_return
                )
                user.save()

            raise UserIsBlockedError(
                "This user can not borrow any books for at least 5 more days"
            )

        book.quantity += 1
        book.save()

        copy.avaliable = True
        copy.save()

        loan.status = True
        loan.save()

        if copy.avaliable:
            if book in user.following:
                subject = "O seu livro favorito está disponível para empréstimo!"
                message = f'O livro "{book.title}" agora está disponível para empréstimo! Dirija-se à BiblioteKA para garantir a sua cópia.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(
                    subject, message, from_email, recipient_list, fail_silently=False
                )


class LoanUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrEmployee]
    serializer_class = LoanSerializer

    @extend_schema(
        operation_id="loans_by_user_get_id",
        description="Rota para listar todos os empréstimos de livros realizados por um usuário específico. Para isso, é necessário passar o ID do usuário na rota. É necessário ter autenticação | token e permissão de dono (estudante) ou empregado",
        summary="Listar empréstimo de livros por ID de usuário",
        tags=["loans"],
    )
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        self.check_object_permissions(request, user)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return Loan.objects.filter(user=user)
