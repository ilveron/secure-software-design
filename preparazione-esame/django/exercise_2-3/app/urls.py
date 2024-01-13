from rest_framework.routers import SimpleRouter

from app.views import SuperHeroViewSet, SuperHeroByAuthorViewSet

router = SimpleRouter()
router.register('', SuperHeroViewSet, basename='superheroes')

urlpatterns = router.urls
