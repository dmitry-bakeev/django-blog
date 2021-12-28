from django.urls import path

from . import views


app_name = 'blogs'
urlpatterns = [
    path(
        'login/',
        views.BlogLoginView.as_view(),
        name='login'
    ),
]
