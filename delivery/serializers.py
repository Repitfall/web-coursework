from rest_framework import serializers
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantGroup
        fields = "__all__"


class RestaurantDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDish
        fields = "__all__"


class RestaurantAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantAttribute
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDish
        fields = "__all__"


class OrderAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAttribute
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"