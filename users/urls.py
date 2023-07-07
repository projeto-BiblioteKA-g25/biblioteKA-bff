from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("users/login/", views.UserLoginView.as_view()),
    path("users/<int:pk>/books/", views.UserBookView.as_view()),
]
