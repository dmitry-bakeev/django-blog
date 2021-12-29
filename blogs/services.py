from .models import Post, Subscription


def get_user_subscriptions_blogs(user):
    user_subscription = Subscription.objects.filter(user=user).first()
    return user_subscription.blogs.all()


def get_user_subscriptions_posts(blogs_qs):
    if not blogs_qs:
        return Post.objects.none()

    blogs_ids = blogs_qs.values_list('id', flat=True)

    return Post.objects.filter(blog__id__in=blogs_ids)
