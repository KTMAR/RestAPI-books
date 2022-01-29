from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')
