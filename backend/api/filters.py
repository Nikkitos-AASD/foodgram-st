from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from recipes.models import Dish, Product

User = get_user_model()


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Product
        fields = ('name',)


class DishFilter(filters.FilterSet):
    categories = filters.NumberFilter(field_name='categories__id')
    is_bookmarked = filters.BooleanFilter(method='filter_is_bookmarked')
    is_in_meal_plan = filters.BooleanFilter(method='filter_is_in_meal_plan')
    creator = filters.NumberFilter(field_name='creator__id')

    class Meta:
        model = Dish
        fields = ('categories', 'is_bookmarked', 'is_in_meal_plan', 'creator')

    def filter_is_bookmarked(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(bookmarks__user=user)
        return queryset

    def filter_is_in_meal_plan(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(meal_plans__user=user)
        return queryset
