from django.db import models


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=100, unique=True)
    synopsis = models.TextField(null=True)
    publishing_date = models.DateTimeField()
    author = models.CharField(max_length=50)
    pages = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
