from django.contrib.auth import get_user_model
from django.db import models

from books.models import Books


class Borrowing(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='borrowings')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='borrowings')
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} borrowed {self.book.title}"

    class Meta:
        unique_together = ('user', 'book')
