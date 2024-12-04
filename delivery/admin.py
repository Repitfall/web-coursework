from django.contrib import admin
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket

admin.site.register(User)
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

