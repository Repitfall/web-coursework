from django.contrib import admin
from .models import UserRoles, Users, UserAddresses, UserPays, Restaurants, RestaurantGroups, RestaurantDishes, DishAttributes, Orders, OrderDishes, OrderAttributes

admin.site.register(UserRoles)
admin.site.register(Users)
admin.site.register(UserAddresses)
admin.site.register(UserPays)
admin.site.register(Restaurants)
admin.site.register(RestaurantGroups)
admin.site.register(RestaurantDishes)
admin.site.register(DishAttributes)
admin.site.register(Orders)
admin.site.register(OrderDishes)
admin.site.register(OrderAttributes)
