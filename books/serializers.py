from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class BookSerializer(serializers.ModelSerializer):
    writer_name = serializers.StringRelatedField(source='writer.name')
    genre_name = serializers.StringRelatedField(source='genre.name')
    media_type_name = serializers.StringRelatedField(source='media_type.name')

    class Meta:
        model = Book
        fields = (
            'id',
            'writer_name',
            'name',
            'genre_name',
            'media_type_name',
            'release_date',
            'slug',
            'description',
            'stock',
            'price',
            'offer_of_the_week',
            'image')
