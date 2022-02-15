from django.db.models import Count, Case, When, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import BookSerializer, UserBookRelationSerializer
from .models import *
from books.permissions import IsOwnerOrStaffOrReadOnly


class BookListView(ModelViewSet):
    queryset = Book.objects.all().annotate(
        annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
        rating=Avg('userbookrelation__rating')).select_related('writer').select_related(
        'genre').select_related('media_type').select_related('owner')
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price']
    search_fields = ['name', 'writer__name', 'genre__name', 'media_type__name', 'description']
    ordering_fields = ['id', 'price', 'name', 'genre__name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])

        return obj
