from rest_framework.generics import ListCreateAPIView
from .models import User
from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, UserBookSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountUser
from rest_framework import generics


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserBookView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = User.objects.all()
    serializer_class = UserBookSerializer
