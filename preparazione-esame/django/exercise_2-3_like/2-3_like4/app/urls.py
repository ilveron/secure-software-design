from rest_framework.routers import SimpleRouter

from app.views import VideoGameViewSet

router = SimpleRouter()
router.register('', VideoGameViewSet, basename='videogame')

urlpatterns = router.urls
