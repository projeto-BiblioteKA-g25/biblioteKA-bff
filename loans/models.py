from django.db import models


class Loan(models.Model):
    class Meta:
        ordering = ["id"]

    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    status = models.BooleanField(default=False)

    copy = models.ForeignKey(
        "copies.Copy",
        on_delete=models.CASCADE,
        related_name="loans",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="loans",
    )
