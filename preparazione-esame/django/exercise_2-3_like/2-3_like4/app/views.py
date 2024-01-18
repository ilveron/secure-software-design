from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.models import VideoGame
from app.permissions import IsPostEditorOrReadOnly
from app.serializers import VideoGameSerializer


# Create your views here.
class VideoGameViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditorOrReadOnly, IsAuthenticated]
    queryset = VideoGame.objects.all()
    serializer_class = VideoGameSerializer

