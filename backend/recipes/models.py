from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, F

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Name', max_length=200)
    color = models.CharField('Color', max_length=7)
    slug = models.SlugField('Slug', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Name', max_length=200)
    unit = models.CharField('Unit', max_length=200)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField('Cuisine name', max_length=100)
    description = models.TextField('Description', blank=True)
    image = models.ImageField('Image', upload_to='cuisines/', blank=True)

    class Meta:
        verbose_name = 'Cuisine'
        verbose_name_plural = 'Cuisines'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Ingredient name', max_length=100)
    measurement = models.CharField('Measurement unit', max_length=50)
    calories = models.PositiveIntegerField('Calories per 100g', default=0)
    protein = models.DecimalField(
        'Protein per 100g',
        max_digits=5,
        decimal_places=2,
        default=0)
    fat = models.DecimalField(
        'Fat per 100g',
        max_digits=5,
        decimal_places=2,
        default=0)
    carbs = models.DecimalField(
        'Carbs per 100g',
        max_digits=5,
        decimal_places=2,
        default=0)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement})'


class Meal(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='meals/')
    cooking_time = models.PositiveIntegerField(
        'Cooking time (minutes)',
        validators=[MinValueValidator(1)]
    )
    servings = models.PositiveIntegerField(
        'Number of servings',
        validators=[MinValueValidator(1)]
    )
    difficulty = models.CharField(
        'Difficulty level',
        max_length=6,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    chef = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meals',
        verbose_name='Chef'
    )
    cuisines = models.ManyToManyField(
        Cuisine,
        related_name='meals',
        verbose_name='Cuisines'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='MealIngredient',
        related_name='meals',
        verbose_name='Ingredients'
    )
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True)

    class Meta:
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'
        ordering = ['-created']

    def __str__(self):
        return self.title


class MealIngredient(models.Model):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name='meal_ingredients',
        verbose_name='Meal'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='meal_ingredients',
        verbose_name='Ingredient'
    )
    amount = models.DecimalField(
        'Amount',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        verbose_name = 'Meal ingredient'
        verbose_name_plural = 'Meal ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['meal', 'ingredient'],
                name='unique_meal_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.meal} - {self.ingredient}'


class SavedMeal(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_meals',
        verbose_name='User'
    )
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name='saved_by',
        verbose_name='Meal'
    )
    saved_at = models.DateTimeField('Saved at', auto_now_add=True)

    class Meta:
        verbose_name = 'Saved meal'
        verbose_name_plural = 'Saved meals'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'meal'],
                name='unique_saved_meal'
            )
        ]

    def __str__(self):
        return f'{self.user} saved {self.meal}'


class MealPlan(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meal_plans',
        verbose_name='User'
    )
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name='planned_for',
        verbose_name='Meal'
    )
    day = models.CharField(
        'Day of week',
        max_length=9,
        choices=DAYS_OF_WEEK
    )
    planned_at = models.DateTimeField('Planned at', auto_now_add=True)

    class Meta:
        verbose_name = 'Meal plan'
        verbose_name_plural = 'Meal plans'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'meal', 'day'],
                name='unique_meal_plan'
            )
        ]

    def __str__(self):
        return f'{self.user} planned {self.meal} for {self.day}'


class Tag(models.Model):
    """Тэги для рецептов с предустановленным выбором."""
    GREEN = '09db4f'
    ORANGE = 'fa6a02'
    PURPLE = 'b813d1'
    COLOR_TAG = [
        (GREEN, 'Зеленый'),
        (ORANGE, 'Оранжевый'),
        (PURPLE, 'Фиолетовый')
    ]
    name = models.CharField('Name', max_length=200, unique=True)
    color = models.CharField('Color', max_length=7, unique=True)
    slug = models.SlugField('Slug', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель для рецептов.
    У автора не может быть создано более одного рецепта с одним именем.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags'
    )
    text = models.TextField('Description')
    name = models.CharField('Name', max_length=200)
    cooking_time = models.PositiveSmallIntegerField(
        'Cooking time',
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField('Image', upload_to='recipes/')
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Ингридиенты для рецепта.
    Промежуточная модель между таблиц:
      Recipe и Ingredient
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ingredient'
    )
    amount = models.PositiveSmallIntegerField(
        'Amount',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Recipe ingredient'
        verbose_name_plural = 'Recipe ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class ShoppingCart(models.Model):
    """
    Список покупок пользователя.
    Ограничения уникальности полей:
      author, recipe.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    """
    Список покупок пользователя.
    Ограничения уникальности полей:
      author, recipe.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'


class Follow(models.Model):
    """
    Подписки на авторов рецептов.
    Ограничения уникальности полей:
      author, user.
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='follower',
        on_delete=models.CASCADE,
        help_text='Текущий пользователь')
    author = models.ForeignKey(
        User,
        verbose_name='Подписка',
        related_name='followed',
        on_delete=models.CASCADE,
        help_text='Подписаться на автора рецепта(ов)')

    class Meta:
        verbose_name = 'Мои подписки'
        verbose_name_plural = 'Мои подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_following')]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
