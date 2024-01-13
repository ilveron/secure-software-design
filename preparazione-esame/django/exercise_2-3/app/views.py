from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.models import SuperHero
from app.permissions import IsPostEditorOrReadOnly
from app.serializers import SuperHeroSerializer


# Create your views here.
class SuperHeroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditorOrReadOnly, IsAuthenticated]
    queryset = SuperHero.objects.all()
    serializer_class = SuperHeroSerializer


class SuperHeroByAuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditorOrReadOnly, IsAuthenticated]
    serializer_class = SuperHeroSerializer

    def get_queryset(self):
        return SuperHero.objects.filter(author=self.request.user)
