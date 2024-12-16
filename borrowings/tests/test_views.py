from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, timedelta

from books.models import Books
from borrowings.models import Borrowing
from borrowings.signals import notify_new_borrowing

User = get_user_model()

BORROWINGS_LIST_URL = reverse("borrowings:borrowings_create")


class BorrowingsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(email="user@example.com", password="password123")
        self.user_2 = get_user_model().objects.create_user(email="user_1@example.com", password="password321")
        self.staff_user = get_user_model().objects.create_user(email="staff@example.com", password="password123",
                                                               is_staff=True)

        self.book = Books.objects.create(title="Test Book", inventory=5, Daily_fee=1.12)

        # Turn off signals so you don't get notifications in the message.
        signals.post_save.disconnect(receiver=notify_new_borrowing, sender=Borrowing)

        self.borrowing = Borrowing.objects.create(
            user=self.user_2,
            book=self.book,
            expected_return_date=date.today() + timedelta(days=7),
        )

        self.borrowing_detail_url = reverse("borrowings:borrowings_detail", args=[self.borrowing.id])
        self.borrowing_return_url = reverse("borrowings:borrowings_return", args=[self.borrowing.id])

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {refresh.access_token}')

    def test_list_borrowings_authenticated_user(self):
        self.authenticate_user(self.user_2)
        response = self.client.get(BORROWINGS_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing.id)

    def test_list_borrowings_staff_user(self):
        self.authenticate_user(self.staff_user)
        response = self.client.get(BORROWINGS_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_borrowing(self):
        self.authenticate_user(self.user)
        data = {
            "book": self.book.id,
            "expected_return_date": date.today() + timedelta(days=7),
        }
        response = self.client.post(BORROWINGS_LIST_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 2)

    def test_create_borrowing_invalid_data(self):
        self.authenticate_user(self.user)
        data = {
            "book": self.book.id,
            "expected_return_date": "invalid-date",
        }
        response = self.client.post(BORROWINGS_LIST_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_borrowing_detail(self):
        self.authenticate_user(self.user)
        response = self.client.get(self.borrowing_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing.id)

    def test_return_borrowing_success(self):
        self.authenticate_user(self.user)
        response = self.client.put(self.borrowing_return_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Book returned successfully.")

        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, 6)

    def test_return_borrowing_already_returned(self):
        self.borrowing.actual_return_date = date.today()
        self.borrowing.save()

        self.authenticate_user(self.user)
        response = self.client.put(self.borrowing_return_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "This book is already returned")
