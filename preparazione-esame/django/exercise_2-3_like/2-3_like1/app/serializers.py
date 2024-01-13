from rest_framework import serializers

from app.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'author', 'genre', 'rating')
        model = Book
