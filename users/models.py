from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    email       = models.EmailField(unique=True)
    username    = models.CharField(max_length=30, unique=True)
    bio         = models.TextField(blank=True, default='')
    avatar      = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        app_label = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.get_full_name()} (@{self.username})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name


class Post(models.Model):
    user       = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        db_constraint=False,
    )
    text       = models.TextField(max_length=2000)
    image      = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'users'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        snippet = self.text[:50] + ('...' if len(self.text) > 50 else '')
        return f'Post by @{self.user.username}: {snippet}'
