from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = (
            'created_at',
        )


class Post(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name='блог')
    title = models.CharField(max_length=settings.LEN, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog} / {self.title} / {self.created_at.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = (
            'created_at',
        )
