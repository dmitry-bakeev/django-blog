from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from .models import Blog, Post, Subscription
from .tasks import send_email_to_subscribers


User = get_user_model()


@receiver(signals.post_save, sender=User)
def add_blog_for_user(instance, created, **kwargs):
    if not created:
        return

    current_blog = instance.blog_set.first()

    if not current_blog:
        Blog.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def add_subscription_for_user(instance, created, **kwargs):
    if not created:
        return

    current_blog = instance.subscription_set.first()

    if not current_blog:
        Subscription.objects.create(user=instance)


@receiver(signals.post_save, sender=Post)
def send_email_notify(instance, created, **kwargs):
    if not created:
        return

    send_email_to_subscribers.delay(instance.pk)
