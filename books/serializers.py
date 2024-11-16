from rest_framework import serializers

from books.models import Books


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        id = ("title", "author", "cover", "inventory", "Daily_fee")