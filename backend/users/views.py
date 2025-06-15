from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    ChefConnectionSerializer,
    ChefMealsSerializer,
    ChefProfileSerializer,
    ChefRegistrationSerializer
)

Chef = get_user_model()


class ChefViewSet(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ChefProfileSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ChefRegistrationSerializer
        if self.action == 'meals':
            return ChefMealsSerializer
        return self.serializer_class

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def follow(self, request, pk=None):
        chef = self.get_object()
        if request.method == 'POST':
            if chef == request.user:
                return Response(
                    {'error': 'You cannot follow yourself'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if chef.followers.filter(follower=request.user).exists():
                return Response(
                    {'error': 'You are already following this chef'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            chef.followers.create(follower=request.user)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not chef.followers.filter(follower=request.user).exists():
                return Response(
                    {'error': 'You are not following this chef'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            chef.followers.filter(follower=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def following(self, request):
        following = request.user.following.all()
        serializer = ChefConnectionSerializer(
            following,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def followers(self, request):
        followers = request.user.followers.all()
        serializer = ChefConnectionSerializer(
            followers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['get']
    )
    def meals(self, request, pk=None):
        chef = self.get_object()
        serializer = self.get_serializer(chef)
        return Response(serializer.data)
