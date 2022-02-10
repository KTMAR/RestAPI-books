from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from books.models import Book, UserBookRelation
from books.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.book_21 = Book.objects.create(name="Калеб Шомоtest gfgfgfgf",
                                           description="dfsfsd",
                                           stock=12,
                                           price="999.00",
                                           offer_of_the_week=False,
                                           )
        self.book_22 = Book.objects.create(name="Калебfdfdfd Шомоtest fgfgfgfgf",
                                           description="MEdfsfsd",
                                           stock=542,
                                           price="934343.00",
                                           offer_of_the_week=False,
                                           )

        UserBookRelation.objects.create(user=self.user1, book=self.book_21, like=True, rating=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book_21, like=True, rating=2)

        UserBookRelation.objects.create(user=self.user1, book=self.book_22, like=True, rating=4)
        UserBookRelation.objects.create(user=self.user2, book=self.book_22, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rating')
        ).order_by('id')

        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': self.book_21.id,
                'name': 'Калеб Шомоtest gfgfgfgf',
                'release_date': None,
                'description': 'dfsfsd',
                'stock': 12,
                'price': '999.00',
                'image': None,
                'annotated_likes': 2,
                'rating': '3.50'
            },
            {
                'id': self.book_22.id,
                'name': 'Калебfdfdfd Шомоtest fgfgfgfgf',
                'release_date': None,
                'description': 'MEdfsfsd',
                'stock': 542,
                'price': '934343.00',
                'image': None,
                'annotated_likes': 1,
                'rating': '4.00'
            }
        ]
        print(data)
        self.assertEqual(expected_data, data)
