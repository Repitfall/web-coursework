from django.db import models


class UserRoles(models.Model):
    title = models.CharField(max_length=32, blank=False)


class Users(models.Model):
    role = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    login = models.CharField(max_length=32, blank=False, unique=True)
    password = models.CharField(max_length=256, blank=False)
    first_name = models.CharField(max_length=32, blank=False)
    last_name = models.CharField(max_length=32, blank=False)


class UserAddresses(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, blank=False)


class UserPays(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    data = models.CharField(max_length=256, blank=False)


class Restaurants(models.Model):
    title = models.TextField()
    info = models.TextField()


class RestaurantGroups(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    title = models.TextField()
    info = models.TextField()


class RestaurantDishes(models.Model):
    group = models.ForeignKey(RestaurantGroups, on_delete=models.CASCADE)
    title = models.TextField()
    info = models.TextField()


class DishAttributes(models.Model):
    dish = models.ForeignKey(RestaurantDishes, on_delete=models.CASCADE)
    title = models.TextField()
    info = models.TextField()


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
    courier = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='courier')
    date = models.DateTimeField(blank=False)
    pay = models.ForeignKey(UserPays, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddresses, on_delete=models.CASCADE)


class OrderDishes(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    dish = models.ForeignKey(RestaurantDishes, on_delete=models.CASCADE)
    count = models.IntegerField()


class OrderAttributes(models.Model):
    dish = models.ForeignKey(OrderDishes, on_delete=models.CASCADE)
    attribute = models.ForeignKey(DishAttributes, on_delete=models.CASCADE)
    data = models.CharField(max_length=8, blank=False)


class Tickets(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    text = models.TextField()
