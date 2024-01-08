from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly, IsPostEditor, IsPermittedOnPost
from posts.serializers import PostSerializer


# Create your views here.
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostByAuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostEditorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditor]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostPermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPermittedOnPost]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
