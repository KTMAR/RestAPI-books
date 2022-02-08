from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .serializers import BookSerializer
from .models import *

from books.permissions import IsOwnerOrStaffOrReadOnly


class BookListView(ModelViewSet):
    queryset = Book.objects.all().order_by('id')
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


# class BookDetail(RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     authentication_classes = [SessionAuthentication, BasicAuthentication]

    #
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
