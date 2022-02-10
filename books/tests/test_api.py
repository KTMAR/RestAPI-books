import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from books.models import Book, UserBookRelation
from books.serializers import BookSerializer


class BookSerializerTestCase(APITestCase):
    url = reverse('book-list')

    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username1')
        self.book_1 = Book.objects.create(name="Калеб Шомоtest",
                                          slug="kaleb-shomo",
                                          description="Test name 3",
                                          stock=12,
                                          price="999.00",
                                          offer_of_the_week=False,
                                          owner=self.user)
        self.book_2 = Book.objects.create(name="Ne Калеб Шомоtest",
                                          slug="Ne kaleb-shomo",
                                          description="Каfgfgf",
                                          stock=542,
                                          price="934343.00",
                                          offer_of_the_week=False,
                                          owner=self.user)
        self.book_3 = Book.objects.create(name="Test name 3",
                                          slug="test-slug-3",
                                          description="Калеб",
                                          stock=32,
                                          price="100000.00",
                                          offer_of_the_week=True,
                                          owner=self.user)
        UserBookRelation.objects.create(user=self.user, book=self.book_2, like=True, rating=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book_2, like=True, rating=2)

    def test_get(self):
        response = self.client.get(self.url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rating'))
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[2]['rating'], '3.50')
        self.assertEqual(serializer_data[2]['annotated_likes'], 2)

    def test_get_filter(self):
        response = self.client.get(self.url, data={'price': '999.00'})
        books = Book.objects.filter(id=self.book_1.id).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rating'))
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        response = self.client.get(self.url, data={'search': 'Test name 3'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rating')).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)



    def test_get_sorted(self):
        response = self.client.get(self.url, data={'ordering': '-id'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_2.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rating')).order_by('-id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_created_post(self):
        data = {
            "writer_name": "Test Created Post 1",
            "name": "Test Created Name 1",
            "genre_name": "Economy",
            "media_type_name": "USB",
            "release_date": "1998-01-02",
            "slug": "test-created-post-1",
            "description": "Description text",
            "stock": 12,
            "price": "999.00",
            "offer_of_the_week": False,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update_post(self):
        url_put = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "writer_name": "Test Updated Post 1",
            "name": "Test Updated Name 1",
            "slug": "test-created-post-1",
            "description": "Description text",
            "stock": 654,
            "price": "1245.00",
            "offer_of_the_week": False,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url_put, data=json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_post(self):
        url_put = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url_put, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_post_not_owner(self):
        url_put = reverse('book-detail', args=(self.book_1.id,))
        self.user2 = User.objects.create(username='test_username2')
        self.client.force_login(self.user2)
        response = self.client.delete(url_put, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_post_not_owner(self):
        url_put = reverse('book-detail', args=(self.book_1.id,))
        self.user2 = User.objects.create(username='test_username2')

        data = {
            "writer_name": "Test Updated Post 1",
            "name": "Test Updated Name 1",
            "slug": "test-created-post-1",
            "description": "Description text",
            "stock": 654,
            "price": "1245.00",
            "offer_of_the_week": False,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url_put, data=json_data, content_type='application/json')
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(12, self.book_1.stock)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_post_not_owner_but_stuff(self):
        url_put = reverse('book-detail', args=(self.book_1.id,))
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        data = {
            "writer_name": "Test Updated Post 1",
            "name": "Test Updated Name 1",
            "slug": "test-created-post-1",
            "description": "Description text",
            "stock": 654,
            "price": "1245.00",
            "offer_of_the_week": False,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url_put, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(654, self.book_1.stock)


class BookRelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username3')
        self.user2 = User.objects.create(username='test_username4')
        self.book_1 = Book.objects.create(name="Калеб Шомоtest",
                                          slug="kaleb-shomo",
                                          description="Test name 3",
                                          stock=12,
                                          price="999.00",
                                          offer_of_the_week=False,
                                          )
        self.book_2 = Book.objects.create(name="Ne Калеб Шомоtest",
                                          slug="Ne kaleb-shomo",
                                          description="Каfgfgf",
                                          stock=542,
                                          price="934343.00",
                                          offer_of_the_week=False,
                                          )

    def test_like_and_bookmarks(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)
        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "rating": 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(3, relation.rating)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "rating": 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
