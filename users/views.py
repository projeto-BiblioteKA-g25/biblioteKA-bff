from rest_framework.generics import ListCreateAPIView
from .models import User
from books.models import Book
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .permissions import (
    IsAccountOwnerOrEmployee,
    IsAccountEmployeExceptPost,
)
from rest_framework import generics


class UserView(ListCreateAPIView):
    permission_classes = [IsAccountEmployeExceptPost]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAccountOwnerOrEmployee]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserBookView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        pk = self.kwargs.get("pk")
        get_user = get_object_or_404(User, pk=pk)
        user = UserSerializer(instance=get_user).data

        following = self.request.data.pop("following")

        for id in following:
            books = get_object_or_404(Book, id=id)
            get_user.following.add(books)

        serializer.save()
