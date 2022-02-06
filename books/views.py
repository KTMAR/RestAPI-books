from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import SearchFilter
from .serializers import BookSerializer
from .models import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


class BookList(ListCreateAPIView):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['price']
    search_fields = ['name', 'writer__name', 'genre__name', 'media_type__name']


class BookDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
