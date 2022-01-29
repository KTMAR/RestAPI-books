from django.http import HttpResponse
from rest_framework.utils import json
from .serializers import BookSerializer
from .models import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


class BookList(ListCreateAPIView):
    queryset = Book.objects.all().order_by('name')
    serializer_class = BookSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = Book.objects.create(image=file)
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class BookDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
