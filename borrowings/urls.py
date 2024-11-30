from django.urls import path

from borrowings.views import (
    BorrowingsListCreateView,
    BorrowingsDetailView,
    BorrowingsReturnView,
)

urlpatterns = [
    path("", BorrowingsListCreateView.as_view(), name="borrowings_create"),
    path("<int:pk>/", BorrowingsDetailView.as_view(), name="borrowings_detail"),
    path("<int:pk>/return/", BorrowingsReturnView.as_view(), name="borrowings_return"),
]
