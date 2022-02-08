from django.test import TestCase

from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.book_21 = Book.objects.create(name="Калеб Шомоtest gfgfgfgf",
                                           slug="kaleb-shomo",
                                           description="dfsfsd",
                                           stock=12,
                                           price="999.00",
                                           offer_of_the_week=False)
        self.book_22 = Book.objects.create(name="Калебfdfdfd Шомоtest fgfgfgfgf",
                                           slug="Ne-kaleb-shomo",
                                           description="MEdfsfsd",
                                           stock=542,
                                           price="934343.00",
                                           offer_of_the_week=False)
        data = BookSerializer([self.book_21, self.book_22], many=True).data
        expected_data = [
            {
                'id': self.book_21.id,
                'name': 'Калеб Шомоtest gfgfgfgf',
                'release_date': None,
                'slug': 'kaleb-shomo',
                'description': 'dfsfsd',
                'stock': 12,
                'price': '999.00',
                'offer_of_the_week': False,
                'image': None,
            },
            {
                'id': self.book_22.id,
                'name': 'Калебfdfdfd Шомоtest fgfgfgfgf',
                'release_date': None,
                'slug': 'Ne-kaleb-shomo',
                'description': 'MEdfsfsd',
                'stock': 542,
                'price': '934343.00',
                'offer_of_the_week': False,
                'image': None,
            }
        ]
        self.assertEqual(expected_data, data)
