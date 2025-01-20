from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.utils import timezone


class UserAddress(models.Model):
    id_user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="adresses",
    )
    address = models.CharField(verbose_name="Адрес", max_length=256)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Адрес пользователя"
        verbose_name_plural = "Адреса пользователей"

    def __str__(self):
        return self.address


class Courier(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=32)
    last_name = models.CharField(verbose_name="Фамилия", max_length=64)
    FOOT = "F"
    BICYCLE = "B"
    CAR = "C"
    COURIER_TYPE = {
        FOOT: "Пеший",
        BICYCLE: "На велосипеде",
        CAR: "На машине",
    }
    type = models.CharField(max_length=1, choices=COURIER_TYPE, default=FOOT)
    resume = models.FileField(verbose_name="Резюме", upload_to='couriers/', blank=True, null=True)
    url = models.URLField(verbose_name="Соцсеть для связи", blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.last_name + self.first_name

    class Meta:
        verbose_name = "Курьер"
        verbose_name_plural = "Курьеры"


class Restaurant(models.Model):
    title = models.CharField(verbose_name="Название", max_length=64)
    info = models.TextField(verbose_name="Описание", blank=True)
    logo = models.ImageField(verbose_name="Логотип", upload_to="logos/")
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"


class RestaurantGroup(models.Model):
    id_restaurant = models.ForeignKey(
        Restaurant,
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
        related_name="restaurant_groups",
    )
    title = models.CharField(verbose_name="Название", max_length=64)
    info = models.TextField(verbose_name="Описание", blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа блюд"
        verbose_name_plural = "Группы блюд"


class RestaurantDish(models.Model):
    id_group = models.ForeignKey(
        RestaurantGroup,
        verbose_name="Группа",
        on_delete=models.CASCADE,
        related_name="restaurant_dishes",
    )
    title = models.CharField(verbose_name="Название", max_length=128)
    price = models.IntegerField(verbose_name="Цена")
    info = models.TextField(verbose_name="Описание", blank=True)
    date_created = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class Order(models.Model):
    current_cart = models.BooleanField()
    id_user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    id_courier = models.ForeignKey(
        Courier, verbose_name="Курьер", on_delete=models.CASCADE, related_name="orders"
    )
    id_address = models.ForeignKey(
        UserAddress,
        verbose_name="Адрес доставки",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    dishes = models.ManyToManyField(to="RestaurantDish", through="OrderDish")
    comment = models.TextField(verbose_name="Комментарий")
    date_created = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return "Заказ" + str(self.id)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderDish(models.Model):
    id_order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        on_delete=models.CASCADE,
        related_name="order_dishes",
    )
    id_dish = models.ForeignKey(
        RestaurantDish,
        verbose_name="Блюдо",
        on_delete=models.CASCADE,
        related_name="order_dishes",
    )
    count = models.IntegerField(verbose_name="Количество")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id_order) + " | Блюдо " + str(self.id_dish)

    class Meta:
        verbose_name = "Заказанное блюдо"
        verbose_name_plural = "Заказанные блюда"


class Ticket(models.Model):
    id_order = models.ForeignKey(
        Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name="tickets"
    )
    comment = models.TextField(verbose_name="Комментарий")
    history = HistoricalRecords()

    def __str__(self):
        return "Тикет " + str(self.id)

    class Meta:
        verbose_name = "Тикет"
        verbose_name_plural = "Тикеты"
