from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import PublishedCreatedModel

User = get_user_model()


class Category(PublishedCreatedModel):
    """Описание модели Категория."""

    title = models.CharField(max_length=30, verbose_name='Заголовок')
    description = models.TextField('Описание')
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedCreatedModel):
    """Описание модели Местоположение."""

    name = models.CharField(max_length=30, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedCreatedModel):
    """Описание модели Публикации."""

    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True
    )
    image = models.ImageField(
        verbose_name='Изображениe',
        upload_to='posts_images',
        blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Получение ссылки на объект"""
        return reverse('blog:post_detail', args=[self.pk])


class Comment(models.Model):
    """Описании модели Комментария к публикациям."""

    text = models.TextField(max_length=256, verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post,
        verbose_name='Публикация',
        on_delete=models.CASCADE,
    )
    created_dt = models.DateTimeField(
        verbose_name='Дата и время добавления',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_dt',)
        default_related_name = 'comments'

    def __str__(self):
        return (f'Комментарий автора {self.author}'
                f' к посту {self.post}, текст: {self.text}')
