from django import template
from ..models import Restaurant

register = template.Library()

@register.simple_tag
def count_restaurants():
    return Restaurant.objects.count()