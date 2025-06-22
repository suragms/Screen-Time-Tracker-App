from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def time_options(value):
    """Convert a comma-separated string into a list of options."""
    return [x.strip() for x in value.split(',')]

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def div(value, arg):
    """Divide the value by the arg."""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return ''

@register.filter
def mul(value, arg):
    """Multiply the value by the arg."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return '' 