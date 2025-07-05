import re
from django import template

register = template.Library()

@register.filter
def regex_replace(value, args):
    """Aplica re.sub com padrão e substituição"""
    try:
        pattern, replacement = args.split('|')
        return re.sub(pattern, replacement, str(value))
    except Exception:
        return value