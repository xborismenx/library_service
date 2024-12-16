from django.db import models


class Books(models.Model):
    CHOICES = {
        "HARD": "HARD",
        "SOFT": "SOFT",
    }
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(CHOICES, max_length=100)
    inventory = models.PositiveIntegerField()
    Daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.title}, author: {self.author}, with cover: {self.cover}, counts: {self.inventory}"
