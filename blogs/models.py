from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Blog(CreatedAtModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f"{self.user}"

    def check_subscription(self, subscription_blogs):
        if self in subscription_blogs:
            return True

        return False

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

    def check_read(self, user):
        from .services import get_user_subscription

        user_subscription = get_user_subscription(user)

        if self in user_subscription.read_posts.all():
            return True

        return False

    def check_own(self, user):
        from .services import get_user_blog

        user_blog = get_user_blog(user)

        if self in user_blog.post_set.all():
            return True

        return False

    def get_absolute_url(self):
        return reverse(
            'blogs:post-detail',
            kwargs={'pk': self.pk}
        )

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = (
            'created_at',
        )


class Subscription(CreatedAtModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    blogs = models.ManyToManyField('Blog', verbose_name='блоги')

    read_posts = models.ManyToManyField('Post', verbose_name='прочитанные посты')

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = (
            'created_at',
        )
