from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from books.models import Books

BOOK_LIST_URL = reverse('books:books-list')


class BookViewSetUserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="user@mail.com", password="user123")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {self.token}")

        self.book = Books.objects.create(
            title="Book",
            author="Author",
            cover="HARD",
            inventory=10,
            Daily_fee=2.50
        )

    def test_create_book_as_non_admin(self):
        data = {
            "title": "Book 3",
            "author": "Author 3",
            "cover": "HARD",
            "inventory": 7,
            "Daily_fee": 1.50
        }
        response = self.client.post(BOOK_LIST_URL, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_for_non_admin(self):
        data = {
            "title": "Book 1 Updated",
            "author": "Author 1 Updated",
            "cover": "SOFT",
            "inventory": 12,
            "Daily_fee": 3.00
        }
        update_response = self.client.put(f"/books/{self.book.id}/", data)
        delete_response = self.client.delete(f"/books/{self.book.id}/")
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)


class BookViewSetAdminTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(email="admin", password="admin123")
        refresh = RefreshToken.for_user(self.admin_user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {self.token}")

        self.book1 = Books.objects.create(
            title="Book 1",
            author="Author 1",
            cover="HARD",
            inventory=10,
            Daily_fee=2.50
        )
        self.book2 = Books.objects.create(
            title="Book 2",
            author="Author 2",
            cover="SOFT",
            inventory=5,
            Daily_fee=3.00
        )

    def test_list_books(self):
        response = self.client.get(BOOK_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_as_admin(self):
        self.client.force_login(user=self.admin_user)

        data = {
            "title": "Book 3",
            "author": "Author 3",
            "cover": "HARD",
            "inventory": 7,
            "Daily_fee": 1.50
        }
        response = self.client.post(BOOK_LIST_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Books.objects.count(), 3)

    def test_update_book_as_admin(self):
        data = {
            "title": "Updated Book 1",
            "author": "Updated Author 1",
            "cover": "SOFT",
            "inventory": 15,
            "Daily_fee": 2.00
        }
        response = self.client.put(f"/books/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book 1")

    def test_delete_book_as_admin(self):
        response = self.client.delete(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Books.objects.count(), 1)
