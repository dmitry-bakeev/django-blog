from .models import Post, Subscription


def get_user_subscriptions_blogs(user):
    user_subscription = Subscription.objects.filter(user=user).first()
    return user_subscription.blogs.all()


def get_user_subscriptions_posts(blogs_qs):
    if not blogs_qs:
        return Post.objects.none()

    blogs_ids = blogs_qs.values_list('id', flat=True)

    return Post.objects.filter(blog__id__in=blogs_ids).select_related('blog')


def get_user_subscriptions_unread_posts(user, posts_qs):
    user_subscription = Subscription.objects.filter(user=user).first()
    read_posts_ids = user_subscription.read_posts.values_list('id', flat=True)
    return posts_qs.exclude(id__in=read_posts_ids)


def unsubscribe_from_blog(subscription, blog):
    posts = blog.post_set.all()

    subscription.blogs.remove(blog)

    for post in posts:
        subscription.read_posts.remove(post)
