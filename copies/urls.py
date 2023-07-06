from django.urls import path

from .views import CopyView

urlpatterns = [path("copies/", CopyView.as_view())]
