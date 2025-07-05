from django import template

register = template.Library()

@register.filter(name='has_screen_permission')
def has_screen_permission(user, screen_name):
    try:
        return user.has_permission(screen_name)
    except Exception:
        return False
