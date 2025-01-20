import re
from rest_framework import serializers
from .models import (
    UserAddress,
    Courier,
    Restaurant,
    RestaurantGroup,
    RestaurantDish,
    Order,
    OrderDish,
    Ticket,
)
from django.contrib.auth.models import User


# ТРЕТИЙ СПОСОБ ВАЛИДАЦИИ
def is_username_unique(value):
    if User.objects.filter(login=value).exists():
        raise serializers.ValidationError("Данный логин уже занят")
    return value


class UserSerializer(serializers.ModelSerializer):
    login = serializers.CharField(validators=[is_username_unique])

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    # ПЕРВЫЙ СПОСОБ ВАЛИДАЦИИ
    def validate(self, values):
        if not re.match(r"^[А-Яа-я\s]+$", values["first_name"]):
            raise serializers.ValidationError(
                "Имя пользователя может содержать только символы кириллицы"
            )

        if not re.match(r"^[А-Яа-я\s]+$", values["last_name"]):
            raise serializers.ValidationError(
                "Фамилия пользователя может содержать только символы кириллицы"
            )
        return values

    # ВТОРОЙ СПОСОБ ВАЛИДАЦИИ
    def validate_password(self, value):
        if len(value) != 64:
            raise serializers.ValidationError("Неправильный хэш пароля")
        if not re.match(r"^[0-9a-f]+$", value):
            raise serializers.ValidationError("Неправильный хэш пароля")


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"

    def validate(self, values):
        if not re.match(r"^[А-Яа-я\s]+$", values["address"]):
            raise serializers.ValidationError(
                "Адрес может содержать только символы кириллицы"
            )


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = "__all__"

    def validate(self, values):
        if not re.match(r"^[А-Яа-я\s]+$", values["first_name"]):
            raise serializers.ValidationError(
                "Имя пользователя может содержать только символы кириллицы"
            )

        if not re.match(r"^[А-Яа-я\s]+$", values["last_name"]):
            raise serializers.ValidationError(
                "Фамилия пользователя может содержать только символы кириллицы"
            )
        return values


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"

    def validate(self, values):
        if not re.match(r"^[А-Яа-я0-9\s]+$", values["title"]):
            raise serializers.ValidationError(
                "Название может содержать только символы кириллицы"
            )


class RestaurantGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantGroup
        fields = "__all__"


class RestaurantDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDish
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDish
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
