from rest_framework.generics import ListCreateAPIView
from .models import User
from books.models import Book
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .permissions import (
    IsAccountOwnerOrEmployee,
    IsAccountEmployeExceptPost,
    IsAccountOwner,
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
    permission_classes = [IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        user = self.request.user
        following = self.request.data.pop("following")
        for id in following:
            books = get_object_or_404(Book, id=id)
            user.following.add(books)
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        following = self.request.data.pop("following")
        for id in following:
            books = get_object_or_404(Book, id=id)
            user.following.remove(books)
