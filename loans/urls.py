from django.urls import path
from .views import LoanView, LoanDatailsView

urlpatterns = [
    path("loans/", LoanView.as_view()),
    path("loans/<int:pk>/", LoanDatailsView.as_view()),
]
