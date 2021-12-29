from dataclasses import dataclass
from typing import Any

from django.urls import reverse_lazy


@dataclass
class MenuItem:
    title: str
    url: Any


UNATHORIZED_MENU = [
    MenuItem('Главная', reverse_lazy('blogs:home')),
    MenuItem('Войти', reverse_lazy('blogs:login'))
]


ATHORIZED_MENU = [
    MenuItem('Главная', reverse_lazy('blogs:home')),
    MenuItem('Добавить пост', reverse_lazy('blogs:post-create')),
    MenuItem('Список блогов', reverse_lazy('blogs:blogs')),
    MenuItem('Мой блог', reverse_lazy('blogs:own-posts')),
    MenuItem('Выйти', reverse_lazy('blogs:logout'))
]
