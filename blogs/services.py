from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Post, Subscription


def get_user_subscription(user):
    return Subscription.objects.filter(user=user).first()


def get_user_subscriptions_blogs(user_subscription):
    return user_subscription.blogs.all()


def get_user_subscriptions_posts(blogs_qs):
    if not blogs_qs:
        return Post.objects.none()

    blogs_ids = blogs_qs.values_list('id', flat=True)

    return Post.objects.filter(blog__id__in=blogs_ids).select_related('blog')


def get_user_subscriptions_unread_posts(user_subscription, posts_qs):
    read_posts_ids = user_subscription.read_posts.values_list('id', flat=True)
    return posts_qs.exclude(id__in=read_posts_ids)


def unsubscribe_from_blog(subscription, blog):
    posts = blog.post_set.all()

    subscription.blogs.remove(blog)

    for post in posts:
        subscription.read_posts.remove(post)


def send_html_email(post):
    query = ~Q(user__email='') & Q(user__email__isnull=False)
    recipients = post.blog.subscription_set.filter(query).values_list('user__email', flat=True)

    if not recipients:
        return

    subject = 'Добавлен новый пост.'

    html_message = render_to_string(
        settings.EMAIL_TEMPLATE,
        context={
            'domain': settings.SITE_ROOT,
            'post': post,
        }
    )

    message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        recipient_list=recipients,
        from_email=settings.DEFAULT_FROM_EMAIL
    )
