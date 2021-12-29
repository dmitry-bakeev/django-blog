from django.template import Library

from blogs.menu import AUTHORIZED_MENU, STAFF_EXTENDED_MENU, UNAUTHORIZED_MENU


register = Library()


@register.simple_tag(takes_context=True)
def get_menu(context):
    request = context['request']
    user = request.user

    if user.is_authenticated:
        if user.is_staff:
            return AUTHORIZED_MENU + STAFF_EXTENDED_MENU
        return AUTHORIZED_MENU

    return UNAUTHORIZED_MENU
