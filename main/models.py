from django.db import models


class Products(models.Model):
    hash = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    img = models.CharField(max_length=200)
    stock_balance = models.IntegerField(default=0)


class Couriers(models.Model):
    number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    is_busy = models.BooleanField(default=False)
    way = models.CharField(max_length=200)


class Delivery(models.Model):
    client = models.CharField(max_length=200)
    addres = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=200)
    products = models.CharField(max_length=200, default='')
    courier = models.CharField(max_length=200, default='')
