from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChefViewSet

router = DefaultRouter()
router.register('chefs', ChefViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
