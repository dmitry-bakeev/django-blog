from django.contrib.auth import get_user_model
from django.test import TestCase

from blogs.models import Blog, Post, Subscription
from blogs.services import (
    get_user_blog,
    get_user_subscription,
    get_user_subscriptions_blogs,
    get_user_subscriptions_posts,
    get_user_subscriptions_unread_posts,
    subscribe_to_blog,
    unsubscribe_from_blog,
    read_post,
    unread_post,
)

User = get_user_model()


class GetUserBlogTest(TestCase):

    def setUp(self):
        self.user = User(username='user')

    def test_not_normal(self):
        blog = get_user_blog(self.user)
        self.assertFalse(blog)

    def test_normal(self):
        self.user.save()
        self.blog = Blog.objects.first()
        blog = get_user_blog(self.user)
        self.assertEqual(self.blog, blog)


class GetUserSubscriptionTest(TestCase):

    def setUp(self):
        self.user = User(username='user')

    def test_not_normal(self):
        subscription = get_user_subscription(self.user)
        self.assertFalse(subscription)

    def test_normal(self):
        self.user.save()
        self.subscription = Subscription.objects.first()
        subscription = get_user_subscription(self.user)
        self.assertEqual(self.subscription, subscription)


class GetUserSubscriptionsBlogsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user1_blog = get_user_blog(self.user1)
        self.user2_subscription = get_user_subscription(self.user2)
        self.user2_blog = get_user_blog(self.user2)
        self.user1_subscription.blogs.add(self.user2_blog)

    def test_not_normal(self):
        blogs = get_user_subscriptions_blogs(self.user2_subscription)
        self.assertFalse(blogs)

    def test_normal(self):
        self.blogs = Blog.objects.exclude(id=self.user1_blog.id)
        blogs = get_user_subscriptions_blogs(self.user1_subscription)
        self.assertQuerysetEqual(self.blogs, blogs)


class GetUserSubscriptionsPostsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user2_blog = get_user_blog(self.user2)
        subscribe_to_blog(self.user1_subscription, self.user2_blog)
        Post.objects.create(blog=self.user2_blog, title='test1', text='test1')
        Post.objects.create(blog=self.user2_blog, title='test2', text='test2')
        self.posts = Post.objects.all()

    def test_not_normal(self):
        posts = get_user_subscriptions_posts(Blog.objects.none())
        self.assertFalse(posts)

    def test_normal(self):
        posts = get_user_subscriptions_posts(self.user1_subscription.blogs.all())
        self.assertQuerysetEqual(self.posts, posts)


class GetUserSubscriptionsUnreadPostsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user2_blog = get_user_blog(self.user2)
        subscribe_to_blog(self.user1_subscription, self.user2_blog)
        post1 = Post.objects.create(blog=self.user2_blog, title='test1', text='test1')
        _ = Post.objects.create(blog=self.user2_blog, title='test2', text='test2')
        self.user1_subscription.read_posts.add(post1)
        self.posts = Post.objects.exclude(id=post1.id)

    def test_not_normal(self):
        posts = get_user_subscriptions_unread_posts(self.user1_subscription, Post.objects.none())
        self.assertFalse(posts)

    def test_normal(self):
        posts = get_user_subscriptions_unread_posts(self.user1_subscription, Post.objects.all())
        self.assertQuerysetEqual(self.posts, posts)


class SubscribeToBlogTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user2_blog = get_user_blog(self.user2)

    def test_normal(self):
        subscribe_to_blog(self.user1_subscription, self.user2_blog)
        self.assertIn(self.user2_blog, self.user1_subscription.blogs.all())


class UnsubscribeFromBlogTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user2_blog = get_user_blog(self.user2)
        self.user1_subscription.blogs.add(self.user2_blog)
        self.post1 = Post.objects.create(blog=self.user2_blog, title='test1', text='test1')
        _ = Post.objects.create(blog=self.user2_blog, title='test2', text='test2')
        self.user1_subscription.read_posts.add(self.post1)

    def test_normal(self):
        unsubscribe_from_blog(self.user1_subscription, self.user2_blog)
        self.assertNotIn(self.post1, self.user1_subscription.read_posts.all())


class ReadPostTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user2_blog = get_user_blog(self.user2)
        self.user2_post = Post.objects.create(blog=self.user2_blog, title='test1', text='test1')
        subscribe_to_blog(self.user1_subscription, self.user2_blog)

    def test_normal(self):
        read_post(self.user1_subscription, self.user2_post)
        self.assertIn(self.user2_post, self.user1_subscription.read_posts.all())


class UnreadPostTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user2_blog = get_user_blog(self.user2)
        self.user2_post = Post.objects.create(blog=self.user2_blog, title='test1', text='test1')
        subscribe_to_blog(self.user1_subscription, self.user2_blog)
        read_post(self.user1_subscription, self.user2_post)

    def test_normal(self):
        unread_post(self.user1_subscription, self.user2_post)
        self.assertNotIn(self.user2_post, self.user1_subscription.read_posts.all())
