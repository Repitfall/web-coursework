from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket
from .serializers import UserSerializer, UserAddressSerializer, CourierSerializer, RestaurantSerializer, RestaurantGroupSerializer, RestaurantDishSerializer, RestaurantAttributeSerializer, OrderSerializer, OrderDishSerializer, OrderAttributeSerializer, TicketSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantGroupViewSet(viewsets.ModelViewSet):
    queryset = RestaurantGroup.objects.all()
    serializer_class = RestaurantGroupSerializer


class RestaurantDishViewSet(viewsets.ModelViewSet):
    queryset = RestaurantDish.objects.all()
    serializer_class = RestaurantDishSerializer
    
    @action(methods=["GET"], detail=False)
    def recommended(self, request):
        dishes = RestaurantDishSerializer(RestaurantDish.objects.filter(
            (Q(id_group__id_restaurant__title="Бургер Кинг") | Q(id_group__id_restaurant__title="Rostic's")) & ~Q(price__gte=300)
        ), many=True)
        return Response(
            {"Рекомендованное": dishes.data}
        )
    
    @action(methods=["GET"], detail=False)
    def premium(self, request):
        dishes = RestaurantDishSerializer(RestaurantDish.objects.filter(
            (Q(id_group__id_restaurant__title="Бургер Кинг") | Q(id_group__id_restaurant__title="Вкусно - и точка"))
            & ~Q(price__lte=300) & Q(id_group__title="Говядина")
        ), many=True)
        return Response(
            {"Премиум-бургеры": dishes.data}
        )


class RestaurantAttributeViewSet(viewsets.ModelViewSet):
    queryset = RestaurantAttribute.objects.all()
    serializer_class = RestaurantAttributeSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDishViewSet(viewsets.ModelViewSet):
    queryset = OrderDish.objects.all()
    serializer_class = OrderDishSerializer


class OrderAttributeViewSet(viewsets.ModelViewSet):
    queryset = OrderAttribute.objects.all()
    serializer_class = OrderAttributeSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
