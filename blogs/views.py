from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from .forms import PostForm
from .models import Blog, Post, Subscription

from .services import (
    get_user_subscriptions_blogs,
    get_user_subscriptions_posts,
    unsubscribe_from_blog,
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


class BlogListView(LoginRequiredMixin, generic.ListView):
    template_name_suffix = '-list'
    model = Blog
    paginate_by = 50

    def get_queryset(self):
        qs = Blog.objects.exclude(user=self.request.user).select_related('user')
        return qs


class SubscribeBlogView(LoginRequiredMixin, generic.View):

    def post(self, request):
        blog_pk = request.POST.get('blog_pk')
        blog = get_object_or_404(Blog, pk=blog_pk)

        subscription = Subscription.objects.filter(user=request.user).first()
        subscription.blogs.add(blog)

        return redirect(request.POST.get('back', '/'))


class UnsubscribeBlogView(LoginRequiredMixin, generic.View):

    def post(self, request):
        blog_pk = request.POST.get('blog_pk')
        blog = get_object_or_404(Blog, pk=blog_pk)

        subscription = Subscription.objects.filter(user=request.user).first()
        unsubscribe_from_blog(subscription, blog)

        return redirect(request.POST.get('back', '/'))


class ReadPostView(LoginRequiredMixin, generic.View):

    def post(self, request):
        post_pk = request.POST.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)

        subscription = Subscription.objects.filter(user=request.user).first()
        subscription.read_posts.add(post)

        return redirect(request.POST.get('back', '/'))


class UnreadPostView(LoginRequiredMixin, generic.View):

    def post(self, request):
        post_pk = request.POST.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)

        subscription = Subscription.objects.filter(user=request.user).first()
        subscription.read_posts.remove(post)

        return redirect(request.POST.get('back', '/'))
