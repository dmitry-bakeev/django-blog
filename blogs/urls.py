from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


app_name = 'blogs'
urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'
    ),
    path(
        'login/',
        views.BlogLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'post-create/',
        views.PostCreateView.as_view(),
        name='post-create'
    ),
    path(
        'post-detail/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post-detail',
    ),
    path(
        'blogs/',
        views.BlogListView.as_view(),
        name='blogs',
    ),
    path(
        'subscribe/',
        views.SubscribeBlogView.as_view(),
        name='subscribe',
    ),
    path(
        'unsubscribe/',
        views.UnsubscribeBlogView.as_view(),
        name='unsubscribe',
    ),
    path(
        'read/',
        views.ReadPostView.as_view(),
        name='read',
    ),
    path(
        'unread/',
        views.UnreadPostView.as_view(),
        name='unread',
    ),
    path(
        'own-posts/',
        views.OwnPostListView.as_view(),
        name='own-posts',
    ),
]
