from rest_framework import serializers

from books.models import Books


class BookSerializer(serializers.ModelSerializer):
    choices = {
        "HARD": "HARD",
        "SOFT": "SOFT",
    }
    cover = serializers.ChoiceField(choices=choices)
    class Meta:
        model = Books
        fields = ("id","title", "author", "cover", "inventory", "Daily_fee")