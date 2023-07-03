from django.db import models
from users.models import User


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=100)
    publishing_date = models.DateTimeField()
    author = models.CharField(max_length=50)
    pages = models.IntegerField()

