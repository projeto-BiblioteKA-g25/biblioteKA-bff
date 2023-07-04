from django.urls import path
from .views import LoanView, LoanCreateView, LoanDatailsView

urlpatterns = [
    path("loans/", LoanView.as_view()),
    path("loans/<int:pk>/", LoanCreateView.as_view()),
    path("loans/<int:pk>/back", LoanDatailsView.as_view()),
]
