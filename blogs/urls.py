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
]
