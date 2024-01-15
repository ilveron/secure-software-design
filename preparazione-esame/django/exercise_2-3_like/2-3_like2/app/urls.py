from rest_framework.routers import SimpleRouter

from app.views import MovieViewSet

router = SimpleRouter()
router.register('', MovieViewSet, basename='movies')

urlpatterns = router.urls
