from django.db import models

from django.contrib.auth.models import UserManager, AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class User(AbstractUser):
    objects = UserManager()
    
    nickname = models.CharField(blank=True, max_length=50)
    introduction = models.TextField(blank=True, max_length=200)
    profile_image = models.ImageField(blank=True, null=True)

class Game(models.Model):
    title = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

class Character(models.Model):
    game = models.ForeignKey(Game, related_name='game_name', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50)
    skill = models.CharField(max_length=100)
    body = models.TextField()
    imgurl = models.URLField(max_length=512) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

class Comment(models.Model):
    # related_name: 역참조 시 이용(누가 날 바라보는지...)
    author = models.ForeignKey(User, related_name='user', on_delete=models.SET_NULL, null=True)
    character = models.ForeignKey(Character, related_name='comments', on_delete=models.CASCADE, null=False)
    # 쿼리 많이 잡아먹는 단점
    parent = models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
