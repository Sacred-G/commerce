from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def absolute_static_url(context, path):
    request = context['request']
    return request.build_absolute_uri(settings.STATIC_URL + path)