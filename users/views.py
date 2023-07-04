from rest_framework.generics import ListCreateAPIView
from .models import User
from books.models import Book
from books.serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .permissions import (
    IsAccountUserOrEmployee,
    IsAccountEmployee,
    IsAccountEmployeeGetUsers,
)
from rest_framework import generics
from rest_framework.response import Response


class UserView(ListCreateAPIView):
    permission_classes = [IsAccountEmployeeGetUsers]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountUserOrEmployee]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserBookView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        pk = self.kwargs.get("pk")
        get_user = get_object_or_404(User, pk=pk)
        user = UserSerializer(instance=get_user).data

        print(self.request.user)
        following = self.request.data.pop("following")

        for id in following:
            books = get_object_or_404(Book, id=id)
            get_user.following.add(books)

        serializer.save()
