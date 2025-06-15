from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, DishViewSet,
    ProductViewSet, UserViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('dishes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
