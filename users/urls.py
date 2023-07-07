from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("sendmail/", views.SendEmailView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/<int:pk>/books/", views.UserBookView.as_view()),
]
