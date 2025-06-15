from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError

from recipes.models import Follow, Recipe
from recipes.serializers import MealSerializer

Chef = get_user_model()


class ChefProfileSerializer(serializers.ModelSerializer):
    recipes_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Chef
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'website', 'location', 'is_verified',
            'recipes_count', 'followers_count', 'following_count',
            'is_following'
        )
        read_only_fields = ('email', 'is_verified')

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(follower=request.user).exists()
        return False


class ChefRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Chef
        fields = (
            'email', 'username', 'first_name', 'last_name',
            'password', 'password_confirm'
        )

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match'}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        chef = Chef.objects.create_user(**validated_data)
        return chef


class ChefConnectionSerializer(serializers.ModelSerializer):
    chef = ChefProfileSerializer(read_only=True)

    class Meta:
        model = Chef.following.through
        fields = ('chef', 'created_at')
        read_only_fields = ('created_at',)


class ChefMealsSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)

    class Meta:
        model = Chef
        fields = ('id', 'username', 'meals')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer для чтения / создания пользователя модели User.
    Переопределён метод create для возможности получения токена по
    кастомным url. - шифрование пароля по правилам djosera.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Chef
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True},
                        'is_subscribed': {'read_only': True}}

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(user=user, author=obj).exists()
        return False

    def create(self, validated_data):
        return Chef.objects.create_user(**validated_data)


class FollowSerializer(serializers.ModelSerializer):
    """Serializer для модели Follow."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(
                user=obj.user,
                author=obj.author).exists()
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return MealSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def validate(self, data):
        author = self.context.get('author')
        user = self.context.get('request').user
        if Follow.objects.filter(
                author=author,
                user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST)
        if user == author:
            raise ValidationError(
                detail='Невозможно подписаться на себя!',
                code=status.HTTP_400_BAD_REQUEST)
        return data
