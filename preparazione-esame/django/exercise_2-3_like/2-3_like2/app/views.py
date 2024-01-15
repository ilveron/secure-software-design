from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.models import Movie
from app.permissions import IsPostEditorOrReadOnly
from app.serializers import MovieSerializer


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditorOrReadOnly, IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
