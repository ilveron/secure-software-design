from django.urls import path
from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet, PostByAuthorViewSet, PostEditorViewSet

# urlpatterns = [
#     path('<int:pk>/', PostDetail.as_view()),
#     path('', PostList.as_view()),
# ]

router = SimpleRouter()
router.register('by-author', PostByAuthorViewSet, basename='posts-by-author')
router.register('', PostViewSet, basename='posts')

router.register('editor', PostEditorViewSet, basename='post-editors')
urlpatterns = router.urls
