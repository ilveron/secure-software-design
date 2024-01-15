from rest_framework import serializers

from app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'director', 'genre', 'year')
        model = Movie
