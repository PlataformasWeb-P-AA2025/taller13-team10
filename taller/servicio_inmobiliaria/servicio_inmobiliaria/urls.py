from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from inmuebles.views import EdificioViewSet, DepartamentoViewSet
from rest_framework.authtoken import views as drf_views

router = routers.DefaultRouter()
router.register(r'edificios', EdificioViewSet)
router.register(r'departamentos', DepartamentoViewSet)

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', drf_views.obtain_auth_token),
]
