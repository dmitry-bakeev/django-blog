from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import PostForm
from .models import Blog, Post

from .services import (
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


class BlogLoginView(LoginView):
    template_name = 'blogs/login-form.html'


class HomeView(LoginRequiredMixin, generic.ListView):
    template_name = 'blogs/home.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_subscription': self.user_subscription,
        })
        return context

    def get_queryset(self):
        self.user_subscription = get_user_subscription(self.request.user)
        blogs = get_user_subscriptions_blogs(self.user_subscription)
        posts = get_user_subscriptions_posts(blogs)
        unread_posts = get_user_subscriptions_unread_posts(self.user_subscription, posts)
        return unread_posts.order_by('-created_at')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_blog = get_user_blog(self.request.user)
        context.update({
            'user_blog': user_blog
        })
        return context


class BlogListView(LoginRequiredMixin, generic.ListView):
    template_name_suffix = '-list'
    model = Blog
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_subscription = get_user_subscription(self.request.user)
        blogs = get_user_subscriptions_blogs(user_subscription)
        context.update({'subscription_blogs': blogs})
        return context

    def get_queryset(self):
        qs = Blog.objects.exclude(user=self.request.user).select_related('user')
        return qs


class SubscribeBlogView(LoginRequiredMixin, generic.View):

    def post(self, request):
        blog_pk = request.POST.get('blog_pk')
        blog = get_object_or_404(Blog, pk=blog_pk)

        user_subscription = get_user_subscription(self.request.user)
        subscribe_to_blog(user_subscription, blog)

        return redirect(request.POST.get('back', '/'))


class UnsubscribeBlogView(LoginRequiredMixin, generic.View):

    def post(self, request):
        blog_pk = request.POST.get('blog_pk')
        blog = get_object_or_404(Blog, pk=blog_pk)

        user_subscription = get_user_subscription(self.request.user)
        unsubscribe_from_blog(user_subscription, blog)

        return redirect(request.POST.get('back', '/'))


class ReadPostView(LoginRequiredMixin, generic.View):

    def post(self, request):
        post_pk = request.POST.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)

        user_subscription = get_user_subscription(self.request.user)
        read_post(user_subscription, post)

        return redirect(request.POST.get('back', '/'))


class UnreadPostView(LoginRequiredMixin, generic.View):

    def post(self, request):
        post_pk = request.POST.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)

        user_subscription = get_user_subscription(self.request.user)
        unread_post(user_subscription, post)

        return redirect(request.POST.get('back', '/'))


class BlogPostListView(LoginRequiredMixin, generic.ListView):
    template_name = 'blogs/blog-post-list.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'own_blog': self.own_blog,
            'user_blog': self.user_blog
        })
        return context

    def get_queryset(self):
        blog_pk = self.request.GET.get('blog_pk')
        if blog_pk:
            user_blog = get_object_or_404(Blog, pk=blog_pk)
            self.own_blog = 0
        else:
            user_blog = get_user_blog(self.request.user)
            self.own_blog = 1

        self.user_blog = user_blog
        return self.model.objects.filter(blog=user_blog).order_by('-created_at')


class ReadPostListView(LoginRequiredMixin, generic.ListView):
    template_name = 'blogs/home.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': '?????????????????????????? ??????????',
            'user_subscription': self.user_subscription
        })
        return context

    def get_queryset(self):
        self.user_subscription = get_user_subscription(self.request.user)
        return self.user_subscription.read_posts.select_related('blog').all()


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blogs:own-posts')
