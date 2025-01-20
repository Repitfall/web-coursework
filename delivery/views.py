from django.shortcuts import render
from django.db.models import Q
import django_filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout
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
from .serializers import (
    UserSerializer,
    UserAddressSerializer,
    CourierSerializer,
    RestaurantSerializer,
    RestaurantGroupSerializer,
    RestaurantDishSerializer,
    OrderSerializer,
    OrderDishSerializer,
    TicketSerializer,
)
from .forms import (
    LoginForm,
    RegisterForm
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id", "username", "last_name"]


class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id_user"]


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id", "last_name"]


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id", "title"]


class RestaurantGroupViewSet(viewsets.ModelViewSet):
    queryset = RestaurantGroup.objects.all()
    serializer_class = RestaurantGroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id", "title"]


class RestaurantDishFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gt", label="Минимальная цена"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lt", label="Максимальная цена"
    )

    class Meta:
        model = RestaurantDish
        fields = ["min_price", "max_price"]


class RestaurantDishViewSet(viewsets.ModelViewSet):
    queryset = RestaurantDish.objects.all()
    serializer_class = RestaurantDishSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["id", "title"]
    filterset_class = RestaurantDishFilter

    @action(methods=["GET"], detail=False)
    def recommended(self, request):
        cache_key = "dishes_recommdended"
        dishes = cache.get(cache_key)
        if dishes is None:
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
        return Response({"Рекомендованное": dishes.data})

    @action(methods=["GET"], detail=False)
    def premium(self, request):
        cache_key = "dishes_premium"
        dishes = cache.get(cache_key)
        if dishes is None:
            dishes = RestaurantDishSerializer(
                RestaurantDish.objects.filter(
                    (
                        Q(id_group__id_restaurant__title="Бургер Кинг")
                        | Q(id_group__id_restaurant__title="Вкусно - и точка")
                    )
                    & ~Q(price__lte=300)
                    & Q(id_group__title="Говядина")
                ),
                many=True,
            )
            cache.set(cache_key, dishes, timeout=60*60)
        return Response({"Премиум-бургеры": dishes.data})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id"]


class OrderDishViewSet(viewsets.ModelViewSet):
    queryset = OrderDish.objects.all()
    serializer_class = OrderDishSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id_order"]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    search_fields = ["id"]


def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    dodo_exists = Restaurant.objects.filter(title = "Додо Пицца").exists()
    min_price_dish = RestaurantDish.objects.aggregate(Min("price"))["price__min"]
    restaurants = Restaurant.objects.order_by("title")
    context = {
        'restaurants': restaurants,
        'min_price_dish': min_price_dish,
        'dodo_exists': dodo_exists,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return HttpResponse('Неверные данные')
            if not user.is_active:
                return HttpResponse('Аккаунт заблокирован')
            dj_login(request, user)
            request.session.set_expiry(300)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.set_password(form.cleaned_data['password'])
            user.save()
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')

def user_order(request):
    pass
