from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import generic

from .services import (
    get_user_subscriptions_blogs,
    get_user_subscriptions_posts,
)


class BlogLoginView(LoginView):
    template_name = 'blogs/login-form.html'


class HomeView(LoginRequiredMixin, generic.ListView):
    template_name = 'blogs/home.html'
    paginate_by = 50

    def get_queryset(self):
        blogs = get_user_subscriptions_blogs(self.request.user)
        posts = get_user_subscriptions_posts(blogs)
        return posts.order_by('-created_at')
