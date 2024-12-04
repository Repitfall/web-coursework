from django.contrib import admin
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['login', 'first_name', 'last_name']

@admin.register(UserAddress)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id_user', 'address']

@admin.register(Courier)
class UserAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name']

@admin.register(Restaurant)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(RestaurantGroup)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title', 'id_restaurant']

@admin.register(RestaurantDish)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title', 'id_group']

@admin.register(RestaurantAttribute)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title', 'id_dish']

@admin.register(Order)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_user']

@admin.register(OrderDish)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_order']

@admin.register(OrderAttribute)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_dish']

@admin.register(Ticket)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id_order']