from django import template
from django.utils.safestring import SafeString, mark_safe
from markdown import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text: str) -> SafeString:
    return mark_safe(markdown(text))
