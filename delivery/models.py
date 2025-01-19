from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.utils import timezone


class UserAddress(models.Model):
    id_user = models.ForeignKey(
        User, verbose_name="ID пользователя", on_delete=models.CASCADE, related_name="adresses"
    )
    address = models.CharField(verbose_name="Адрес", max_length=256)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Адреса пользователей"


class Courier(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=32)
    last_name = models.CharField(verbose_name="Фамилия", max_length=64)
    FOOT = "F"
    BICYCLE = "B"
    CAR = "C"
    COURIER_TYPE = {
        FOOT: "Foot",
        BICYCLE: "Bicycle",
        CAR: "Car",
    }
    type = models.CharField(max_length=1, choices=COURIER_TYPE, default=FOOT)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Курьеры"


class Restaurant(models.Model):
    title = models.CharField(verbose_name="Название", max_length=64)
    info = models.TextField(verbose_name="Описание", blank=True)
    logo = models.ImageField(verbose_name="Логотип", upload_to ='uploads/')
    history = HistoricalRecords()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Рестораны"


class RestaurantGroup(models.Model):
    id_restaurant = models.ForeignKey(
        Restaurant, verbose_name="ID ресторана", on_delete=models.CASCADE, related_name="groups"
    )
    title = models.CharField(verbose_name="Название", max_length=64)
    info = models.TextField(verbose_name="Описание", blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Группы блюд"


class RestaurantDish(models.Model):
    id_group = models.ForeignKey(
        RestaurantGroup, verbose_name="ID группы", on_delete=models.CASCADE, related_name="dishes"
    )
    title = models.CharField(verbose_name="Название", max_length=128)
    price = models.IntegerField(verbose_name="Цена")
    info = models.TextField(verbose_name="Описание", blank=True)
    date_created = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    date_published = models.DateField(verbose_name="Дата опубликования", auto_now_add=True)
    date_updated = models.DateField(verbose_name="Дата изменения", auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Блюда"


class RestaurantAttribute(models.Model):
    id_dish = models.ForeignKey(
        RestaurantDish, verbose_name="ID блюда", on_delete=models.CASCADE, related_name="attributes"
    )
    title = models.CharField(verbose_name="Название", max_length=128)
    info = models.TextField(verbose_name="Описание", blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name_plural = "Атрибуты блюд"


class Order(models.Model):
    id_user = models.ForeignKey(
        User, verbose_name="ID пользователя", on_delete=models.CASCADE, related_name="orders"
    )
    id_courier = models.ForeignKey(
        Courier, verbose_name="ID курьера", on_delete=models.CASCADE, related_name="orders"
    )
    id_address = models.ForeignKey(
        UserAddress, verbose_name="ID адреса доставки", on_delete=models.CASCADE, related_name="orders"
    )
    comment = models.TextField(verbose_name="Комментарий")
    date_created = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    date_updated = models.DateField(verbose_name="Дата изменения", auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Заказы"


class OrderDish(models.Model):
    id_order = models.ForeignKey(
        Order, verbose_name="ID заказа", on_delete=models.CASCADE, related_name="order_dishes"
    )
    dish = models.ForeignKey(
        RestaurantDish, verbose_name="ID блюда", on_delete=models.CASCADE, related_name="order_dishes"
    )
    count = models.IntegerField(verbose_name="Количество")
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Заказанные блюда"


class OrderAttribute(models.Model):
    id_dish = models.ForeignKey(
        OrderDish, verbose_name="ID блюда в заказе", on_delete=models.CASCADE, related_name="order_attributes"
    )
    id_attribute = models.ForeignKey(
        RestaurantAttribute, verbose_name="ID атрибута", on_delete=models.CASCADE, related_name="order_attributes"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Атрибуты заказанных блюд"


class Ticket(models.Model):
    id_order = models.ForeignKey(
        Order, verbose_name="ID заказа", on_delete=models.CASCADE, related_name="tickets"
    )
    comment = models.TextField(verbose_name="Комментарий")
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Тикеты"
