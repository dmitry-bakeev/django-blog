from django.template import Library

from blogs.menu import UNATHORIZED_MENU, ATHORIZED_MENU


register = Library()


@register.simple_tag(takes_context=True)
def get_menu(context):
    request = context['request']

    if request.user.is_authenticated:
        return ATHORIZED_MENU

    return UNATHORIZED_MENU
