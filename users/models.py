from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=120, unique=True)
    employee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    block_end_date = models.DateTimeField(null=True, blank=True)
