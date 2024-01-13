from rest_framework.routers import SimpleRouter

from app.views import BookViewSet

router = SimpleRouter()
router.register('', BookViewSet, basename='superheroes')

urlpatterns = router.urls
