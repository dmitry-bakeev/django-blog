from django.contrib.auth import get_user_model
from django.test import TestCase

from blogs.models import Post
from blogs.services import (
    get_user_blog,
    get_user_subscription,
    subscribe_to_blog,
    read_post,
)

User = get_user_model()


class BlogTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user2_blog = get_user_blog(self.user2)

    def test_check_subscription_not_normal(self):
        check = self.user2_blog.check_subscription(self.user1_subscription.blogs.all())
        self.assertFalse(check)

    def test_check_subscription_normal(self):
        subscribe_to_blog(self.user1_subscription, self.user2_blog)
        check = self.user2_blog.check_subscription(self.user1_subscription.blogs.all())
        self.assertTrue(check)


class PostTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user1_subscription = get_user_subscription(self.user1)
        self.user1_blog = get_user_blog(self.user1)
        self.user2_blog = get_user_blog(self.user2)
        self.user2_post = Post.objects.create(blog=self.user2_blog, title='test1', text='test1')
        subscribe_to_blog(self.user1_subscription, self.user2_blog)

    def test_check_read_not_normal(self):
        check = self.user2_post.check_read(self.user1_subscription)
        self.assertFalse(check)

    def test_check_read_normal(self):
        read_post(self.user1_subscription, self.user2_post)
        check = self.user2_post.check_read(self.user1_subscription)
        self.assertTrue(check)

    def test_check_own_not_normal(self):
        check = self.user2_post.check_own(self.user1_blog)
        self.assertFalse(check)

    def test_check_own_normal(self):
        check = self.user2_post.check_own(self.user2_blog)
        self.assertTrue(check)
