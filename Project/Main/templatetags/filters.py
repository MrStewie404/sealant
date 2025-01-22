from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='string_cutter')
def string_cutter(value, length):
    """
    Обрезает строку до указанной длины и добавляет троеточие.
    """
    if not isinstance(value, str):
        return value
    if not isinstance(length, int):
        return value
    if len(value) <= length:
        return value
    return format_html("{}...", value[:length])

@register.filter(name='in_group')
def in_any_group(group, groups_to_check):
    return any(g in group for g in groups_to_check.split(','))