from django.db import transaction
from django.db.models import Case, When, Value, BooleanField
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingWriteSerializer,
    BorrowingReadSerializer,
    BorrowingReturnSerializer, BorrowingDetailSerializer,
)


class BorrowingsListCreateView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingWriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowingWriteSerializer
        return BorrowingReadSerializer

    def get_queryset(self):
        queryset = self.queryset.all().annotate(
            is_active=Case(
                When(actual_return_date__isnull=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

        # only staff can filter borrowings
        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            is_active = self.request.query_params.get("is_active")

            if is_active:
                queryset = queryset.filter(is_active=is_active)
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class BorrowingsDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer


@extend_schema(
    request=BorrowingReturnSerializer,
    summary="Endpoint for return borrowing book",
    description="Endpoint for return borrowing book from auth user",
)
class BorrowingsReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReturnSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {
                    "detail": "This book is already returned",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            borrowing.actual_return_date = now().date()
            borrowing.save()

            borrowing.book.inventory += 1
            borrowing.book.save()

            return Response(
                {"message": "Book returned successfully."}, status=status.HTTP_200_OK
            )
