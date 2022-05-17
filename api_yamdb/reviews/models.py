from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from api_yamdb.settings import GROUPS, USER
from .validators import less_then_now_year_validator


class User(AbstractUser):
    '''Кастомная модель User'''
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=100,
        blank=True,
        choices=GROUPS,
        default=USER
    )
    confirmation_code = models.CharField(
        'Проверочный код',
        max_length=100,
        blank=True
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[less_then_now_year_validator])
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=timezone.now().year),
                name='year_lte_now'),
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='single_review_per_user'),
            models.CheckConstraint(
                check=models.Q(score__range=(1, 10)),
                name='score_between_1-10'),
        ]
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self) -> str:
        return f'Обзор на {self.title.name}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
