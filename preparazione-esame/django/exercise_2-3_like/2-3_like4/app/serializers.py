from rest_framework import serializers

from app.models import VideoGame


class VideoGameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'developer', 'genre', 'rating')
        model = VideoGame
