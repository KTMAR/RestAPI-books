from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'writer', 'name', 'genre', 'media_type', 'release_date', 'slug', 'description', 'stock', 'price',
                  'offer_of_the_week', 'image')
