from django.shortcuts import render
from django.db.models import Q
import django_filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    Comment,
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
from .forms import LoginForm, RegisterForm, CommentForm


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
    date = django_filters.DateFromToRangeFilter(
        field_name="date_created", label="Диапазон дат публикации"
    )
    published = django_filters.BooleanFilter(
        field_name="published", label="В открытом доступе"
    )
    info = django_filters.CharFilter(lookup_expr="icontains", label="Описание")

    class Meta:
        model = RestaurantDish
        fields = ["min_price", "max_price", "date", "published", "info"]


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
            cache.set(cache_key, dishes, timeout=60 * 60)
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
            cache.set(cache_key, dishes, timeout=60 * 60)
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

    @action(methods=["POST"], detail=True)
    def change_order_dish(self, request, pk=None):
        order_dish = self.get_object()
        serializer = OrderDishSerializer(order_dish, data=request.data, partial=True)
        if serializer.is_valid():
            order_dish.save()
            return Response({"response": "Заказанное блюдо изменено"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    search_fields = ["id"]


def index(request, restaurant_slug=None, group_slug=None, id_dish=None):

    if id_dish:
        dish = get_object_or_404(RestaurantDish, id=id_dish)
        comments = Comment.objects.filter(id_dish=id_dish)
        context = {
            "dish": dish,
            "comments": comments,
        }
        return render(request, "dish.html", context)

    if restaurant_slug:
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
        groups = RestaurantGroup.objects.filter(id_restaurant=restaurant)
        dishes = []
        for group in groups:
            dishes += RestaurantDish.objects.filter(id_group=group).exclude(
                published=False
            )
        context = {
            "restaurant": restaurant,
            "groups": groups,
            "dishes": dishes,
        }

        if group_slug:
            group = get_object_or_404(
                RestaurantGroup, slug=group_slug, id_restaurant=restaurant
            )
            dishes = RestaurantDish.objects.filter(id_group=group).exclude(
                published=False
            )
            context = {
                "restaurant": restaurant,
                "groups": groups,
                "dishes": dishes,
            }

        return render(request, "groups.html", context)

    min_price_dish = RestaurantDish.objects.exclude(published=False).aggregate(Min("price"))["price__min"]
    restaurants = Restaurant.objects.order_by("title")
    context = {
        "restaurants": restaurants,
        "min_price_dish": min_price_dish,
    }
    return render(request, "index.html", context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user is None:
                return HttpResponse("Неверные данные")
            if not user.is_active:
                return HttpResponse("Аккаунт заблокирован")
            dj_login(request, user)
            request.session.set_expiry(3600)
            return redirect("/")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.set_password(form.cleaned_data["password"])
            user.save()
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")


def search(request):
    filter = request.GET.get("filter")
    if filter:
        if filter == "recommended":
            dishes = list(RestaurantDish.objects.filter(
                (
                    Q(id_group__id_restaurant__title="Бургер Кинг")
                    | Q(id_group__id_restaurant__title="Rostic's")
                )
                & ~Q(price__gte=300)
                ))
        elif filter == "less_price":
            dishes = RestaurantDish.objects.order_by("price").exclude(published=False)
        else:
            dishes = RestaurantDish.objects.exclude(published=False) 
    else:
        searching = request.GET.get("search")
        if searching:
            dishes = (
                RestaurantDish.objects.filter(title__icontains=searching)
                .exclude(published=False)
            )
        else:
            dishes = RestaurantDish.objects.exclude(published=False)
    count = len(dishes)
    context = {
        "dishes": dishes,
        "count": count
        }
    return render(request, "search.html", context)


@login_required
def comment_add(request, id_dish):
    dish = get_object_or_404(RestaurantDish, id=id_dish)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.id_dish = dish
            comment.id_user = request.user
            comment.save()
            return redirect("dish", id_dish=id_dish)
    else:
        form = CommentForm()
    context = {
        'form': form,
        'dish': dish,
    }
    return render(request, 'dish.html', context)

@login_required
def comment_edit(request, id_comment):
    comment = get_object_or_404(Comment, id=id_comment)
    if comment.id_user != request.user:
        return redirect('dish', id_dish=comment.id_dish.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        delete_file = request.POST.get('delete_file')
        if form.is_valid():
            if delete_file:
                comment.file.delete(save=False)
                comment.file = None
            form.save()
            return redirect('dish', id_dish=comment.id_dish.id)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'comment_edit.html', context)

@login_required
def comment_delete(request, id_comment):
    comment = get_object_or_404(Comment, id=id_comment)
    if comment.id_user != request.user:
        return redirect('dish', id_dish=comment.id_dish.id)
    dish_id = comment.id_dish.id
    comment.delete()
    return redirect('dish', id_dish=dish_id)
