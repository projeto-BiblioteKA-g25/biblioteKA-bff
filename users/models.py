from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        ordering = ["id"]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=120, unique=True)
    employee = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    block_end_date = models.DateField(null=True, blank=True)
    following = models.ManyToManyField(
        "books.Book",
        related_name="followers",
    )
