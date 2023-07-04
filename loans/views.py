from datetime import datetime, timedelta
from rest_framework import generics
from .models import Loan
from copies.models import Copy
from books.models import Book
from .serializers import LoanSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .exceptions import SuspendedUserError, CopyUnavailableError
from django.shortcuts import get_object_or_404
from rest_framework.views import Response, status


# Create your views here.
class LoanView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanDatailsView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

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
            book.avaliable = False
            book.save()
            raise CopyUnavailableError("This book copy is unavailable")

        else:
            book.quantity -= 1
            book.save()

            serializer.save(return_date=date_return, user=user, copy=copy)
