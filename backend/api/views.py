from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import DishFilter, ProductFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CategorySerializer, CustomUserCreateSerializer,
    CustomUserSerializer, DishCreateSerializer,
    DishReadSerializer, DishShortSerializer,
    ProductSerializer, UserFollowSerializer
)
from recipes.models import (
    Category, Product, Dish, DishProduct,
    Bookmark, MealPlan
)
from users.models import Follow

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        if self.action == 'followers':
            return UserFollowSerializer
        return CustomUserSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def follow(self, request, pk=None):
        user = request.user
        following = get_object_or_404(User, pk=pk)

        if request.method == 'POST':
            if user == following:
                return Response(
                    {'error': 'You cannot follow yourself'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(
                follower=user,
                following=following
            ).exists():
                return Response(
                    {'error': 'You are already following this user'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(follower=user, following=following)
            serializer = self.get_serializer(following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            follow = Follow.objects.filter(
                follower=user,
                following=following
            )
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'You are not following this user'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def followers(self, request):
        user = request.user
        following = User.objects.filter(following__follower=user)
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = None


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DishFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return DishCreateSerializer
        return DishReadSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def bookmark(self, request, pk=None):
        user = request.user
        dish = get_object_or_404(Dish, pk=pk)

        if request.method == 'POST':
            if Bookmark.objects.filter(user=user, dish=dish).exists():
                return Response(
                    {'error': 'Dish is already bookmarked'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Bookmark.objects.create(user=user, dish=dish)
            serializer = DishShortSerializer(dish)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            bookmark = Bookmark.objects.filter(user=user, dish=dish)
            if bookmark.exists():
                bookmark.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Dish is not bookmarked'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def meal_plan(self, request, pk=None):
        user = request.user
        dish = get_object_or_404(Dish, pk=pk)

        if request.method == 'POST':
            if MealPlan.objects.filter(user=user, dish=dish).exists():
                return Response(
                    {'error': 'Dish is already in meal plan'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            MealPlan.objects.create(user=user, dish=dish)
            serializer = DishShortSerializer(dish)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            meal_plan = MealPlan.objects.filter(user=user, dish=dish)
            if meal_plan.exists():
                meal_plan.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Dish is not in meal plan'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_list(self, request):
        user = request.user
        if not MealPlan.objects.filter(user=user).exists():
            return Response(
                {'error': 'Shopping list is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ingredients = DishProduct.objects.filter(
            dish__meal_plans__user=user
        ).values(
            'product__name',
            'product__unit'
        ).annotate(amount=Sum('quantity'))

        shopping_list = ['Shopping List\n']
        for ingredient in ingredients:
            shopping_list.append(
                f'{ingredient["product__name"]} - '
                f'{ingredient["amount"]} {ingredient["product__unit"]}\n'
            )

        response = HttpResponse(
            ''.join(shopping_list),
            content_type='text/plain'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response
