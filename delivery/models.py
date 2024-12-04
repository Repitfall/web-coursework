from django.db import models

class User(models.Model):
    login = models.CharField(verbose_name="Логин", max_length=32, unique=True)
    password = models.CharField(verbose_name="Хэш-пароля", max_length=64)
    email = models.EmailField(verbose_name="Почта", max_length=128, unique=True)
    first_name = models.CharField(verbose_name="Имя", max_length=32)
    last_name = models.CharField(verbose_name="Фамилия", max_length=64)


class UserAddress(models.Model):
    id_user = models.ForeignKey(User, verbose_name="ID пользователя", on_delete=models.CASCADE)
    address = models.CharField(verbose_name="Адрес", max_length=256)


class Courier(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=32)
    last_name = models.CharField(verbose_name="Фамилия", max_length=64)


class Restaurant(models.Model):
    title = models.CharField(verbose_name="Название", max_length=64)
    info = models.TextField(verbose_name="Описание")


class RestaurantGroup(models.Model):
    id_restaurant = models.ForeignKey(Restaurant, verbose_name="ID ресторана", on_delete=models.CASCADE)
    info = models.TextField(verbose_name="Описание")


class RestaurantDish(models.Model):
    id_group = models.ForeignKey(RestaurantGroup, verbose_name="ID группы", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=128)
    info = models.TextField(verbose_name="Описание")


class RestaurantAttribute(models.Model):
    id_dish = models.ForeignKey(RestaurantDish, verbose_name="ID блюда", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=128)
    info = models.TextField(verbose_name="Описание")


class Order(models.Model):
    id_user = models.ForeignKey(User, verbose_name="ID пользователя", on_delete=models.CASCADE)
    id_courier = models.ForeignKey(Courier, verbose_name="ID курьера", on_delete=models.CASCADE)
    id_address = models.ForeignKey(UserAddress, verbose_name="ID адреса доставки", on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Комментарий")


class OrderDish(models.Model):
    id_order = models.ForeignKey(Order, verbose_name="ID заказа", on_delete=models.CASCADE)
    dish = models.ForeignKey(RestaurantDish, verbose_name="ID блюда", on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="Количество")


class OrderAttribute(models.Model):
    id_dish = models.ForeignKey(OrderDish, verbose_name="ID блюда в заказе", on_delete=models.CASCADE)
    id_attribute = models.ForeignKey(RestaurantAttribute, verbose_name="ID атрибута", on_delete=models.CASCADE)


class Tickets(models.Model):
    id_order = models.ForeignKey(Order, verbose_name="ID заказа", on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Комментарий")

