from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    """
    Checks if a string ends with the specified suffix.
    """
    if isinstance(value, str):
        return value.endswith(suffix)
    return False
