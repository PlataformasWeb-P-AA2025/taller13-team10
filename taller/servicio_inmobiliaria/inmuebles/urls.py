from rest_framework.routers import DefaultRouter
from .views import EdificioViewSet, DepartamentoViewSet

router = DefaultRouter()
router.register(r'edificios', EdificioViewSet)
router.register(r'departamentos', DepartamentoViewSet)

urlpatterns = router.urls