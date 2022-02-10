from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class BookSerializer(serializers.ModelSerializer):
    writer_name = serializers.StringRelatedField(source='writer.name')
    genre_name = serializers.StringRelatedField(source='genre.name')
    media_type_name = serializers.StringRelatedField(source='media_type.name')
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'writer_name',
            'name',
            'genre_name',
            'media_type_name',
            'release_date',
            'description',
            'stock',
            'price',
            'image',
            'annotated_likes',
            'rating')




class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rating')
