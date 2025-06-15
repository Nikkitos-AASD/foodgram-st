from django.contrib.auth.models import AbstractUser
from django.db import models


class Chef(AbstractUser):
    bio = models.TextField('Biography', blank=True)
    avatar = models.ImageField('Avatar', upload_to='chefs/', blank=True)
    website = models.URLField('Website', blank=True)
    location = models.CharField('Location', max_length=100, blank=True)
    is_verified = models.BooleanField('Verified chef', default=False)
    followers_count = models.PositiveIntegerField('Followers count', default=0)
    recipes_count = models.PositiveIntegerField('Recipes count', default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Chef'
        verbose_name_plural = 'Chefs'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email


class ChefConnection(models.Model):
    follower = models.ForeignKey(
        Chef,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Follower'
    )
    following = models.ForeignKey(
        Chef,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Following'
    )
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Chef connection'
        verbose_name_plural = 'Chef connections'
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_chef_connection'
            )
        ]

    def __str__(self):
        return f'{self.follower} follows {self.following}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.following.followers_count += 1
            self.following.save(update_fields=['followers_count'])
