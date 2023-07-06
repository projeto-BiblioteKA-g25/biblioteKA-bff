from django.urls import path
from .views import LoanView, LoanCreateView, LoanDetailView

urlpatterns = [
    path("loans/", LoanView.as_view()),
    path("loans/copy/<int:pk>/", LoanCreateView.as_view()),
    path("loans/<int:pk>/return/", LoanDetailView.as_view()),
]
