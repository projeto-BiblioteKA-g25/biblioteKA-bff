from django.urls import path
from .views import LoanView

urlpatterns = [path("loans/", LoanView.as_view())]
