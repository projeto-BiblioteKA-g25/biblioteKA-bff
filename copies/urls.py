from django.urls import path

from .views import CopyBookByIdView, CopyView

urlpatterns = [
    path("copies/", CopyView.as_view()),
    path("copies/<int:pk>/books/", CopyBookByIdView.as_view()),
]
