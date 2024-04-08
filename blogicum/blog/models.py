"""
This module contains the models for the blog app.

The models included are:
- `Post`: This model represents individual blog posts.
- `Category`: This model provides categorization for blog posts.
- `Location`: This model stores location data associated with blog posts.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatechars

User = get_user_model()

TRUNCATION_LENGTH = 30


class CreationPublishedModel(models.Model):
    """BaseModel Abstract model class."""

    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class Post(CreationPublishedModel):
    """Post model represents a single post in the blog."""

    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно'
                  ' делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        'Location',
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='post_images',
        blank=True
    )

    class Meta(CreationPublishedModel.Meta):
        """A meta class that configures additional parameters of the model."""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return truncatechars(self.title, TRUNCATION_LENGTH)


class Category(CreationPublishedModel):
    """Category model is used to organize posts into different categories."""

    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta(CreationPublishedModel.Meta):
        """A meta class that configures additional parameters of the model."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return truncatechars(self.title, TRUNCATION_LENGTH)


class Location(CreationPublishedModel):
    """
    The Location model stores information about different locations
    that can be associated with a Post.
    """

    name = models.CharField('Название места', max_length=256)

    class Meta(CreationPublishedModel.Meta):
        """A meta class that configures additional parameters of the model."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return truncatechars(self.name, TRUNCATION_LENGTH)


class Comment(models.Model):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return truncatechars(self.text, TRUNCATION_LENGTH)
