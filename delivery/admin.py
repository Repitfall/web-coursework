from django.contrib import admin
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['login', 'first_name', 'last_name']


admin.site.register(UserAddress)
admin.site.register(Courier)
admin.site.register(Restaurant)
admin.site.register(RestaurantGroup)
admin.site.register(RestaurantDish)
admin.site.register(RestaurantAttribute)
admin.site.register(Order)
admin.site.register(OrderDish)
admin.site.register(OrderAttribute)
admin.site.register(Ticket)

