from django.contrib import admin

from .models import Blog, Post, Subscription


class DisableEditModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Blog)
class BlogAdmin(DisableEditModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(DisableEditModelAdmin):
    pass
