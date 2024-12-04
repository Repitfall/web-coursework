from django.db import models

class User(models.Model):
    login
    password
    first_name
    last_name


class UserAddress(models.Model):
    id_user
    address


class Courier(models.Model):
    first_name
    last_name


class Restaurant(models.Model):
    title
    info


class RestaurantGroup(models.Model):
    id_restaurant
    info


class RestaurantDish(models.Model):
    id_group
    title
    info


class RestaurantAttribute(models.Model):
    id_dish
    title
    info


class Order(models.Model):
    id_user
    id_courier
    id_address
    comment


class OrderDish(models.Model):
    id_order
    dish
    count


class OrderAttribute(models.Model):
    id_dish
    id_attribute
    data


class Tickets(models.Model):
    id_order
    comment

