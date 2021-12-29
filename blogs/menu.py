from dataclasses import dataclass
from typing import Any

from django.urls import reverse_lazy


@dataclass
class MenuItem:
    title: str
    url: Any


UNAUTHORIZED_MENU = [
    MenuItem('Главная', reverse_lazy('blogs:home')),
    MenuItem('Войти', reverse_lazy('blogs:login'))
]


AUTHORIZED_MENU = [
    MenuItem('Главная', reverse_lazy('blogs:home')),
    MenuItem('Просмотренные посты', reverse_lazy('blogs:read-posts')),
    MenuItem('Добавить пост', reverse_lazy('blogs:post-create')),
    MenuItem('Список блогов', reverse_lazy('blogs:blogs')),
    MenuItem('Мой блог', reverse_lazy('blogs:own-posts')),
    MenuItem('Выйти', reverse_lazy('blogs:logout'))
]

STAFF_EXTENDED_MENU = [
    MenuItem('Админ-панель', reverse_lazy('admin:index')),
]
