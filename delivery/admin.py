from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket

@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['login', 'first_name', 'last_name']
    search_fields = ['login']
    fields = ['last_name', 'first_name']

@admin.register(UserAddress)
class UserAddressAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id_user', 'address']
    list_filter = ['id_user']
    search_fields = ['address']

@admin.register(Courier)
class CourierAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['last_name', 'first_name']
    search_fields = ['last_name']

@admin.register(Restaurant)
class RestaurantAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(RestaurantGroup)
class RestaurantGroupAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'id_restaurant']
    list_editable = ['id_restaurant']
    list_filter = ['id_restaurant']
    search_fields = ['title']

@admin.register(RestaurantDish)
class RestaurantDishAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'id_group']
    list_editable = ['id_group']
    list_filter = ['id_group']
    search_fields = ['title']

@admin.register(RestaurantAttribute)
class RestaurantAttributeAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'id_dish']
    list_editable = ['id_dish']
    list_filter = ['id_dish']
    search_fields = ['title']

@admin.register(Order)
class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'id_user']
    search_fields = ['id_user']

@admin.register(OrderDish)
class OrderDishAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'id_order']
    search_fields = ['id_order']

@admin.register(OrderAttribute)
class OrderAttributeAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'id_dish']
    search_fields = ['id_dish']

@admin.register(Ticket)
class TicketAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id_order']
    search_fields = ['id_order']
    list_display_links = ['id_order']