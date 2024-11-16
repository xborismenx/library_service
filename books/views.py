from rest_framework import viewsets

from books.models import Books
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer