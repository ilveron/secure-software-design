from rest_framework.routers import SimpleRouter

from app.views import ProductViewSet

router = SimpleRouter()
router.register('', ProductViewSet, basename='product')

urlpatterns = router.urls
