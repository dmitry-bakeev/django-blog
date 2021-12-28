from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Blog(CreatedAtModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = (
            'created_at',
        )


class Post(CreatedAtModel):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name='блог')
    title = models.CharField(max_length=settings.LEN, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст')

    def __str__(self):
        return f"{self.blog} / {self.title} / {self.created_at.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = (
            'created_at',
        )


class Subscription(CreatedAtModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    blogs = models.ManyToManyField('Blog', verbose_name='блоги')

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = (
            'created_at',
        )
