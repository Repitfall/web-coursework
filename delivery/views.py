from django.shortcuts import render
from django.db.models import Q
import django_filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket
from .serializers import UserSerializer, UserAddressSerializer, CourierSerializer, RestaurantSerializer, RestaurantGroupSerializer, RestaurantDishSerializer, RestaurantAttributeSerializer, OrderSerializer, OrderDishSerializer, OrderAttributeSerializer, TicketSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'login', 'last_name']


class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id_user']


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'last_name']


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title']


class RestaurantGroupViewSet(viewsets.ModelViewSet):
    queryset = RestaurantGroup.objects.all()
    serializer_class = RestaurantGroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title']


class RestaurantDishFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = RestaurantDish
        fields = "__all__"


class RestaurantDishViewSet(viewsets.ModelViewSet):
    queryset = RestaurantDish.objects.all()
    serializer_class = RestaurantDishSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title']
    filterset_class = RestaurantDishFilter
    
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
    filter_backends = [SearchFilter]
    search_fields = ['title']

    @action(methods=["POST"], detail=True)
    def change_attribute(self, request, pk=None):
        attribute = self.get_object()
        serializer = RestaurantAttributeSerializer(attribute, data=request.data, partial=True)
        if serializer.is_valid():
            attribute.save()
            return Response({"response": "Атрибут изменён"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id']


class OrderDishViewSet(viewsets.ModelViewSet):
    queryset = OrderDish.objects.all()
    serializer_class = OrderDishSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id_order']


class OrderAttributeViewSet(viewsets.ModelViewSet):
    queryset = OrderAttribute.objects.all()
    serializer_class = OrderAttributeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id_dish']


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    search_fields = ['id']
