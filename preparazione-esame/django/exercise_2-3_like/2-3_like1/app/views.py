from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.models import Book
from app.permissions import IsPostEditorOrReadOnly
from app.serializers import BookSerializer


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditorOrReadOnly, IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookByAuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditorOrReadOnly, IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)
