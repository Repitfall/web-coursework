from django import template
from ..models import Restaurant, RestaurantDish
from django.db.models import Q
from django.core.cache import cache
import random

register = template.Library()


@register.simple_tag
def count_restaurants():
    return Restaurant.objects.count()

@register.simple_tag
def min_price_dishes():
    dishes = RestaurantDish.objects.order_by("price")[:4]
    return dishes

@register.simple_tag
def recommended_dishes():
    dishes = list(RestaurantDish.objects.filter(
        (
            Q(id_group__id_restaurant__title="Бургер Кинг")
            | Q(id_group__id_restaurant__title="Rostic's")
        )
        & ~Q(price__gte=300)
        ))
    dishes = random.sample(dishes, 4)
    return dishes

@register.simple_tag
def count_recommended_dishes():
    dishes = list(RestaurantDish.objects.filter(
        (
            Q(id_group__id_restaurant__title="Бургер Кинг")
            | Q(id_group__id_restaurant__title="Rostic's")
        )
        & ~Q(price__gte=300)
        ))
    count = len(dishes)
    return count


