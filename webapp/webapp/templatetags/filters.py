from django import template

register = template.Library()


@register.filter
def isExist(value, arg):
    """Removes all values of arg from the given string"""
    return arg in value
