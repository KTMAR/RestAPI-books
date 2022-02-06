from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name="Калеб Шомоtest",
                                     slug="kaleb-shomo",
                                     description="dfsfsd",
                                     stock=12,
                                     price="999.00",
                                     offer_of_the_week=False)
        book_2 = Book.objects.create(name="Ne Калеб Шомоtest",
                                     slug="Ne kaleb-shomo",
                                     description="MEdfsfsd",
                                     stock=542,
                                     price="934343.00",
                                     offer_of_the_week=False)
        url = 'http://127.0.0.1:8000/api/books/'
        response = self.client.get(url)
        serializer_data = BookSerializer([book_1, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


