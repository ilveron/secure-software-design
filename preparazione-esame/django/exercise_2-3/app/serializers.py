from rest_framework import serializers

from app.models import SuperHero


class SuperHeroSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'epic_name', 'secret_identity', 'city')
        model = SuperHero
