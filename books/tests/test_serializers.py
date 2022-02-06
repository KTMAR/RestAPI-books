from django.test import TestCase

from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
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
        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'writer': None,
                'name': "Калеб Шомоtest",
                'genre': None,
                'media_type': None,
                'release_date': None,
                'slug': "kaleb-shomo",
                'description': "dfsfsd",
                'stock': 12,
                'price': "999.00",
                'image': None,
                'offer_of_the_week': False
            },
            {
                'id': book_2.id,
                'writer': None,
                'name': "Ne Калеб Шомоtest",
                'genre': None,
                'media_type': None,
                'release_date': None,
                'slug': "Ne kaleb-shomo",
                'description': "MEdfsfsd",
                'stock': 542,
                'price': "934343.00",
                'image': None,
                'offer_of_the_week': False
            }
        ]
        # print(data)
        self.assertEqual(expected_data, data)
