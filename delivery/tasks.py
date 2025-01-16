from celery import shared_task
from django.db.models import Q
from django.core.cache import cache
from django.core.mail import send_mail
from .models import RestaurantDish
from .serializers import RestaurantDishSerializer


@shared_task
def mail_send(recipient_email, subject, message):
    send_mail(subject, message, 'noreply@example.com', [recipient_email], fail_silently=False)
    return "Письмо отправлено!"

@shared_task
def cache_dishes_recommended():
    cache_key = "dishes_recommdended"
    dishes = RestaurantDishSerializer(
        RestaurantDish.objects.filter(
            (
                Q(id_group__id_restaurant__title="Бургер Кинг")
                | Q(id_group__id_restaurant__title="Rostic's")
                )
            & ~Q(price__gte=300)
        ),
        many=True,
    )
    cache.set(cache_key, dishes, timeout=60*60)