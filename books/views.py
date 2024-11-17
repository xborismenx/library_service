from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from books.models import Books
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny(), ]
        return [IsAdminUser(), ]
