from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

from borrowings.models import Borrowing


class BorrowingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book", "expected_return_date")

    def validate(self, data):
        book = data["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError({"detail": f"Book {book.title} does not have in inventory."})
        return data

    def create(self, validated_data):
        book = validated_data.pop("book")
        try:
            with transaction.atomic():
                book.inventory -= 1
                book.save()
                user = self.context['request'].user
                borrowing = Borrowing.objects.create(user=user, book=book, **validated_data)
                return borrowing
        except IntegrityError:
            raise ValidationError({'detail': 'This user has already borrowed this book.'})


class BorrowingReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book", "user", "expected_return_date")
        read_only_fields = ("id", "user", "book", "expected_return_date")


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("user", "book", "actual_return_date")
