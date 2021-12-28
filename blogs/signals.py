from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from .models import Blog


User = get_user_model()


@receiver(signals.post_save, sender=User)
def add_blog_for_user(instance, created, **kwargs):
    if not created:
        return

    current_blog = instance.blog_set.first()

    if not current_blog:
        Blog.objects.create(user=instance)
