from django.contrib import admin

from .models import (
    Category, Product, Dish, DishProduct,
    Bookmark, MealPlan
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)
    list_filter = ('name',)


class DishProductInline(admin.TabularInline):
    model = DishProduct
    min_num = 1
    extra = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'prep_time', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'created_at')
    inlines = (DishProductInline,)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish')
    search_fields = ('user__email', 'dish__title')
    list_filter = ('user', 'dish')


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish')
    search_fields = ('user__email', 'dish__title')
    list_filter = ('user', 'dish')
