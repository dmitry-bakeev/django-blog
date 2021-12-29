from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import generic

from .forms import PostForm
from .models import Post

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


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    template_name_suffix = '-form'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return redirect(self.get_success_url())


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    template_name_suffix = '-detail'
    model = Post
